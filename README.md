# iac-terraform-github-actions

IaC com Terraform + GitHub Actions (plan/diff/apply, idempotencia).
Infrastructure as Code with Terraform + GitHub Actions (plan/diff/apply, idempotency).

## Sobre o projeto / About

Projeto de infraestrutura como codigo que valida o ciclo plan/diff/apply do
Terraform num fluxo de GitHub Actions, com foco em idempotencia: a mesma
entrada produz sempre o mesmo plano, e aplicar o plano duas vezes nao duplica
recursos.

Nao contem credenciais AWS embutidas. Usa o recurso `local_file` (provedor
built-in do Terraform), entao nao e necessario configurar provedor nem chaves
para rodar `init`, `validate` e `plan` localmente.

Infrastructure as Code project that validates the Terraform plan/diff/apply
cycle in a GitHub Actions workflow, focused on idempotency: the same input
always yields the same plan, and applying the plan twice does not duplicate
resources.

No hardcoded AWS credentials. Uses the `local_file` resource (Terraform
built-in provider), so no provider or keys are needed to run `init`,
`validate`, and `plan` locally.

## Estrutura do repositorio / Project structure

| Caminho | Funcao |
|---|---|
| `main.tf` | Recurso `local_file`, variaveis de ambiente e prefixo, saidas |
| `.github/workflows/ci.yml` | Workflow CI: checkout, setup-terraform, `init`, `validate`, `plan` |
| `pyproject.toml` | Projeto Python, dependencia de teste (`pytest`) |
| `src/iac_actions/plan.py` | Leitura de HCL, render de plano e aplicacao idempotente simulada |
| `tests/test_tf_actions.py` | 10 testes unitarios (estrutura HCL, workflow CI, plano deterministico, aplicacao idempotente) |
| `README.md` | Este arquivo (PT-BR + EN) |
| `BRIEF.md` | Resumo de entregas e como verificar |

## Como usar / How to use

Prerequisito: Terraform >= 1.5.0.

```
terraform init -input=false
terraform validate
terraform plan -input=false
```

Para aplicar de verdade (cria um arquivo local em `generated/`):

```
terraform apply -auto-approve
```

Executar o fluxo no GitHub: abra um PR ou faça push na branch `main`. O
workflow roda `init`, `validate` e `plan` em cada alteracao.

Prerequisite: Terraform >= 1.5.0.

```
terraform init -input=false
terraform validate
terraform plan -input=false
```

To apply for real (creates a local file under `generated/`):

```
terraform apply -auto-approve
```

Run the flow on GitHub: open a PR or push to branch `main`. The workflow
runs `init`, `validate`, and `plan` on every change.

## Testes

Terraform nao esta instalado neste host, entao `terraform validate` nao pode
ser executado. Os testes Python continuam passando e cobrem a validacao do HCL,
do workflow de CI e do comportamento de plano/idempotencia.

```
python -m pytest -q
```

Resultado: 10 aprovados, 0 falhos.

Terraform is not installed on this host, so `terraform validate` cannot run.
The Python tests still pass and cover HCL structure, the CI workflow, and the
plan/idempotency behavior.

```
python -m pytest -q
```

Result: 10 passed, 0 failed.

## Licenca / License

MIT

## Autor / Author

Kelvin Oliveira
