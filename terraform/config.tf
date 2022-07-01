terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }

  backend "s3" {
    bucket = "jd-terraform"
    key    = "birdle"
    region = "us-west-2"

    workspace_key_prefix = "workspace"
  }
}

provider "aws" {
  region = "us-west-2"

  default_tags {
    tags = {
      terraform = "true"
    }
  }
}