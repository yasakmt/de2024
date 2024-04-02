#Creates three Dynamodb tables with primary keys.
resource "aws_dynamodb_table" "dynamodb-table-customers" {
  name           = "customers"
  hash_key       = "id"
  billing_mode     = "PAY_PER_REQUEST"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }


  global_secondary_index {
    name               = "EmailIndex"
    hash_key           = "email"
    projection_type    = "ALL"

  }

  tags = {
    Name        = "de"
    Environment = "dev"
  }
}

resource "aws_dynamodb_table" "dynamodb-table-transactions" {
  name           = "transactions"
  hash_key       = "transactions_id"
  billing_mode     = "PAY_PER_REQUEST"

  attribute {
    name = "transactions_id"
    type = "S"
  }

  tags = {
    Name        = "de"
    Environment = "dev"
  }
}

resource "aws_dynamodb_table" "dynamodb-table-products" {
  name           = "products"
  hash_key       = "sku"
  billing_mode     = "PAY_PER_REQUEST"

  attribute {
    name = "sku"
    type = "S"
  }

  tags = {
    Name        = "de"
    Environment = "dev"
  }
}
