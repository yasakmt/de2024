provider "aws" {
  region = "us-east-1"
}

module "iam_for_lambda" {
  source = "./modules/IAM"
}

module "lambda" {
  source = "./modules/lambda"
  lambda_etl_role = module.iam_for_lambda.lambda_etl_role

}

module "s3_de" {
  source = "./modules/s3"
  s3_bucket_name  = var.s3_bucket_name
  create_folder = var.create_folder
  customers_queue_arn = module.sqs_queue.customers_queue_arn
  transactions_queue_arn = module.sqs_queue.transactions_queue_arn
  products_queue_arn = module.sqs_queue.products_queue_arn
  erasure_queue_arn = module.sqs_queue.erasure_queue_arn
}

module "sqs_queue" {
  source = "./modules/sqs"
  s3_bucket_arn = module.s3_de.s3_bucket_arn
}


module "dynamodb" {
  source = "./modules/dynamodb"

}
