module "lambda_dynamo_inserter" {
  source = "github.com/claranet/terraform-aws-lambda?ref=v1.2.0"

  function_name = "${var.app_name}-dynamo-inserter"
  handler       = "lambda_handler.lambda_handler"

  source_path = abspath("${path.module}/../lambdas/dynamo_inserter")
  description = "Deliver timestamps into dynamo"

  runtime = "python3.8"

  environment = {
    variables = {
      DYNAMO_TABLE = aws_dynamodb_table.app.name
    }
  }

  policy = {
    json = data.aws_iam_policy_document.lambda_sqs_to_dynamo.json
  }

  tags = local.tags
}

data "aws_iam_policy_document" "lambda_sqs_to_dynamo" {
  statement {
    sid = "ConsumeSQSQueue"

    actions = [
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:ReceiveMessage",
    ]

    resources = [
      module.app_queues.queue_arn
    ]
  }

  statement {
    sid = "WriteToDynamo"

    actions = [
      "dynamodb:PutItem",
      "dynamodb:BatchWriteItem",
    ]

    resources = [
      aws_dynamodb_table.app.arn
    ]
  }

  statement {
    sid = "UseKMSKey"

    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey*",
    ]

    resources = [
      aws_kms_key.app.arn
    ]
  }
}

resource "aws_lambda_event_source_mapping" "sqs_to_dynamo" {
  event_source_arn = module.app_queues.queue_arn
  function_name    = module.lambda_dynamo_inserter.function_name
}
