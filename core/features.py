def compute_features(intel):

    outlook_map = {
        "positive": 1,
        "neutral": 0,
        "negative": -1
    }

    outlook_encoded = outlook_map[intel.outlook.value]

    risk_score = (
        25
        + 15 * len(intel.risk_factors)
        + 10 * len(intel.weaknesses)
        + 5 * len(intel.strengths)
        + 15 * len(intel.competitive_advantage)
        + 5 * outlook_encoded
    )

    return {
        "strength_count": len(intel.strengths),
        "weakness_count": len(intel.weaknesses),
        "risk_factor_count": len(intel.risk_factors),
        "competitive_advantage_count": len(intel.competitive_advantage),
        "outlook_encoded": outlook_encoded,
        "risk_score": risk_score
    }