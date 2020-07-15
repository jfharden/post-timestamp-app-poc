resource "aws_dynamodb_table" "app" {
  name         = "${var.app_name}-timestamps"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "Timestamp"
  range_key    = "RequestId"

  attribute {
    name = "Timestamp"
    type = "S"
  }

  attribute {
    name = "RequestId"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.app.arn
  }

  tags = local.tags
}
