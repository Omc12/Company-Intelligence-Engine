from pydantic import BaseModel, Field
from schema import CompanyIntelligence

class CompanyFeatures(BaseModel):
    strength_count: int
    weakness_count: int
    risk_factor_count: int
    competitive_advantage_count: int
    outlook_encoded: int
    risk_score: float = Field(ge = 0, le = 100)

def compute_features(intel: CompanyIntelligence) -> CompanyFeatures:
    strength_count = len(intel.strengths)
    weakness_count = len(intel.weaknesses)
    risk_factor_count = len(intel.risk_factors)
    competitive_advantage_count = len(intel.competitive_advantage)

    outlook_map = {
        "positive": 1,
        "neutral": 0,
        "negative": -1
    }

    outlook_encoded = outlook_map[intel.outlook.value]

    raw_score = (
        50
        + 8 * risk_factor_count
        + 5 * weakness_count
        - 3 * strength_count
        - 5 * competitive_advantage_count
        - 6 * outlook_encoded
    )

    risk_score = max(0, min(100, raw_score))

    return CompanyFeatures (
        strength_count=strength_count,
        weakness_count=weakness_count,
        risk_factor_count=risk_factor_count,
        competitive_advantage_count=competitive_advantage_count,
        outlook_encoded=outlook_encoded,
        risk_score=risk_score  
    )