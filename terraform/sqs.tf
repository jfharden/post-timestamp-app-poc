module "app_queues" {
  source                        = "./sqs_queue/"
  aws_region                    = var.aws_region
  name                          = var.app_name
  kms_key_arn                   = aws_kms_key.app.arn
  kms_key_id                    = aws_kms_key.app.id
  low_priority_alert_sns_topic  = aws_sns_topic.alerts_low_priority.arn
  high_priority_alert_sns_topic = aws_sns_topic.alerts_high_priority.arn
  tags                          = local.tags
}
