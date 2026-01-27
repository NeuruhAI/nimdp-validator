import yaml
from pathlib import Path
from .models import NimdpConfig

DEFAULT_CONFIG = {
    "phases": {
        "PHASE_1_PRODUCT": {
            "weight": 0.30,
            "tokens": {
                "TARGET_LOCK": {
                    "desc": "Buyer segment clarity (narrow ICP).",
                    "weight": 0.35,
                    "keywords_any": ["ICP", "ideal customer", "buyer segment", "niche", "target market"],
                    "hard_blocker": True,
                    "remediation": "Define a narrow ICP with firmographics, pain, urgency, and budget. Add it to the spec under Product."
                },
                "VALUE_EQUATION": {
                    "desc": "Value equation maximized: Dream Outcome × Likelihood / (Time × Effort).",
                    "weight": 0.25,
                    "keywords_any": ["Dream Outcome", "Likelihood of Achievement", "time delay", "effort", "sacrifice", "value equation"],
                    "hard_blocker": False,
                    "remediation": "Explicitly state Dream Outcome, proof mechanisms, time-to-value, and effort reduction strategies."
                },
                "RISK_REVERSAL": {
                    "desc": "Guarantees, warranties, or risk-shifting bonuses.",
                    "weight": 0.20,
                    "keywords_any": ["guarantee", "warranty", "risk reversal", "money-back", "free extension"],
                    "hard_blocker": False,
                    "remediation": "Add a guarantee or performance warranty with clear terms; include bonuses that reduce perceived risk."
                },
                "OFFER_FRAME": {
                    "desc": "Transformation-first framing vs feature list.",
                    "weight": 0.20,
                    "keywords_any": ["transformation", "outcome", "before/after", "result", "case study"],
                    "hard_blocker": False,
                    "remediation": "Rewrite offer copy to headline the transformation and outcomes; demote features to supporting role."
                }
            }
        },
        "PHASE_2_MARKETING": {
            "weight": 0.25,
            "tokens": {
                "BEACHHEAD": {
                    "desc": "Single must-win segment selected before going wide.",
                    "weight": 0.35,
                    "keywords_any": ["beachhead", "first pin", "primary segment", "must-win niche"],
                    "hard_blocker": True,
                    "remediation": "Pick one high-urgency segment and state it clearly. Defer all others to the Bowling Alley plan."
                },
                "WHOLE_PRODUCT": {
                    "desc": "Complete solution incl. services/integrations for pragmatists.",
                    "weight": 0.25,
                    "keywords_any": ["whole product", "integration", "add-on", "implementation", "support", "SLA", "compliance"],
                    "hard_blocker": False,
                    "remediation": "List the complete bundle: integrations, onboarding, training, SLAs, compliance artifacts."
                },
                "PRAGMATIST_TRANSLATION": {
                    "desc": "Messaging that de-risks innovation for mainstream buyers.",
                    "weight": 0.20,
                    "keywords_any": ["pragmatist", "proof", "case studies", "reference customers", "ROI evidence"],
                    "hard_blocker": False,
                    "remediation": "Add proof assets: case studies, references, ROI calculators, implementation timelines."
                },
                "BOWLING_ALLEY": {
                    "desc": "Sequenced adjacent niches after beachhead.",
                    "weight": 0.20,
                    "keywords_any": ["bowling alley", "adjacent segments", "expansion sequence", "next segments"],
                    "hard_blocker": False,
                    "remediation": "Map a 3–4 segment expansion plan with entry criteria and readiness checkpoints."
                }
            }
        },
        "PHASE_3_SALES": {
            "weight": 0.20,
            "tokens": {
                "DREAM_100": {
                    "desc": "Top 100 accounts identified with named cadence.",
                    "weight": 0.35,
                    "keywords_any": ["Dream 100", "top 100", "account list", "account-based", "ABM"],
                    "hard_blocker": True,
                    "remediation": "Publish the named Dream 100 list in the spec; define cadence by channel and owner."
                },
                "EDUCATE": {
                    "desc": "Education-first assets for authority building.",
                    "weight": 0.25,
                    "keywords_any": ["webinar", "whitepaper", "playbook", "workshop", "education-based"],
                    "hard_blocker": False,
                    "remediation": "Add 1-2 education assets (e.g., webinar series, ‘State of X’ brief) with titles and deadlines."
                },
                "FOLLOW_UP": {
                    "desc": "7+ touches in a multi-channel sequence.",
                    "weight": 0.20,
                    "keywords_any": ["follow-up", "multi-touch", "sequence", "cadence", "8 touches", "7 touches"],
                    "hard_blocker": False,
                    "remediation": "Document an 8-touch sequence with timing, channel stack, and disqualification criteria."
                },
                "DATA_HOOK": {
                    "desc": "Stat-driven opening and ROI proof.",
                    "weight": 0.20,
                    "keywords_any": ["data shows", "percent", "%", "study", "benchmark", "ROI"],
                    "hard_blocker": False,
                    "remediation": "Insert 2–3 credible stats that frame urgency; cite source and weave into openers."
                }
            }
        },
        "PHASE_4_OPERATIONS": {
            "weight": 0.20,
            "tokens": {
                "VISION_LOCK": {
                    "desc": "EOS 8Q vision completed and shared.",
                    "weight": 0.25,
                    "keywords_any": ["8 questions", "EOS", "vision", "core focus", "10-year target", "marketing strategy", "3-year picture", "1-year plan"],
                    "hard_blocker": False,
                    "remediation": "Attach the completed EOS Vision/Traction Organizer (all 8 questions) to the spec."
                },
                "RIGHT_PEOPLE": {
                    "desc": "GWC: Gets it, Wants it, Capacity per seat.",
                    "weight": 0.20,
                    "keywords_any": ["GWC", "Gets it", "Wants it", "Capacity", "right people right seats"],
                    "hard_blocker": False,
                    "remediation": "List each role with GWC status; move or hire to close gaps."
                },
                "DATA_TRACK": {
                    "desc": "5–15 weekly KPIs live.",
                    "weight": 0.20,
                    "keywords_any": ["KPI", "scorecard", "dashboard", "metrics", "weekly"],
                    "hard_blocker": False,
                    "remediation": "Publish a weekly scorecard with 5–15 metrics, owners, and targets."
                },
                "IDS": {
                    "desc": "Level-10 cadence with IDS (Identify, Discuss, Solve).",
                    "weight": 0.15,
                    "keywords_any": ["Level 10", "L10", "IDS", "weekly meeting", "issues list"],
                    "hard_blocker": False,
                    "remediation": "Schedule a weekly L10 with a living issues list and documented IDS outcomes."
                },
                "PROCESS_CORE": {
                    "desc": "20% SOPs that drive 80% of results documented.",
                    "weight": 0.10,
                    "keywords_any": ["SOP", "standard operating", "process map", "playbook"],
                    "hard_blocker": False,
                    "remediation": "Document the top 20% SOPs by throughput; store links in the spec."
                },
                "ROCKS": {
                    "desc": "3–7 quarterly Rocks with owners.",
                    "weight": 0.10,
                    "keywords_any": ["Rocks", "quarterly priorities", "OKR", "90-day"],
                    "hard_blocker": False,
                    "remediation": "List 3–7 Rocks with owners, deadlines, and definitions of done."
                }
            }
        },
        "QA_RECURSION": {
            "weight": 0.05,
            "tokens": {
                "INTEGRATION_CHECK": {
                    "desc": "Cross-phase alignment confirmed pre-launch.",
                    "weight": 0.5,
                    "keywords_any": ["integration check", "cross-phase", "market ready", "go/no-go"],
                    "hard_blocker": False,
                    "remediation": "Add a formal, named Integration Check section with a go/no-go gate."
                },
                "FEEDBACK_LOOP": {
                    "desc": "30/60/90 (or similar) learning loop locked.",
                    "weight": 0.5,
                    "keywords_any": ["feedback loop", "post-launch", "retro", "30/60/90", "iteration"],
                    "hard_blocker": False,
                    "remediation": "Schedule post-launch retros at 30/60/90 with owners and improvement backlog."
                }
            }
        }
    },
    "pass_threshold": 0.80,
    "hard_block_on_fail": True
}

def load_config(external_yaml: Path = None) -> NimdpConfig:
    data = DEFAULT_CONFIG
    if external_yaml and external_yaml.exists():
        with external_yaml.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    
    return NimdpConfig(**data)
