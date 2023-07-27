variable "AWS_AECCESS_KEY" {
  type        = string
  description = "AWS access key"
  sensitive   = true
}

variable "AWS_AECCESS_KEY_SECRET" {
  type        = string
  description = "AWS access key secret"
  sensitive   = true
}

variable "AWS_REGION" {
  type        = string
  description = "AWS region"
  default     = "ap-northeast-2"
}

variable "lambda_build_bucket" {
  type        = string
  description = "S3 bucket for lambda build"
  default     = "atcoder-readme-stats--build"
}
