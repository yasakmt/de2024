# Objective

My objective was to develop a aws lambda funtion to process the given "test-data" by implementing all the contraints and dependancies mentioned in the problem statement. 

# Solution

The solution was implemted using serverless approach. I used one S3 bucket, One Lambda function, 4 SQS queues for four types of files, and three DynamoDB tables.

# Steps to verify my lambda_funtion

My code can be tested with AWS Lambda's inbuild functionality. The Test event is provided below.  

Create follwing three DynamoDB tables with default configs:
Table name "customerstb" with id(string) as primary key.
Table name "products" with sku(string) as primary key.
Table "transactions" with transactions_id(string) as primary key.

Test event json for lambda funtion:
Replace the text in bold with your s3 bucket and object to process the test data.

{
  "Records": [
    {
      "messageId": "07f25304-a486-41ff-878d-e8c06927d4f9",
      "receiptHandle": "AQEBPTSzH1cxeR+wwYkxQqnHNlF24tTp/FahUrmfwaqNr+7JiSI+iJZsIurYJU6hSwcxMxUuPG4uk7WRGRl+0Fjc7NVOiJ3+GKbWEPTkkJT40sdIdbKyPT41dbmiDdepJH22Y5xnTdPDOk0BIYJWuHnKhwOT+8JWl9GAenWCuG5aTkk8rZx6BCEXu42yt1dF99Zoc4qcOSZy0SIKsDRVheIWFZ+Rnq4r1pjA5RDyR0eIKZAJ0z4PldkuOrRuY4NZueHpSSs87Yma3yuWGVwp1e/7Xi6UZ3UOhNI/GgrjTdIm/gSLq5ImdRBtoNNWj/OH8FlXgDAq/SsxPGAenq/7GiME8YX1JQNvU0hSiUTBquqOikuR6RkSNjzT6LByaZiNQMkd57nnJe025B37ghhwUsVa+w==",
      "body": "{\"Records\":[{\"eventVersion\":\"2.1\",\"eventSource\":\"aws:s3\",\"awsRegion\":\"us-east-1\",\"eventTime\":\"2024-03-27T16:13:05.644Z\",\"eventName\":\"ObjectCreated:Put\",\"userIdentity\":{\"principalId\":\"A2OD2O6XU255T\"},\"requestParameters\":{\"sourceIPAddress\":\"90.213.3.26\"},\"responseElements\":{\"x-amz-request-id\":\"Z5C22K4003CSVBJ8\",\"x-amz-id-2\":\"1hBHpLNt57eCoJdH3wiiHFtAv1hqElpAfaNJUdHRIBxquZM4brQqjD0sGEOPu7mySmT5wOGvjgFsIUy8zdSDw+ckWvVZuMGb\"},\"s3\":{\"s3SchemaVersion\":\"1.0\",\"configurationId\":\"event2sqs\",\"bucket\":{\"name\":\"**yasa-sqs**\",\"ownerIdentity\":{\"principalId\":\"A2OD2O6XU255T\"},\"arn\":\"arn:aws:s3:::**yasa-sqs**\"},\"**object\":{\"key\":\"products.json.gz**\",\"size\":254,\"eTag\":\"79af9538ae357947fcc565ac12aaf4a2\",\"sequencer\":\"006604459198A97878\"}}}]}",
      "attributes": {
        "ApproximateReceiveCount": "3",
        "SentTimestamp": "1711555986707",
        "SenderId": "AROA4R74ZO52XAB5OD7T4:S3-PROD-END",
        "ApproximateFirstReceiveTimestamp": "1711555986719"
      },
      "messageAttributes": {},
      "md5OfBody": "36439d4dd1cbd1309b4d43322f891f5c",
      "eventSource": "aws:sqs",
      "eventSourceARN": "arn:aws:sqs:us-east-1:05424318:products-sqs",
      "awsRegion": "us-east-1"
    }
  ]
}


