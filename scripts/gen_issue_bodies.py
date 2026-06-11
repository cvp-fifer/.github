# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Generate issue-bodies/*.md skeletons from ISSUE_TEMPLATE/*.yml issue forms.

The skeletons carry the exact `### <label>` heading structure GitHub renders
when a form is submitted, so issues filed via `gh issue create --body-file`
and via the web form are structurally identical. `type: markdown` elements are
skipped — GitHub never renders them into the submitted body.

Usage:
    uv run scripts/gen_issue_bodies.py            # regenerate issue-bodies/
    uv run scripts/gen_issue_bodies.py --check    # exit 1 if anything drifted
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FORMS_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
OUT_DIR = ROOT / "issue-bodies"


def one_line(text: str) -> str:
    return " / ".join(part.strip() for part in text.strip().splitlines() if part.strip())


def guidance(attrs: dict, required: bool) -> str:
    parts = ["(required)" if required else "(optional)"]
    if desc := attrs.get("description"):
        parts.append(one_line(desc))
    if placeholder := attrs.get("placeholder"):
        parts.append(f"e.g. {one_line(placeholder)}" if attrs.get("description") else one_line(placeholder))
    return f"<!-- {' '.join(parts)} -->"


def render(form: dict, src_rel: str) -> str:
    lines = [
        f"<!-- GENERATED from {src_rel} by scripts/gen_issue_bodies.py — do not edit.",
        "     Regenerate: uv run scripts/gen_issue_bodies.py -->",
    ]
    label_args = " ".join(f"-l {label}" for label in form.get("labels") or [])
    hint = f'<!-- gh: gh issue create -R cvp-fifer/<repo> -t "<title>" {label_args} -F <this file>'
    if issue_type := form.get("type"):
        hint += f' — issue type "{issue_type}" is applied by the web form only; set it via web/API if needed'
    lines.append(hint + " -->")

    for element in form.get("body", []):
        etype = element.get("type")
        if etype == "markdown":
            continue
        attrs = element.get("attributes", {})
        required = bool(element.get("validations", {}).get("required"))
        lines += ["", f"### {attrs.get('label', '').strip()}", ""]
        if etype == "dropdown":
            options = " | ".join(attrs.get("options", []))
            tag = "(required)" if required else "(optional)"
            lines.append(f"<!-- {tag} pick exactly one: {options} -->")
        elif etype == "checkboxes":
            lines += [f"- [ ] {opt.get('label', '')}" for opt in attrs.get("options", [])]
        else:  # input / textarea
            lines.append(guidance(attrs, required))
            if value := attrs.get("value"):
                lines.append(value.rstrip("\n"))
    return "\n".join(lines) + "\n"


def main() -> int:
    check = "--check" in sys.argv[1:]
    sources = sorted(path for path in FORMS_DIR.glob("*.yml") if path.name != "config.yml")
    if not sources:
        print(f"no issue forms found in {FORMS_DIR}", file=sys.stderr)
        return 1

    drifted: list[str] = []
    OUT_DIR.mkdir(exist_ok=True)
    for src in sources:
        form = yaml.safe_load(src.read_text(encoding="utf-8"))
        out = OUT_DIR / f"{re.sub(r'^[0-9]+-', '', src.stem)}.md"
        content = render(form, str(src.relative_to(ROOT)))
        if check:
            if not out.exists() or out.read_text(encoding="utf-8") != content:
                drifted.append(str(out.relative_to(ROOT)))
        else:
            out.write_text(content, encoding="utf-8")
            print(f"wrote {out.relative_to(ROOT)}")

    if drifted:
        print(f"drifted from ISSUE_TEMPLATE/: {', '.join(drifted)}", file=sys.stderr)
        print("regenerate: uv run scripts/gen_issue_bodies.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
