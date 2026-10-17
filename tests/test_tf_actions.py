"""Testes unitarios do iac-terraform-github-actions.

Valida a estrutura do HCL, o workflow de CI e o comportamento de
plano/idempotencia simulado, sem depender do binario do Terraform.
"""

from __future__ import annotations

from pathlib import Path

from iac_actions.plan import ResourceBlock, apply_plan, extract_blocks, has_block, read_hcl, render_plan

ROOT = Path(__file__).resolve().parents[1]
MAIN_TF = ROOT / "main.tf"
CI_YML = ROOT / ".github" / "workflows" / "ci.yml"


def test_main_tf_has_terraform_block() -> None:
    text = read_hcl(MAIN_TF)
    assert has_block(text, "terraform")
    assert has_block(text, "required_version")


def test_main_tf_has_variables() -> None:
    text = read_hcl(MAIN_TF)
    assert has_block(text, 'variable "environment"')
    assert has_block(text, 'variable "prefix"')


def test_main_tf_has_local_file_resource() -> None:
    text = read_hcl(MAIN_TF)
    assert has_block(text, 'resource "local_file"')


def test_main_tf_has_outputs() -> None:
    text = read_hcl(MAIN_TF)
    assert has_block(text, "output")


def test_no_hardcoded_aws_credentials() -> None:
    text = read_hcl(MAIN_TF).lower()
    for secret in ("access_key", "secret_key", "secret_id", "aws_secret", "aws_access"):
        assert secret not in text


def test_extract_blocks_parses_local_file() -> None:
    blocks = extract_blocks(read_hcl(MAIN_TF))
    assert any(b.kind == "local_file" and b.name == "manifest" for b in blocks)


def test_ci_yml_has_init_validate_plan() -> None:
    text = CI_YML.read_text(encoding="utf-8")
    for step in ("terraform init", "terraform validate", "terraform plan"):
        assert step in text


def test_plan_is_deterministic() -> None:
    blocks = extract_blocks(read_hcl(MAIN_TF))
    assert render_plan(blocks, "dev") == render_plan(blocks, "dev")


def test_plan_is_idempotent_same_input_same_output() -> None:
    blocks = extract_blocks(read_hcl(MAIN_TF))
    plan_a = render_plan(blocks, "homolog")
    plan_b = render_plan(blocks, "homolog")
    assert plan_a == plan_b


def test_apply_is_idempotent_no_duplicates() -> None:
    blocks = extract_blocks(read_hcl(MAIN_TF))
    plan = render_plan(blocks, "dev")
    state: set[str] = set()
    first = apply_plan(state, plan)
    second = apply_plan(first, plan)
    assert first == second
    assert len(first) == len(blocks)
