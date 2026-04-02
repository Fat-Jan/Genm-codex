#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_MATRIX_PATH = REPO_ROOT / "shared" / "templates" / "host-capability-matrix-v1.json"
MATRIX_OVERRIDE_ENV = "GENM_HOST_CAPABILITY_MATRIX_FILE"
HOST_DISPLAY_NAMES = {
    "claude": "Claude Code",
    "codex": "Codex",
    "opencode": "OpenCode",
    "openclaw": "OpenCLAW",
    "trae": "Trae",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render host capability projection from the current host matrix.")
    parser.add_argument(
        "--format",
        choices=["json", "install-table", "support-table", "support-details"],
        default="json",
    )
    return parser.parse_args()


def get_matrix_path(*, allow_env_override: bool = True) -> Path:
    raw_path = os.environ.get(MATRIX_OVERRIDE_ENV) if allow_env_override else None
    return Path(raw_path) if raw_path else DEFAULT_MATRIX_PATH


def read_matrix(
    *,
    matrix_path: Path | None = None,
    allow_env_override: bool = True,
) -> dict[str, Any]:
    path = matrix_path or get_matrix_path(allow_env_override=allow_env_override)
    return json.loads(path.read_text(encoding="utf-8"))


def build_projection(
    *,
    matrix_path: Path | None = None,
    allow_env_override: bool = True,
) -> dict[str, Any]:
    payload = read_matrix(
        matrix_path=matrix_path,
        allow_env_override=allow_env_override,
    )
    hosts: list[dict[str, Any]] = []
    for host_id, row in payload["hosts"].items():
        install_command = None
        if row["install_mode"] != "unsupported":
            install_command = "bash scripts/install-skills.sh"
            if host_id != "codex":
                install_command = f"bash scripts/install-skills.sh {host_id}"
        hosts.append(
            {
                "host_id": host_id,
                "display_name": HOST_DISPLAY_NAMES.get(host_id, host_id),
                "status": row["status"],
                "verification_level": row["verification_level"],
                "install_mode": row["install_mode"],
                "skill_install_root": row["skill_install_root"],
                "install_command": install_command,
                "supports_skill_discovery": row["supports_skill_discovery"],
                "supports_alias": row["supports_alias"],
                "supports_rules_context": row["supports_rules_context"],
                "supports_hooks": row["supports_hooks"],
                "supports_mcp": row["supports_mcp"],
                "supports_native_invocation": row["supports_native_invocation"],
                "degrade_policy": row["degrade_policy"],
                "notes": row["notes"],
                "evidence": row["evidence"],
            }
        )
    return {
        "version": payload.get("version", "1.0"),
        "hosts": hosts,
    }


def render_install_table(projection: dict[str, Any]) -> str:
    lines = [
        "| 平台 | 安装命令 | skill 路径 |",
        "|------|---------|----------|",
    ]
    for host in projection["hosts"]:
        if host["install_mode"] == "unsupported":
            continue
        lines.append(
            f"| {host['display_name']} | `{host['install_command']}` | `{host['skill_install_root']}` |"
        )
    lines.append("| 全平台 | `bash scripts/install-skills.sh --all` | 以上全部支持宿主 |")
    return "\n".join(lines)


def render_support_table(projection: dict[str, Any]) -> str:
    lines = [
        "| 平台 | 状态 | 验证等级 | 安装支持 |",
        "|------|------|----------|----------|",
    ]
    for host in projection["hosts"]:
        lines.append(
            f"| {host['display_name']} | {host['status']} | {host['verification_level']} | {host['install_mode']} |"
        )
    return "\n".join(lines)


def render_support_details(projection: dict[str, Any]) -> str:
    sections: list[str] = []
    for host in projection["hosts"]:
        sections.append(f"### {host['display_name']}")
        sections.append(f"- 状态：`{host['status']}`")
        sections.append(f"- 验证等级：`{host['verification_level']}`")
        if host["install_mode"] == "unsupported":
            sections.append("- 安装支持：`unsupported`")
        else:
            sections.append(
                f"- 安装支持：`{host['install_mode']}` -> `{host['skill_install_root']}`"
            )
            sections.append(f"- 安装命令：`{host['install_command']}`")
        sections.append("- 能力边界：")
        sections.append(
            f"  - `skill_discovery`: `{host['supports_skill_discovery']}`"
        )
        sections.append(f"  - `alias`: `{host['supports_alias']}`")
        sections.append(
            f"  - `rules_context`: `{host['supports_rules_context']}`"
        )
        sections.append(f"  - `hooks`: `{host['supports_hooks']}`")
        sections.append(f"  - `mcp`: `{host['supports_mcp']}`")
        sections.append(
            f"  - `native_invocation`: `{host['supports_native_invocation']}`"
        )
        sections.append(f"- 退化策略：{host['degrade_policy']}")
        sections.append(f"- 备注：{host['notes']}")
        sections.append("- 证据：")
        for evidence in host["evidence"]:
            sections.append(
                f"  - `{evidence['kind']}` `{evidence['ref']}`: {evidence['summary']}"
            )
        sections.append("")
    return "\n".join(sections).strip()


def main() -> None:
    args = parse_args()
    projection = build_projection()
    if args.format == "install-table":
        print(render_install_table(projection))
        return
    if args.format == "support-table":
        print(render_support_table(projection))
        return
    if args.format == "support-details":
        print(render_support_details(projection))
        return
    print(json.dumps(projection, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
