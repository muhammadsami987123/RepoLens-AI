from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ReportSection(BaseModel):
    title: str
    content: str


class Report(BaseModel):
    id: str
    analysis_id: str
    user_id: str
    owner: str
    repository: str
    repository_url: str
    created_at: str
    health_score: Dict[str, Any] = {}
    executive_summary: str = ""
    repository_overview: str = ""
    purpose: str = ""
    technology_stack: List[str] = []
    languages: Dict[str, int] = {}
    repository_structure: str = ""
    architecture: str = ""
    data_flow: str = ""
    important_files: List[Dict[str, Any]] = []
    dependencies: Dict[str, Any] = {}
    configuration: str = ""
    api_structure: str = ""
    database_structure: str = ""
    authentication_analysis: str = ""
    code_quality: str = ""
    security_findings: List[Dict[str, Any]] = []
    performance_considerations: str = ""
    issues: List[Dict[str, Any]] = []
    runtime_errors: str = ""
    completeness: Dict[str, Any] = {}
    how_to_install: str = ""
    how_to_run: str = ""
    how_to_build: str = ""
    how_to_deploy: str = ""
    recommended_improvements: str = ""
    final_assessment: str = ""
    markdown_report: str = ""
    raw_analysis: Dict[str, Any] = {}
