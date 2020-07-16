module "lambda_dlq_to_s3" {
  source = "github.com/claranet/terraform-aws-lambda?ref=v1.2.0"

  function_name = "${var.name}-dlq-to-s3"
  handler       = "lambda_handler.lambda_handler"

  source_path = abspath("${path.module}/../../lambdas/sqs_to_s3")
  description = "Deliver dead letter queue messages to AWS s3"

  runtime = "python3.8"

  environment = {
    variables = {
      S3_BUCKET = aws_s3_bucket.dead_letters.bucket
    }
  }

  policy = {
    json = data.aws_iam_policy_document.lambda_dlq_to_s3.json
  }

  tags = var.tags
}

data "aws_iam_policy_document" "lambda_dlq_to_s3" {
  statement {
    sid = "ConsumeSQSDLQ"

    actions = [
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:ReceiveMessage",
    ]

    resources = [
      aws_sqs_queue.dead_letter.arn,
    ]
  }

  statement {
    sid = "WriteToS3"

    actions = [
      "s3:PutObject",
    ]

    resources = [
      "${aws_s3_bucket.dead_letters.arn}/*",
    ]
  }

  statement {
    sid = "UseKMSKey"

    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey*",
    ]

    resources = [
      var.kms_key_arn,
    ]
  }
}

resource "aws_lambda_event_source_mapping" "dlq_to_s3" {
  event_source_arn = aws_sqs_queue.dead_letter.arn
  function_name    = module.lambda_dlq_to_s3.function_name
}
