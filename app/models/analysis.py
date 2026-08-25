from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class AnalysisCreate(BaseModel):
    repository_url: str
    depth: str = "deep"  # standard, deep, architecture_only, security_focus


class AnalysisStatus(BaseModel):
    id: str
    status: str  # pending, running, completed, failed
    stage: str = ""
    progress: int = 0
    message: str = ""


class Issue(BaseModel):
    severity: str  # critical, high, medium, low, informational
    title: str
    description: str
    file: Optional[str] = None
    evidence: Optional[str] = None
    recommendation: Optional[str] = None
    confidence: str = "medium"  # high, medium, low


class SecurityFinding(BaseModel):
    severity: str
    category: str
    title: str
    description: str
    file: Optional[str] = None
    evidence: Optional[str] = None


class HealthScore(BaseModel):
    overall: int
    architecture: int
    code_quality: int
    testing: int
    documentation: int
    security: int
    configuration: int
    deployment_readiness: int
    completeness: int


class AnalysisResult(BaseModel):
    id: str
    user_id: str
    repository_url: str
    owner: str
    repository: str
    status: str
    depth: str
    health_score: Optional[HealthScore] = None
    technology_stack: List[str] = []
    languages: Dict[str, int] = {}
    total_files: int = 0
    total_issues: int = 0
    completeness_category: str = ""
    created_at: str
    completed_at: Optional[str] = None
    report_id: Optional[str] = None
    error: Optional[str] = None
