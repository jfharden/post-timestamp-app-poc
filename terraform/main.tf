terraform {
  required_version = "~> 0.12"

  required_providers {
    aws      = "~> 2.70"
    external = "~>1.2"
    null     = "~>2.1"
  }
}

provider "aws" {
  region = var.aws_region
}

locals {
  tags = {
    "${var.resource_group_tag_name}" = var.app_name
    Environment                      = var.environment
  }
}

resource "aws_resourcegroups_group" "app" {
  name        = var.app_name
  description = "Resources which are part of the ${var.app_name} deployment"

  resource_query {
    query = jsonencode({
      ResourceTypeFilters = ["AWS::AllSupported"],
      TagFilters = [
        {
          Key    = "${var.resource_group_tag_name}",
          Values = ["${var.app_name}"],
        },
      ],
    })
  }

  tags = local.tags
}

resource "aws_kms_key" "app" {
  description = "Key for encryption of all resources in ${var.app_name}"
  tags        = local.tags
}
