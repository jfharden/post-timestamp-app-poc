variable "app_name" {
  type        = string
  description = "Name to call created resources, used as a prefix in a small number of circumstances"
  default     = "jfharden-poc"
}

variable "aws_region" {
  type        = string
  description = "AWS Region"
  default     = "eu-west-2" // London
}

variable "environment" {
  type        = string
  description = "Environment (e.g. dev, integration, staging, prod, etc)"
  default     = "dev"
}

variable "resource_group_tag_name" {
  type        = string
  description = "A tag will be added to every resource (which supports tagging) which has this as the key. The value will be the app_name"
  default     = "project"
}
