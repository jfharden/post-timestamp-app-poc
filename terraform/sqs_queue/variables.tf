variable "aws_region" {
  type        = string
  description = "AWS Region"
}

variable "name" {
  type        = string
  description = "Name of the queue, DLQ will be <name>-dlq, s3 dead letter bucket will be <name>-dead-letters"
}

variable "kms_key_arn" {
  type        = string
  description = "KMS Key ARN for queue and s3 encryption"
}

variable "kms_key_id" {
  type        = string
  description = "KMS Key ID for queue and s3 encryption"
}

variable "low_priority_alert_sns_topic" {
  type        = string
  description = "SNS topic to send low priority alerts to"
}

variable "high_priority_alert_sns_topic" {
  type        = string
  description = "SNS topic to send high priority alerts to"
}

variable "tags" {
  type        = map(string)
  description = "Map of tags to add to all resources"
}
