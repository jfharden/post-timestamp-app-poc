output "api_gateway_url" {
  description = "URL of the api gateway endpoint for POSTing to"
  value       = "${aws_api_gateway_deployment.app.invoke_url}${aws_api_gateway_resource.app.path}"
}
