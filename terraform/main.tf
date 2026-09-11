terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

resource "local_file" "project_info" {
  filename = "${path.module}/project-info.txt"
  content  = "${var.project_name} managed by Terraform"
}
