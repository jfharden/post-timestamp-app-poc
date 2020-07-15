output "queue_arn" {
  description = "ARN for the SQS queue"
  value       = aws_sqs_queue.app.arn
}

output "queue_id" {
  description = "SQS Queue URL"
  value = aws_sqs_queue.app.id
}

output "dlq_arn" {
  description = "ARN for the dead letter SQS queue"
  value       = aws_sqs_queue.dead_letter.arn
}
