from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class CompanyAnalysis(BaseModel):
    """Structured output for LLM company analysis focused on developer tools"""
    pricing_model: str  # Free, Freemium, Paid, Enterprise, Unknown
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    description: str = ""
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []
    # Trend analysis fields
    trend_status: Optional[str] = None  # Rising, Stable, Declining, Hot, Emerging
    popularity_score: Optional[int] = None  # 1-10 scale
    community_activity: Optional[str] = None  # High, Medium, Low
    recent_updates: Optional[str] = None  # Recent, Moderate, Stale
    market_position: Optional[str] = None  # Leader, Challenger, Niche, New


class CompanyInfo(BaseModel):
    name: str
    description: str
    website: str
    pricing_model: Optional[str] = None
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    competitors: List[str] = []
    # Developer-specific fields
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []
    developer_experience_rating: Optional[str] = None  # Poor, Good, Excellent
    # Trend analysis fields
    trend_status: Optional[str] = None  # Rising, Stable, Declining, Hot, Emerging
    popularity_score: Optional[int] = None  # 1-10 scale
    community_activity: Optional[str] = None  # High, Medium, Low
    recent_updates: Optional[str] = None  # Recent, Moderate, Stale
    market_position: Optional[str] = None  # Leader, Challenger, Niche, New


class ComparisonMatrix(BaseModel):
    """Structured comparison matrix for tools"""
    tools: List[str]
    categories: List[str]
    matrix: Dict[str, Dict[str, str]]  # tool_name -> category -> value


class ResearchState(BaseModel):
    query: str
    extracted_tools: List[str] = []  # Tools extracted from articles
    companies: List[CompanyInfo] = []
    search_results: List[Dict[str, Any]] = []
    analysis: Optional[str] = None
    report: Optional[str] = None
    comparison_matrix: Optional[ComparisonMatrix] = None