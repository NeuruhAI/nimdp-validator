import os
import requests
from typing import Dict, Any
from datetime import datetime, timezone
from .models import ValidationResult

def push_to_notion(project_name: str, result: ValidationResult) -> Dict[str, Any]:
    api_key = os.environ.get("NOTION_API_KEY")
    database_id = os.environ.get("NOTION_DATABASE_ID")
    
    if not api_key or not database_id:
        return {"ok": False, "error": "NOTION_API_KEY or NOTION_DATABASE_ID missing from environment"}
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    score_pct = round(result.score * 100, 2)
    summary = f"{project_name} — {result.status} — {score_pct}%\n"
    
    if result.remediations:
        summary += "\nTop Remediations:\n"
        for r in result.remediations[:10]:
            summary += f"- {r.token}: {r.fix}\n"
            
    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {"title": [{"type": "text", "text": {"content": project_name}}]},
            "Status": {"select": {"name": result.status}},
            "Score": {"number": float(score_pct)},
            "Timestamp (UTC)": {"date": {"start": datetime.now(timezone.utc).isoformat()}}
        },
        "children": [{
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": summary}}]}
        }]
    }
    
    try:
        resp = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload, timeout=10)
        if 200 <= resp.status_code < 300:
            return {"ok": True, "page_id": resp.json().get("id")}
        return {"ok": False, "error": f"HTTP {resp.status_code}: {resp.text}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
