"""
Security analysis service: checks for common security issues in code.
"""
import re
from typing import Dict, Any, List


SECURITY_PATTERNS = [
    {
        "id": "hardcoded_secret",
        "pattern": r'(?i)(password|secret|api_key|apikey|token|passwd|pwd)\s*=\s*["\'][^"\']{6,}["\']',
        "title": "Potential hardcoded secret",
        "severity": "high",
        "category": "Secrets",
        "description": "A variable that appears to hold sensitive credentials contains a hardcoded string value.",
        "recommendation": "Move secrets to environment variables and use a .env file. Never commit secrets to version control.",
    },
    {
        "id": "debug_mode",
        "pattern": r'(?i)(debug\s*=\s*true|DEBUG\s*=\s*True)',
        "title": "Debug mode enabled",
        "severity": "medium",
        "category": "Configuration",
        "description": "Debug mode appears to be enabled, which may expose stack traces and internal details.",
        "recommendation": "Ensure debug mode is disabled in production environments.",
    },
    {
        "id": "sql_injection",
        "pattern": r'(?i)(execute|cursor\.execute|query)\s*\(\s*f["\']|\.format\(',
        "title": "Potential SQL injection risk",
        "severity": "high",
        "category": "Injection",
        "description": "SQL queries constructed with string formatting may be vulnerable to injection.",
        "recommendation": "Use parameterized queries or an ORM to prevent SQL injection.",
    },
    {
        "id": "shell_exec",
        "pattern": r'(?i)(os\.system|subprocess\.call|eval\(|exec\()',
        "title": "Shell execution or code eval detected",
        "severity": "medium",
        "category": "Injection",
        "description": "Shell commands or code evaluation found, which can be dangerous if inputs are not sanitized.",
        "recommendation": "Validate and sanitize all inputs before shell execution. Prefer subprocess with argument lists.",
    },
    {
        "id": "cors_wildcard",
        "pattern": r'(?i)(allow_origins\s*=\s*\[?\s*["\*]|Access-Control-Allow-Origin["\s]*:\s*["\*])',
        "title": "Permissive CORS configuration",
        "severity": "medium",
        "category": "Configuration",
        "description": "CORS is configured with wildcard (*) which allows any origin to make cross-origin requests.",
        "recommendation": "Restrict CORS to specific trusted domains in production.",
    },
    {
        "id": "no_auth_check",
        "pattern": r'(?i)@app\.(get|post|put|delete|patch)\s*\((?!.*depend)',
        "title": "API endpoint may lack authentication",
        "severity": "low",
        "category": "Authentication",
        "description": "API endpoint defined without visible dependency injection for authentication.",
        "recommendation": "Ensure all sensitive endpoints verify authentication using dependency injection or decorators.",
    },
    {
        "id": "insecure_http",
        "pattern": r'http://(?!localhost|127\.0\.0\.1|0\.0\.0\.0)',
        "title": "HTTP used instead of HTTPS",
        "severity": "low",
        "category": "Transport",
        "description": "HTTP URLs detected in code, which transmit data in plaintext.",
        "recommendation": "Use HTTPS for all external communication.",
    },
    {
        "id": "env_key_exposure",
        "pattern": r'(?i)os\.environ\[.*(key|secret|password|token)',
        "title": "Environment variable access for sensitive key",
        "severity": "informational",
        "category": "Configuration",
        "description": "Sensitive environment variable accessed directly. Ensure proper .env management.",
        "recommendation": "Use a settings management library (e.g., pydantic-settings) for structured environment handling.",
    },
]


def analyze_security(file_contents: Dict[str, str], all_paths: List[str]) -> Dict[str, Any]:
    """Run security pattern checks across all file contents."""
    issues = []
    findings_by_file: Dict[str, List] = {}
    seen_ids: set = set()

    for file_path, content in file_contents.items():
        # Skip lock files and non-code files
        if file_path.endswith((".lock", ".json")) and "package.json" not in file_path:
            continue

        file_issues = []
        for pattern_def in SECURITY_PATTERNS:
            matches = re.findall(pattern_def["pattern"], content)
            if matches:
                dedup_key = f"{file_path}:{pattern_def['id']}"
                if dedup_key not in seen_ids:
                    seen_ids.add(dedup_key)
                    issue = {
                        "severity": pattern_def["severity"],
                        "category": pattern_def["category"],
                        "title": pattern_def["title"],
                        "description": pattern_def["description"],
                        "file": file_path,
                        "evidence": f"Pattern matched in {file_path}",
                        "recommendation": pattern_def["recommendation"],
                        "confidence": "medium",
                        "type": "security",
                    }
                    file_issues.append(issue)
                    issues.append(issue)

        if file_issues:
            findings_by_file[file_path] = file_issues

    # Check for missing security files
    has_env_example = any(".env.example" in p or ".env.sample" in p for p in all_paths)
    has_gitignore = ".gitignore" in all_paths
    has_security_md = any("SECURITY.md" in p or "security.md" in p for p in all_paths)

    positive_signals = []
    if has_env_example:
        positive_signals.append(".env.example present — credentials not committed")
    if has_gitignore:
        positive_signals.append(".gitignore present")
    if has_security_md:
        positive_signals.append("SECURITY.md present")

    # Calculate security score
    severity_weights = {"critical": -20, "high": -10, "medium": -5, "low": -2, "informational": -1}
    score = 90
    for issue in issues:
        score += severity_weights.get(issue["severity"], 0)
    score = max(20, min(100, score))

    # Categorize findings
    categories: Dict[str, List] = {}
    for issue in issues:
        cat = issue["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(issue)

    return {
        "issues": issues,
        "findings_by_file": findings_by_file,
        "categories": categories,
        "positive_signals": positive_signals,
        "score": score,
        "total_findings": len(issues),
        "critical": sum(1 for i in issues if i["severity"] == "critical"),
        "high": sum(1 for i in issues if i["severity"] == "high"),
        "medium": sum(1 for i in issues if i["severity"] == "medium"),
        "low": sum(1 for i in issues if i["severity"] == "low"),
        "informational": sum(1 for i in issues if i["severity"] == "informational"),
        "summary": f"{len(issues)} potential security findings. Security score: {score}/100.",
    }
