import boto3
from collections import defaultdict
import json
import gzip
from io import BytesIO
import os
import logging
from urllib.parse import unquote
import hashlib
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#DynamoDB client
dynamodb_client = boto3.client('dynamodb')

# Cache for storing primary keys, organized by table name
primary_key_cache = defaultdict(set)

#Fetching primary keys from DynamoDB tables to cache them
def fetch_primary_keys(table_name, primary_key_attribute_name):
    print("Fetching primary keys from DynamoDB tables to cache them")
    # Pagination support
    last_evaluated_key = None
    while True:
        # Fetching a batch of items from the table
        scan_kwargs = {
            'TableName': table_name,
            'ProjectionExpression': primary_key_attribute_name,
        }
        if last_evaluated_key:
            scan_kwargs['ExclusiveStartKey'] = last_evaluated_key

        response = dynamodb_client.scan(**scan_kwargs)

        # Updating cache with primary keys
        for item in response.get('Items', []):
            primary_key = item[primary_key_attribute_name]['S']
            primary_key_cache[table_name].add(primary_key)

        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            break
#Fetch and cache primary keys for all specified tables on cold start
def cache_all_primary_keys():

    tables_and_keys = {
        'customerstb': 'id',
        'products':'sku',
        'transactions': 'transaction_id'

    }

    for table, key in tables_and_keys.items():
        fetch_primary_keys(table, key)
    print("Primary keys for all tables fetched and cached.")

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('customerstb')


def validate_total_cost(record):
    # To validate purchase total and total_cost as per the problem statement
    total_cost = float(record['purchases']['total_cost'])
    calculated_total = sum(float(product['total']) for product in record['purchases']['products'])
    return total_cost == calculated_total

def validate_products_record(record):
    # Making sure  'popularity' and 'price' exist in the record and as per the problem statement.
    popularity_condition = record.get('popularity', 0) > 0
    price_condition = Decimal(record.get('price', 0)) > 0

    if popularity_condition and price_condition:
        print("Record is valid.")
        return True
    else:
        print("Record is invalid.")
        return False

def convert_floats_to_decimals_and_sku_to_string(obj):
    #Covenrting flo values to decimal, and sku to string before inserting the record to DynamamoDB table
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'sku':
                obj[k] = str(v)
            else:
                obj[k] = convert_floats_to_decimals_and_sku_to_string(v)
    elif isinstance(obj, list):
        obj = [convert_floats_to_decimals_and_sku_to_string(v) for v in obj]
    elif isinstance(obj, float):
        return Decimal(str(obj))
    return obj

#HASH_PII #For Erasure-requests only
def hash_pii(value):
    """Hashing the PII value using SHA-256"""
    if value is None:
        placeholder = "placeholder_for_none"
        return hashlib.sha256(placeholder.encode()).hexdigest()
    else:
        return hashlib.sha256(value.encode()).hexdigest()

# Following fields in customers table will be anonymized: 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'address', 'email'.
def update_customer_fields(customer_id=None, email=None):

    key = None
    original_item = {}

    if customer_id:
        key = {'id': customer_id}
        try:
            response = table.get_item(Key=key)
            original_item = response.get('Item', {})
        except Exception as e:
            return f"Failed to fetch item by customer ID: {str(e)}"
    elif email:
        #Quering using a GSI for email
        index_name = 'EmailIndex'  # The name of the GSI for email
        try:
            response = table.query(
                IndexName=index_name,
                KeyConditionExpression='email = :email',
                ExpressionAttributeValues={':email': email}
            )
            items = response.get('Items', [])
            if not items:
                return "No matching customer found by email."
            # Assuming email is unique, and taking the first match
            key = {'id': items[0]['id']}
            original_item = items[0]
        except Exception as e:
            return f"Failed to fetch item by email: {str(e)}"
    else:
        return "No identifier provided."

    if not original_item:
        return "No matching customer found."

    # Anonymizing fields
    fields_to_anonymize = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'address', 'email']
    anonymized_values = {field: hash_pii(original_item[field]) for field in fields_to_anonymize if field in original_item}

    # preparing update expression
    update_expression = "SET " + ", ".join([f"{k} = :{k}" for k in anonymized_values.keys()])
    expression_attribute_values = {f":{k}": v for k, v in anonymized_values.items()}

    # Update the item in DynamoDB
    try:
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response
    except Exception as e:
        return f"Error updating item: {str(e)}"


def lambda_handler(event, context):
    cache_all_primary_keys()
    print(primary_key_cache)
    table_mappings = {
        'customers': 'customerstb',
        'transactions':'transactions',
        'products' : 'products',
        'erasure-requests':'customerstb',
    }
    logger.info("Event: " + json.dumps(event))

    for record in event['Records']:
        body = json.loads(record['body'])
        records = body['Records']
        print(records)
        for s3_record in records:
            # Extracting the bucket name and key from the record
            bucket_name = s3_record['s3']['bucket']['name']
            key = s3_record['s3']['object']['key']
            print(f"Bucket Name: {bucket_name}")
            print(f"Object Key: {key}")

    file_prefix = key.split('/')[-1].split('.')[0]
    table_name = table_mappings.get(file_prefix)
    print(f"Processing: {file_prefix} for {table_name}")


    if not table_name:
        print(f"No table mapping found for file: {key}")
        return "No table mapping found"

    table = dynamodb.Table(table_name)

    response = s3_client.get_object(Bucket=bucket_name, Key=unquote(key))
    file_content = response['Body'].read()
    print(BytesIO(file_content))

    if key.endswith('.gz'):
        file_stream = gzip.GzipFile(fileobj=BytesIO(file_content), mode='rb')
    elif key.endswith('.json'):
        file_stream = BytesIO(file_content)
    else:
        print("Unsupported file format")
        return

    print(f"received json file: {file_prefix} for table {table_name}" )

    valid_records = []
    required_fields_cust = ['id', 'first_name', 'last_name', 'email']
    required_fields_tranx = ['transaction_id','customer_id']
    required_fields_products = ['sku','price','popularity']
    required_fields_erasure = ['customer-id', 'email']

    with file_stream as f:
        for line in f:
            try:
                # Decode each line as JSON
                record = json.loads(line.decode('utf-8'))

                print(record)

                # Checking if all required fields are present and not empty
                print("Checking if all required fields are present in the record and not empty")
                if table_name == "customerstb" and  all(record.get(field) for field in required_fields_cust):
                    if not any(record["id"] == r["id"] for r in valid_records) and record["id"] not in primary_key_cache['customerstb']:
                        valid_records.append(record)
                    else:
                        print(f"Duplicate id in the json record or id already exist in the table: {record}" )

                elif table_name == "transactions" and all(record.get(field) for field in required_fields_tranx) and validate_total_cost(record):
                    if not any(record["transaction_id"] == r["transaction_id"] for r in valid_records) and record["customer_id"] in primary_key_cache['customerstb']:
                        valid_records.append(record)
                    else:
                        print(f"Duplicate record, or record not valid, or customer id not exist in customers table: {record}")


                elif table_name == "products" and all(record.get(field) for field in required_fields_products) and validate_products_record(record):
                     updated_record = convert_floats_to_decimals_and_sku_to_string(record)
                     #convert_floats_to_decimals_and_sku_to_string(record) and valid_records.append(record)
                     if updated_record['sku'] in primary_key_cache['products']:
                         print(f"sku already exist hence skipping the record: {updated_record}")
                     else:
                         valid_records.append(updated_record)


                elif file_prefix == "erasure-requests" and any(record.get(field) for field in required_fields_erasure):
                         print("Processing Erasure dataset to update the records in 'customerstb' table in dynamodb")
                          # Assuming the key name 'customer-id' is always consistent.
                         valid_records.append(record)

                else:
                    print("Record missing required fields or contains empty values. Skipping record.")


            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from line: {e}")


    if file_prefix!="erasure-requests":
        print(f"Final step for processing valid records in {file_prefix}")
        for record in valid_records:
            try:
                table.put_item(Item=record)
                print(f"Inserted following record: {record} in {table_name}")
            except Exception as e:
                print(f"Error inserting item: {e}")

    elif file_prefix == 'erasure-requests':
        print(f"Checking records for availability of customer-id or email to complete the final steps in processing {file_prefix}")
        for record in valid_records:
          email = record.get('email')

          if 'customer-id' in record:
              record['id'] = record.pop('customer-id')
              customer_id = record.get('id')
              print(f"Processing the record in erasure-requests file for customer_id: {customer_id}")
              print(update_customer_fields(customer_id=customer_id, email=None))
          elif email:
              print(f"customer-id not found in the record. But the record have 'email' hence processing the record to anonymize all the PII fields including {email}")
              print(update_customer_fields(customer_id=None, email=email))

          else:
            print(f"'cusotmer-id' and 'email' not found in the record: {record}")


    return {
        'statusCode': 200,
        'body': json.dumps('Processing completed successfully!')
    }
