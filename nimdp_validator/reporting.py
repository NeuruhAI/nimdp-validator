import json
from pathlib import Path
from typing import Tuple
import re
from datetime import datetime, timezone
from .models import ValidationResult

def sanitize_title(s: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]+', '_', s).strip('_')

def build_markdown_report(project_name: str, result: ValidationResult) -> str:
    lines = []
    lines.append(f"# NIMDP Validation Report — {project_name}")
    lines.append(f"- Generated (UTC): {result.timestamp_utc}")
    lines.append(f"- Score: **{round(result.score * 100, 2)}%**")
    lines.append(f"- Status: **{result.status}**\n")
    lines.append("---\n")
    
    for pname, pobj in result.phases.items():
        lines.append(f"## {pname}")
        lines.append(f"- Score Contribution: {round(pobj.score_contrib * 100, 2)}%\n")
        lines.append("| Token | Present | Hard Blocker | Weight |")
        lines.append("|---|---:|---:|---:|")
        for tname, tobj in pobj.tokens.items():
            lines.append(f"| {tname} | {'YES' if tobj.present else 'NO'} | {'YES' if tobj.hard_blocker else 'NO'} | {tobj.weight} |")
        lines.append("")
        
    if result.remediations:
        lines.append("## Remediation Plan")
        for r in result.remediations:
            lines.append(f"- **{r.token}**: {r.issue}. Fix: {r.fix}")
            
    return "\n".join(lines)

def write_reports(project_name: str, outdir: Path, result: ValidationResult) -> Tuple[Path, Path]:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    base = f"{ts}__{sanitize_title(project_name)}"
    json_path = outdir / f"{base}.json"
    md_path = outdir / f"{base}.md"
    
    outdir.mkdir(parents=True, exist_ok=True)
    
    # Dump Pydantic model to JSON
    with json_path.open("w", encoding="utf-8") as f:
        f.write(result.model_dump_json(indent=2))
        
    md = build_markdown_report(project_name, result)
    with md_path.open("w", encoding="utf-8") as f:
        f.write(md)
        
    return json_path, md_path
