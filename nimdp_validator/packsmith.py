import os
from pathlib import Path
import yaml
import json
from typing import Dict, Any
from openai import OpenAI
from rich.console import Console

console = Console()

def reverse_engineer_with_ai(input_text: str) -> Dict[str, Any]:
    """
    Uses OpenAI to extract NIMDP tokens from a successful specification/document.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    prompt = f"""
    You are an expert in the Neuruh Integrated Market Domination Protocol (NIMDP). 
    I will provide you with a successful business specification, launch plan, or proposal.
    Your task is to reverse-engineer it into a NIMDP Token Map (YAML format).
    
    NIMDP Token Map Structure:
    - phases:
        PHASE_NAME:
            weight: float (total weights across phases must sum to 1.0)
            tokens:
                TOKEN_KEY:
                    desc: string
                    weight: float (weights within a phase must sum to 1.0)
                    keywords_any: [list of strings to search for]
                    remediation: string (how to fix if missing)
                    hard_blocker: boolean (optional)
    
    Extract the core "winning" patterns from this document as tokens.
    
    DOCUMENT CONTENT:
    {input_text}
    
    Return ONLY valid YAML.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {{"role": "system", "content": "You are a NIMDP architect. Output ONLY YAML."}},
            {{"role": "user", "content": prompt}}
        ],
        temperature=0.2
    )
    
    yaml_content = response.choices[0].message.content.strip()
    # Remove markdown code blocks if present
    if yaml_content.startswith("```yaml"):
        yaml_content = yaml_content[7:-3].strip()
    elif yaml_content.startswith("```"):
         yaml_content = yaml_content[3:-3].strip()
         
    return yaml.safe_load(yaml_content)

def generate_pack(template_name: str, output_path: Path):
    templates = {
        "saas_preseed": {
            "phases": {
                "PHASE_1_PRODUCT": {
                    "weight": 0.4,
                    "tokens": {
                        "MVP_SCOPE": {"desc": "Clear definition of MVP.", "weight": 0.5, "keywords_any": ["MVP", "minimal", "core features"], "remediation": "Define what is IN and OUT of MVP."},
                        "PROBLEM_SOLUTION": {"desc": "Clear problem statement.", "weight": 0.5, "keywords_any": ["problem", "solution", "pain point"], "remediation": "State the problem clearly."}
                    }
                }
            },
            "pass_threshold": 0.7
        },
        "defense_proposal": {
             "phases": {
                "PHASE_1_COMPLIANCE": {
                    "weight": 0.5,
                    "tokens": {
                        "FAR_CLAUSE": {"desc": "FAR compliance check.", "weight": 1.0, "keywords_any": ["FAR", "DFARS", "compliance"], "remediation": "Cite relevant FAR clauses."}
                    }
                }
            },
            "pass_threshold": 0.9
        }
    }
    
    content = templates.get(template_name)
    if not content:
        raise ValueError(f"Unknown template: {template_name}. Available: {list(templates.keys())}")
        
    with output_path.open("w", encoding="utf-8") as f:
        yaml.dump(content, f, sort_keys=False)
    console.print(f"[bold green]Generated pack '{template_name}' at {output_path}[/bold green]")

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Packsmith: Generate and Reverse Engineer NIMDP Packs")
    subparsers = parser.add_subparsers(dest="command")
    
    # Template command
    t_parser = subparsers.add_parser("template", help="Generate from template")
    t_parser.add_argument("name", help="Template name")
    t_parser.add_argument("output", help="Output YAML path")
    
    # Reverse command
    r_parser = subparsers.add_parser("reverse", help="Reverse engineer from document via AI")
    r_parser.add_argument("input", help="Input document path")
    r_parser.add_argument("output", help="Output YAML path")
    
    args = parser.parse_args()
    
    if args.command == "template":
        generate_pack(args.name, Path(args.output))
    elif args.command == "reverse":
        if not os.environ.get("OPENAI_API_KEY"):
            console.print("[bold red]ERROR:[/bold red] OPENAI_API_KEY environment variable not set.")
            sys.exit(1)
            
        input_path = Path(args.input)
        if not input_path.exists():
            console.print(f"[bold red]ERROR:[/bold red] Input file not found: {input_path}")
            sys.exit(1)
            
        with console.status("[bold blue]AI is reverse-engineering the winning spec...") as status:
            text = input_path.read_text(encoding="utf-8", errors="ignore")
            pack_data = reverse_engineer_with_ai(text)
            
            with Path(args.output).open("w", encoding="utf-8") as f:
                yaml.dump(pack_data, f, sort_keys=False)
                
        console.print(f"[bold green]Successfully reverse-engineered NIMDP pack to {args.output}[/bold green]")
    else:
        parser.print_help()
