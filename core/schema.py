from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Outlook(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class RiskIntelligence(BaseModel):

    risk_factors: List[str] = Field(min_items=1)
    outlook: Outlook
    confidence: float


class BusinessIntelligence(BaseModel):

    strengths: List[str] = Field(min_items=1)
    weaknesses: List[str] = Field(min_items=1)
    competitive_advantage: List[str] = Field(min_items=1)
    confidence: float


class CompanyIntelligence(BaseModel):

    summary: str
    strengths: List[str]
    weaknesses: List[str]
    competitive_advantage: List[str]
    risk_factors: List[str]
    outlook: Outlook
    confidence: float