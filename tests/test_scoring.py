from nimdp_validator.core import find_any_keywords, score_phase
from nimdp_validator.models import PhaseDef, TokenDef

def test_find_keywords():
    assert find_any_keywords("This is a Niche product", ["niche"]) is True
    assert find_any_keywords("Nothing here", ["niche"]) is False
    assert find_any_keywords("CASE STUDY included", ["case study"]) is True

def test_score_phase_perfect():
    pdef = PhaseDef(
        weight=1.0,
        tokens={
            "T1": TokenDef(desc="d1", weight=0.5, keywords_any=["k1"], remediation="r1"),
            "T2": TokenDef(desc="d2", weight=0.5, keywords_any=["k2"], remediation="r2")
        }
    )
    score, results, remed, hb = score_phase("k1 k2", "Phase1", pdef)
    assert score == 1.0
    assert len(remed) == 0
    assert hb is False

def test_score_phase_partial():
    pdef = PhaseDef(
        weight=1.0,
        tokens={
            "T1": TokenDef(desc="d1", weight=0.5, keywords_any=["k1"], remediation="r1"),
            "T2": TokenDef(desc="d2", weight=0.5, keywords_any=["k2"], remediation="r2")
        }
    )
    score, results, remed, hb = score_phase("k1 only", "Phase1", pdef)
    assert score == 0.5
    assert len(remed) == 1
    assert remed[0].token == "Phase1.T2"
    assert hb is False

def test_hard_blocker():
    pdef = PhaseDef(
        weight=1.0,
        tokens={
            "T1": TokenDef(desc="d1", weight=0.5, keywords_any=["k1"], remediation="r1", hard_blocker=True),
        }
    )
    score, results, remed, hb = score_phase("missing", "Phase1", pdef)
    assert score == 0.0
    assert hb is True
    assert len(remed) == 1
