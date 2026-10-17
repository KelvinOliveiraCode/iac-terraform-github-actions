# iac-terraform-github-actions
# MVP: IaC com Terraform + GitHub Actions (plan/diff/apply, idempotencia).
# Sem credenciais embutidas. Usa local_file (provedor built-in, sem credenciais AWS).

terraform {
  required_version = ">= 1.5.0, < 2.0.0"
}

variable "environment" {
  description = "Nome do ambiente de destino (dev, homolog, prod)"
  type        = string
  default     = "dev"
}

variable "prefix" {
  description = "Prefixo aplicado aos nomes dos recursos"
  type        = string
  default     = "iac"
}

locals {
  content = <<-EOF
    Ambiente: ${var.environment}
    Prefixo:  ${var.prefix}
    Gerado por: iac-terraform-github-actions
    Idempotente: sim (mesma entrada => mesmo plano)
  EOF
}

resource "local_file" "manifest" {
  content      = local.content
  filename     = "${path.module}/generated/manifest-${var.environment}.txt"
  file_permission = "0644"
}

output "manifest_path" {
  description = "Caminho do manifesto gerado"
  value       = local_file.manifest.filename
}

output "environment" {
  description = "Ambiente configurado"
  value       = var.environment
}
