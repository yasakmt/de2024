output "lambda_etl_role" {
  value = aws_iam_role.lambda_execution_role.arn
}
