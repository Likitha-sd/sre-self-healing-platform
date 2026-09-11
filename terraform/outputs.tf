output "project_file" {
  description = "Path of the Terraform-managed project file"
  value       = local_file.project_info.filename
}
