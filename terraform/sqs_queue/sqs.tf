resource "aws_sqs_queue" "app" {
  name = var.name

  message_retention_seconds = 1209600 // 14 days
  kms_master_key_id         = var.kms_key_id

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dead_letter.arn
    maxReceiveCount     = 20
  })

  tags = var.tags
}

resource "aws_sqs_queue" "dead_letter" {
  name = "${var.name}-dlq"

  message_retention_seconds = 1209600 // 14 days
  kms_master_key_id         = var.kms_key_id
  tags                      = var.tags
}
