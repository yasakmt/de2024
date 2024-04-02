resource "aws_lambda_function" "etl-lambda-funtion" {

  filename      = "C:/Users/removed/removed/removed/etl-lambda-fun.zip"
  function_name = "lambda_function"
  role          = var.lambda_etl_role
  handler       = "lambda_function.lambda_handler"

  #source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.12"

}
