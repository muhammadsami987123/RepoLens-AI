"""
Project completeness and health assessment service.
"""
from typing import Dict, Any, List


COMPLETENESS_SIGNALS = {
    "documentation": [
        "README.md", "readme.md", "CONTRIBUTING.md", "CHANGELOG.md",
        "docs/", "documentation/", "wiki/",
    ],
    "testing": [
        "tests/", "test/", "__tests__/", "spec/",
        "pytest.ini", "jest.config", ".mocharc",
        "requirements-test.txt", "requirements-dev.txt",
    ],
    "configuration": [
        ".env.example", ".env.sample", "config/",
        "Makefile", "docker-compose.yml", "Dockerfile",
    ],
    "deployment": [
        "Dockerfile", "docker-compose.yml",
        "vercel.json", "netlify.toml", ".github/workflows",
        "kubernetes/", "k8s/", "heroku.yml",
        "fly.toml", "railway.toml",
    ],
    "security": [
        "SECURITY.md", ".github/SECURITY.md",
        ".gitignore", ".env.example",
    ],
    "ci_cd": [
        ".github/workflows", ".gitlab-ci.yml",
        ".travis.yml", "Jenkinsfile", ".circleci/",
    ],
}

CATEGORY_THRESHOLDS = {
    "Production Ready": 85,
    "Mostly Complete": 70,
    "MVP / Prototype": 50,
    "Incomplete": 30,
    "Experimental": 0,
}


def analyze_completeness(
    file_contents: Dict[str, str],
    all_paths: List[str],
    metadata: Dict,
    deps_result: Dict,
    languages: Dict[str, int],
) -> Dict[str, Any]:
    """Assess project completeness across multiple dimensions."""
    paths_lower = [p.lower() for p in all_paths]
    paths_str = "\n".join(paths_lower)

    def signal_present(signals: List[str]) -> int:
        """Count how many signals are present (0-100 score)."""
        found = 0
        for sig in signals:
            sig_lower = sig.lower()
            if sig_lower in paths_str or any(sig_lower in p for p in paths_lower):
                found += 1
        return min(int((found / len(signals)) * 100), 100) if signals else 50

    # Documentation score
    doc_score = signal_present(COMPLETENESS_SIGNALS["documentation"])
    # Boost if README has substance
    readme_content = (
        file_contents.get("README.md", "") or
        file_contents.get("readme.md", "")
    )
    if len(readme_content) > 1000:
        doc_score = min(doc_score + 20, 100)
    elif len(readme_content) > 300:
        doc_score = min(doc_score + 10, 100)

    # Testing score
    test_score = signal_present(COMPLETENESS_SIGNALS["testing"])
    has_tests = test_score > 0
    if not has_tests:
        test_score = 10

    # Configuration score
    config_score = signal_present(COMPLETENESS_SIGNALS["configuration"])

    # Deployment score
    deploy_score = signal_present(COMPLETENESS_SIGNALS["deployment"])

    # Security score
    security_score = signal_present(COMPLETENESS_SIGNALS["security"])

    # CI/CD score
    cicd_score = signal_present(COMPLETENESS_SIGNALS["ci_cd"])

    # Architecture score (presence of organized structure)
    structured_dirs = sum(
        1 for d in ["src/", "app/", "lib/", "api/", "services/", "components/"]
        if any(p.startswith(d.rstrip("/")) for p in paths_lower)
    )
    arch_score = min(structured_dirs * 15 + 40, 100)

    # Dependency management score
    dep_score = 60
    if deps_result.get("dependency_files"):
        dep_score = 85
    if len(deps_result.get("production", [])) > 0:
        dep_score = min(dep_score + 10, 100)

    # Overall weighted score
    overall = int(
        doc_score * 0.15 +
        test_score * 0.20 +
        config_score * 0.10 +
        deploy_score * 0.15 +
        security_score * 0.10 +
        arch_score * 0.15 +
        dep_score * 0.10 +
        cicd_score * 0.05
    )

    # Repository maturity signals
    stars = metadata.get("stargazers_count", 0)
    forks = metadata.get("forks_count", 0)
    open_issues_count = metadata.get("open_issues_count", 0)
    has_license = metadata.get("license") is not None
    has_description = bool(metadata.get("description"))

    if has_license:
        overall = min(overall + 3, 100)
    if has_description:
        overall = min(overall + 2, 100)
    if stars > 100:
        overall = min(overall + 5, 100)

    # Determine category
    category = "Experimental"
    for cat, threshold in CATEGORY_THRESHOLDS.items():
        if overall >= threshold:
            category = cat
            break

    # What's missing
    missing = []
    if doc_score < 50:
        missing.append("Comprehensive documentation")
    if test_score < 30:
        missing.append("Test suite")
    if deploy_score < 30:
        missing.append("Deployment configuration")
    if security_score < 50:
        missing.append("Security documentation (.env.example, SECURITY.md)")
    if cicd_score < 30:
        missing.append("CI/CD pipeline")
    if not has_license:
        missing.append("License file")

    return {
        "overall_score": overall,
        "category": category,
        "documentation_score": doc_score,
        "testing_score": test_score,
        "configuration_score": config_score,
        "deployment_score": deploy_score,
        "security_score": security_score,
        "architecture_score": arch_score,
        "dependency_score": dep_score,
        "cicd_score": cicd_score,
        "completeness_score": overall,
        "has_tests": has_tests,
        "has_license": has_license,
        "has_description": has_description,
        "missing": missing,
        "stars": stars,
        "forks": forks,
        "open_issues": open_issues_count,
        "summary": f"Project is {category} with an overall health score of {overall}/100.",
    }
