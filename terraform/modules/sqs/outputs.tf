output "customers_queue_arn" {
  value = aws_sqs_queue.terraform_queue.arn
}

output "transactions_queue_arn" {
  value = aws_sqs_queue.transactions_queue.arn
}

output "products_queue_arn" {
  value = aws_sqs_queue.products_queue.arn

}

output "erasure_queue_arn" {
  value = aws_sqs_queue.erasure_requests_queue.arn

}
