import sys
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.markdown import Markdown
from .config import load_config
from .core import read_file_text, aggregate_scores
from .reporting import write_reports
from .notion import push_to_notion

console = Console()

def parse_args():
    p = argparse.ArgumentParser(description="Validate specs against the NIMDP market domination standard.")
    p.add_argument("--project-name", required=True, help="Project name")
    p.add_argument("--input", nargs="+", required=True, help="One or more spec files (.md/.txt/.json)")
    p.add_argument("--outdir", required=True, help="Output directory for reports")
    p.add_argument("--token-map", default="token_map.yaml", help="Optional external token map (YAML)")
    p.add_argument("--push-notion", action="store_true", help="Push results to Notion")
    p.add_argument("--threshold", type=float, default=None, help="Override pass threshold (0..1)")
    p.add_argument("--no_hard_block", action="store_true", help="Ignore hard blockers (for testing)")
    return p.parse_args()

def main():
    args = parse_args()
    
    console.print(Panel(f"[bold cyan]NIMDP Validator[/bold cyan] - Checking: [bold]{args.project_name}[/bold]", expand=False))

    # 1. Load Config
    token_map_path = Path(args.token_map)
    with console.status(f"[bold green]Loading configuration from {token_map_path}...") as status:
        config = load_config(token_map_path)
    
        if args.threshold is not None:
            config.pass_threshold = args.threshold
        if args.no_hard_block:
            config.hard_block_on_fail = False

        # 2. Read Inputs
        texts = []
        for ipath in args.input:
            p = Path(ipath)
            if not p.exists():
                console.print(f"[bold red]ERROR[/bold red] Input file not found: {p}")
                sys.exit(2)
            try:
                t = read_file_text(p)
                if t:
                    texts.append(t)
            except Exception as e:
                console.print(f"[bold red]ERROR[/bold red] Failed reading {p}: {e}")
                sys.exit(2)
                
        if not texts:
            console.print("[bold red]ERROR[/bold red] No readable content from inputs.")
            sys.exit(2)

        # 3. Validate
        status.update("[bold green]Validating content...")
        result = aggregate_scores(texts, config)

    # 4. Report
    outdir = Path(args.outdir)
    jpath, mpath = write_reports(args.project_name, outdir, result)

    # Display Results
    console.print("\n[bold]=== VALIDATION SUMMARY ===[/bold]")
    
    score_style = "green" if result.status == "MARKET READY" else "red"
    console.print(f"Status:  [{score_style} bold]{result.status}[/{score_style} bold]")
    console.print(f"Score:   [bold]{round(result.score * 100, 2)}%[/bold] (threshold {round(result.threshold * 100, 2)}%)")
    
    if result.hard_block_triggered:
         console.print("[bold red]!! HARD BLOCK TRIGGERED !![/bold red]")

    # Phase Breakdown Table
    table = Table(title="Phase Breakdown")
    table.add_column("Phase", style="cyan")
    table.add_column("Score Contribution", style="magenta")
    table.add_column("Status", style="bold")

    for pname, pobj in result.phases.items():
        # Determine simple status for phase based on token hits (just illustrative)
        # Actually, let's just show the score
        table.add_row(
            pname, 
            f"{round(pobj.score_contrib * 100, 2)}%",
            "[green]OK[/green]" if pobj.score_contrib > 0 else "[yellow]Low[/yellow]" 
        )
    console.print(table)
    
    console.print(f"\nReports saved to:\n- {jpath}\n- {mpath}")

    # 5. Optional Notion
    if args.push_notion:
        with console.status("[bold blue]Pushing to Notion...") as status:
            push_res = push_to_notion(args.project_name, result)
            if push_res.get("ok"):
                console.print(f"[green]Notion Page Created:[/green] page_id={push_res.get('page_id')}")
            else:
                console.print(f"[red]Notion Error:[/red] {push_res.get('error')}")

    # 6. Exit Code
    if result.status == "MARKET READY":
        sys.exit(0)
    elif result.status == "NOT READY":
        sys.exit(1)
    else:
        sys.exit(3)

if __name__ == "__main__":
    main()
