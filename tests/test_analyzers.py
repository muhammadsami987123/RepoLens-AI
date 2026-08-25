"""
Analyzer unit tests.
"""
import pytest
from app.services.dependency_analyzer import analyze_dependencies
from app.services.architecture_analyzer import analyze_architecture
from app.services.security_analyzer import analyze_security
from app.services.completeness_analyzer import analyze_completeness


SAMPLE_PACKAGE_JSON = """{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.0.0",
    "axios": "^1.0.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "typescript": "^5.0.0"
  }
}"""

SAMPLE_REQUIREMENTS = """fastapi==0.115.0
uvicorn==0.30.6
openai==1.51.0
# dev
pytest==8.3.3
"""

SAMPLE_INSECURE_CODE = """
import os
password = "hardcoded_secret_123"
os.system("rm -rf /tmp/cache")
"""


def test_dependency_analysis_node():
    result = analyze_dependencies({"package.json": SAMPLE_PACKAGE_JSON})
    assert result["package_manager"] is not None
    assert len(result["production"]) == 2
    assert len(result["development"]) == 2
    assert result["total"] if "total" in result else len(result["all_dependencies"]) > 0


def test_dependency_analysis_python():
    result = analyze_dependencies({"requirements.txt": SAMPLE_REQUIREMENTS})
    assert result["package_manager"] is not None
    prod = result["production"]
    names = [d["name"] for d in prod]
    assert "fastapi" in names


def test_dependency_analysis_empty():
    result = analyze_dependencies({})
    assert result["production"] == []
    assert result["development"] == []


def test_architecture_detection():
    paths = ["src/index.js", "package.json", "src/components/App.jsx", "src/api/client.js"]
    file_contents = {"package.json": SAMPLE_PACKAGE_JSON}
    result = analyze_architecture(paths, file_contents, {"language": "JavaScript"}, {"JavaScript": 10000})
    assert "JavaScript" in result["tech_stack"]


def test_security_analysis_detects_hardcoded():
    result = analyze_security({"app.py": SAMPLE_INSECURE_CODE}, ["app.py"])
    assert result["total_findings"] > 0
    issues = result["issues"]
    titles = [i["title"] for i in issues]
    assert any("hardcoded" in t.lower() or "secret" in t.lower() or "shell" in t.lower() for t in titles)


def test_security_analysis_clean_code():
    clean = "import os\nkey = os.environ.get('API_KEY')\n"
    result = analyze_security({"clean.py": clean}, ["clean.py"])
    # Should have few or no high severity findings
    assert result["critical"] == 0
    assert result["high"] == 0


def test_completeness_analysis():
    file_contents = {
        "README.md": "# My Project\n\n" + "This is a comprehensive readme. " * 50,
        "requirements.txt": "fastapi==0.115.0\n",
        ".env.example": "API_KEY=\n",
    }
    paths = list(file_contents.keys()) + ["tests/test_main.py", "Dockerfile"]
    metadata = {"stargazers_count": 50, "forks_count": 10, "open_issues_count": 5,
                 "license": {"name": "MIT"}, "description": "A project"}
    deps = {"production": [{"name": "fastapi", "version": "0.115.0"}], "development": [], "dependency_files": ["requirements.txt"]}

    result = analyze_completeness(file_contents, paths, metadata, deps, {"Python": 50000})
    assert result["overall_score"] > 30
    assert "category" in result
    assert result["documentation_score"] > 30
