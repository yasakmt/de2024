resource "aws_s3_bucket" "s3_de" {
  bucket = var.s3_bucket_name
  tags = {
    Name        = "de"
    Environment = "dev"
  }
}
resource "aws_s3_object" "create_folder" {
  bucket = aws_s3_bucket.s3_de.id
  key = "${var.create_folder}/"
  content = var.put_an_object
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.s3_de.id

  queue {
    id      = "customers-event"
    queue_arn     = var.customers_queue_arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = "customers.json.gz"
  }

  queue {
    id      = "transactions-event"
    queue_arn     = var.transactions_queue_arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = "transactions.json.gz"
  }

  queue {
    id      = "products-event"
    queue_arn     = var.products_queue_arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = "products.json.gz"
  }
  queue {
    id      = "erasure-requests-event"
    queue_arn     = var.products_queue_arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = "erasure-requests.json.gz"
  }

}
