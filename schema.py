from pydantic import BaseModel, Field
from enum import Enum
from typing import List


class Outlook(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class CompanyIntelligence(BaseModel):
    summary: str = Field(
        ...,
        description="Concise summary of the company analysis (max 3 sentences)."
    )

    strengths: List[str] = Field(
        ...,
        max_length=5,
        description="List of key strengths (maximum 5)."
    )

    weaknesses: List[str] = Field(
        ...,
        max_length=5,
        description="List of key weaknesses (maximum 5)."
    )

    competitive_advantage: List[str] = Field(
        ...,
        max_length=5,
        description="List of structural competitive advantages (maximum 5)."
    )

    risk_factors: List[str] = Field(
        ...,
        max_length=5,
        description="List of key risk factors (maximum 5)."
    )

    outlook: Outlook = Field(
        ...,
        description="Overall forward-looking classification."
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Model confidence between 0 and 1."
    )
