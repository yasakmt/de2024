variable "s3_bucket_name" {
  type = string
  default = "yasa-de-us-east-01"
}

variable "aws_region" {
  type = string
  default = "us-east-1"
}

variable "aws_account_id" {
  type = string
  default = "05824243187" #I removed few digits from the number. Now this acct number is incorrect.
}


variable "s3_bucket_arn" {
  type = string
}

####customers, transaction, products, erasure-request queues####
variable "sqs_queue_name" {
  description = "sqs queue name for customers dataset"
  type = string
  default = "de-customers"
}

variable "sqs_transactions_queue_name" {
  type = string
  default = "de-transactions"
}

variable "sqs_products_queue_name" {
  type = string
  default = "de-products"
}

variable "sqs_erasure_requests_queue_name" {
  type = string
  default = "de-erasure-requests"
}
