"""Simulacao deterministica de plano e aplicacao idempotente do Terraform.

Terraform nao esta instalado neste host, entao esses helpers validam a
estrutura do HCL e simulam o comportamento de plan/apply sem chamar o binario.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ResourceBlock:
    """Um bloco `resource "tipo" "nome" {` extraído do HCL."""

    kind: str
    name: str


def read_hcl(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def has_block(text: str, keyword: str) -> bool:
    return any(line.strip().startswith(keyword) for line in text.splitlines())


def extract_blocks(text: str) -> list[ResourceBlock]:
    """Extrai blocos `resource` de uma string HCL (formato simples e determinístico)."""

    blocks: list[ResourceBlock] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not (line.startswith("resource ") or line.startswith('resource "')):
            continue
        parts = line.split('"')
        if len(parts) >= 4:
            blocks.append(ResourceBlock(kind=parts[1], name=parts[3]))
    return blocks


def render_plan(blocks: list[ResourceBlock], environment: str) -> str:
    """Renderiza um plano determinístico a partir dos blocos extraídos."""

    lines = [f"Terraform plan (ambiente={environment})"]
    if not blocks:
        lines.append("  No changes.")
        return "\n".join(lines)
    lines.append("  Planned resources:")
    for block in blocks:
        lines.append(f"    + {block.kind}.{block.name}")
    return "\n".join(lines)


def apply_plan(state: set[str], plan: str) -> set[str]:
    """Aplica o plano de forma idempotente: nao duplica recursos ja presentes."""

    next_state = set(state)
    for line in plan.splitlines():
        if line.startswith("    + "):
            resource = line.split("+ ", 1)[1].strip()
            next_state.add(resource)  # set -> aplicacao idempotente
    return next_state
