module "lambda_sqs_poster" {
  source = "github.com/claranet/terraform-aws-lambda?ref=v1.2.0"

  function_name = "${var.app_name}-post-app"
  handler       = "lambda_handler.lambda_handler"

  source_path = abspath("${path.module}/../lambdas/api_gateway_to_sqs")
  description = "Send a message to an SQS queue with the current timestamp and request id"

  runtime = "python3.8"

  environment = {
    variables = {
      SQS_QUEUE = module.app_queues.queue_id
    }
  }

  policy = {
    json = data.aws_iam_policy_document.lambda_to_sqs.json
  }

  tags = local.tags
}

data "aws_iam_policy_document" "lambda_to_sqs" {
  statement {
    sid = "WriteToSQSQueue"

    actions = [
      "sqs:SendMessage",
    ]

    resources = [
      module.app_queues.queue_arn
    ]
  }

  statement {
    sid = "UseKMSKey"

    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey",
    ]

    resources = [
      aws_kms_key.app.arn
    ]
  }
}
