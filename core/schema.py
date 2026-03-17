from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Outlook(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class RiskIntelligence(BaseModel):

    risk_factors: List[str] = Field(description="List of key risk factors identified")
    outlook: Outlook
    confidence: float


class BusinessIntelligence(BaseModel):

    strengths: List[str] = Field(description="List of company strengths")
    weaknesses: List[str] = Field(description="List of company weaknesses")
    competitive_advantage: List[str] = Field(description="List of competitive advantages")
    confidence: float


class CompanyIntelligence(BaseModel):

    summary: str
    strengths: List[str]
    weaknesses: List[str]
    competitive_advantage: List[str]
    risk_factors: List[str]
    outlook: Outlook
    confidence: float