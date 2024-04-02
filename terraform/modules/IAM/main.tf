resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda_policy_etl"
  description = "Policy that allows lambda function to interact with SQS, S3, and DynamoDB"
  policy      = templatefile("${path.module}/lambda_iam_policy.json",{
    aws_account_id = var.aws_account_id,
    aws_region = var.aws_region,
    s3_bucket_name = var.s3_bucket_name
    sqs_queue_name = var.sqs_queue_name
    sqs_transactions_queue_name = var.sqs_transactions_queue_name
    sqs_products_queue_name = var.sqs_products_queue_name
    sqs_erasure_requests_queue_name = var.sqs_erasure_requests_queue_name

  })
}

# Defining an IAM policy document for assuming the role
data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_execution_role" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_etl_policy" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}



