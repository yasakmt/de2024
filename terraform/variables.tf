variable "s3_bucket_name" {
  description = "bucket name"
  type = string
  default = "yasa-de-us-east-01"
}

variable "create_folder" {
  description = "s3 folder name"
  type = string
  default = "data/"
}

variable "put_an_object" {
  description = "s3 object"
  type = string
  default = "/dev/null"
}







