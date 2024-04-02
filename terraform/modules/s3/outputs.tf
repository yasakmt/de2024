output "s3_bucket_arn" {
  value = aws_s3_bucket.s3_de.arn
}

output "s3_bucket_name" {
  value = aws_s3_bucket.s3_de.bucket
}
