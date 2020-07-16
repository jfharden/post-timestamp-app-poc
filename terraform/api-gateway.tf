resource "aws_api_gateway_rest_api" "app" {
  name        = var.app_name
  description = "JFHarden POC for posting timestamps to dynamo"

  tags = local.tags
}

resource "aws_api_gateway_resource" "app" {
  rest_api_id = aws_api_gateway_rest_api.app.id
  parent_id   = aws_api_gateway_rest_api.app.root_resource_id
  path_part   = "app"
}

resource "aws_api_gateway_method" "app" {
  rest_api_id   = aws_api_gateway_rest_api.app.id
  resource_id   = aws_api_gateway_resource.app.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "app" {
  rest_api_id = aws_api_gateway_rest_api.app.id
  resource_id = aws_api_gateway_method.app.resource_id
  http_method = aws_api_gateway_method.app.http_method

  integration_http_method = aws_api_gateway_method.app.http_method
  type                    = "AWS_PROXY"
  uri                     = module.lambda_sqs_poster.function_invoke_arn
}

resource "aws_api_gateway_deployment" "app" {
  rest_api_id = aws_api_gateway_rest_api.app.id
  stage_name  = var.environment

  depends_on = [
    aws_api_gateway_integration.app,
  ]
}

resource "aws_api_gateway_method_settings" "app" {
  rest_api_id = aws_api_gateway_rest_api.app.id
  stage_name  = aws_api_gateway_deployment.app.stage_name
  method_path = "${aws_api_gateway_resource.app.path_part}/${aws_api_gateway_method.app.http_method}"

  settings {
    metrics_enabled = true
    logging_level   = "OFF"

    throttling_rate_limit  = 100
    throttling_burst_limit = 50
  }
}
