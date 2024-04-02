variable "s3_bucket_name" {
  type = string
}

variable "create_folder" {
  type = string
}

variable "put_an_object" {
  type = string
  default = "/dev/null"

}

variable "customers_queue_arn" {
  type = string

}

variable "transactions_queue_arn" {
  type = string

}

variable "products_queue_arn" {
  type = string

}

variable "erasure_queue_arn" {
  type = string

}
