resource "aws_sqs_queue" "terraform_queue" {
  name                      = var.sqs_queue_name
  policy = templatefile("${path.module}/sqs_iam_policy.json", {
    aws_account_id = var.aws_account_id,
    aws_region = var.aws_region,
    sqs_queue_name = var.sqs_queue_name,
    s3_bucket_name = var.s3_bucket_arn

  })

  tags = {
    de = "dev"
  }
}

resource "aws_sqs_queue" "transactions_queue" {
  name                      = var.sqs_transactions_queue_name
  policy = templatefile("${path.module}/sqs_iam_policy.json", {
    aws_account_id = var.aws_account_id,
    aws_region = var.aws_region,
    sqs_queue_name = var.sqs_transactions_queue_name,
    s3_bucket_name = var.s3_bucket_arn

  })

  tags = {
    de = "dev"
  }
}

resource "aws_sqs_queue" "products_queue" {
  name                      = var.sqs_products_queue_name
  policy = templatefile("${path.module}/sqs_iam_policy.json", {
    aws_account_id = var.aws_account_id,
    aws_region = var.aws_region,
    sqs_queue_name = var.sqs_products_queue_name,
    s3_bucket_name = var.s3_bucket_arn

  })

  tags = {
    de = "dev"
  }
}

resource "aws_sqs_queue" "erasure_requests_queue" {
  name                      = var.sqs_erasure_requests_queue_name
  policy = templatefile("${path.module}/sqs_iam_policy.json", {
    aws_account_id = var.aws_account_id,
    aws_region = var.aws_region,
    sqs_queue_name = var.sqs_erasure_requests_queue_name,
    s3_bucket_name = var.s3_bucket_arn

  })

  tags = {
    de = "dev"
  }
}
