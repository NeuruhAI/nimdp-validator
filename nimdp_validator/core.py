import re
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime, timezone
from .models import NimdpConfig, ValidationResult, PhaseResult, TokenResult, Remediation, PhaseDef

def read_file_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return re.sub(r'\s+', ' ', text).strip()

def find_any_keywords(text: str, keywords: List[str]) -> bool:
    t = text.lower()
    return any(kw.lower() in t for kw in keywords)

def score_phase(text: str, phase_name: str, phase_def: PhaseDef) -> Tuple[float, Dict[str, TokenResult], List[Remediation], bool]:
    phase_weight = phase_def.weight
    hard_block_triggered = False
    token_results = {}
    remediations = []
    achieved = 0.0
    total = 0.0
    
    for token_key, token_def in phase_def.tokens.items():
        t_weight = token_def.weight
        total += t_weight
        hit = find_any_keywords(text, token_def.keywords_any)
        
        token_results[token_key] = TokenResult(
            desc=token_def.desc,
            weight=t_weight,
            present=hit,
            hard_blocker=token_def.hard_blocker
        )
        
        if hit:
            achieved += t_weight
        else:
            remediations.append(Remediation(
                token=f"{phase_name}.{token_key}",
                issue=f"Missing evidence for {token_key}",
                fix=token_def.remediation
            ))
            if token_def.hard_blocker:
                hard_block_triggered = True
                
    phase_score = (achieved / total) * phase_weight if total > 0 else 0.0
    return phase_score, token_results, remediations, hard_block_triggered

def aggregate_scores(texts: List[str], config: NimdpConfig) -> ValidationResult:
    joined = " ".join(texts)
    results = {}
    total_score = 0.0
    all_remediations = []
    any_hard_block = False
    
    for pname, pdef in config.phases.items():
        pscore, tokens, fixes, hb = score_phase(joined, pname, pdef)
        results[pname] = PhaseResult(score_contrib=pscore, tokens=tokens)
        total_score += pscore
        if hb:
            any_hard_block = True
        all_remediations.extend(fixes)
        
    final_score = round(total_score, 4)
    
    status = "NOT READY"
    if any_hard_block and config.hard_block_on_fail:
        status = "BLOCKED"
    elif final_score >= config.pass_threshold:
        status = "MARKET READY"
        
    return ValidationResult(
        score=final_score,
        status=status,
        hard_block_triggered=any_hard_block,
        phases=results,
        remediations=all_remediations,
        threshold=config.pass_threshold,
        hard_block_on_fail=config.hard_block_on_fail,
        timestamp_utc=datetime.now(timezone.utc).isoformat()
    )
