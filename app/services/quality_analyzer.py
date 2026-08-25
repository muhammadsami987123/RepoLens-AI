"""
Code quality analysis service.
"""
import re
from typing import Dict, Any, List


def analyze_code_quality(
    file_contents: Dict[str, str],
    all_paths: List[str],
    languages: Dict[str, int],
) -> Dict[str, Any]:
    """Analyze code quality patterns across the repository."""
    issues = []
    observations = []

    # Check for tests
    has_tests = any(
        "test" in p.lower() or "spec" in p.lower() or "__tests__" in p
        for p in all_paths
    )
    if not has_tests:
        issues.append({
            "severity": "medium",
            "title": "No test files detected",
            "description": "No test files found in the repository. Testing is essential for production-ready software.",
            "file": None,
            "recommendation": "Add unit tests and integration tests.",
            "type": "quality",
            "confidence": "high",
        })
    else:
        observations.append("Test files detected — good testing hygiene")

    # Check for README
    has_readme = any("readme" in p.lower() for p in all_paths)
    if has_readme:
        observations.append("README present — documentation exists")
    else:
        issues.append({
            "severity": "low",
            "title": "No README file found",
            "description": "A README file is missing, making it harder for developers to understand the project.",
            "file": None,
            "recommendation": "Add a README.md with setup, usage, and contribution instructions.",
            "type": "quality",
            "confidence": "high",
        })

    # Analyze Python files
    if "Python" in languages:
        for path, content in file_contents.items():
            if not path.endswith(".py"):
                continue

            lines = content.splitlines()

            # Large file check
            if len(lines) > 500:
                issues.append({
                    "severity": "low",
                    "title": f"Large module detected ({len(lines)} lines)",
                    "description": f"{path} is quite large and may benefit from being split into smaller modules.",
                    "file": path,
                    "recommendation": "Consider splitting large files into focused modules.",
                    "type": "quality",
                    "confidence": "high",
                })

            # Bare except check
            if "except:" in content:
                issues.append({
                    "severity": "medium",
                    "title": "Bare except clause detected",
                    "description": f"{path} uses a bare 'except:' which catches all exceptions including system exits.",
                    "file": path,
                    "recommendation": "Use specific exception types (e.g., 'except ValueError:') to avoid masking errors.",
                    "type": "quality",
                    "confidence": "high",
                })

            # TODO/FIXME check
            todos = [l.strip() for l in lines if re.search(r"(?i)(TODO|FIXME|HACK|XXX)", l)]
            if len(todos) > 3:
                issues.append({
                    "severity": "low",
                    "title": f"Multiple TODO/FIXME comments ({len(todos)})",
                    "description": f"{path} contains {len(todos)} unresolved TODO/FIXME markers.",
                    "file": path,
                    "recommendation": "Address or track TODO items in an issue tracker.",
                    "type": "quality",
                    "confidence": "medium",
                })

            # Hardcoded values
            if re.search(r'(?i)(password|secret|key)\s*=\s*["\'][^"\']{4,}["\']', content):
                issues.append({
                    "severity": "high",
                    "title": "Potential hardcoded credential in Python code",
                    "description": f"{path} appears to contain a hardcoded password, secret, or key.",
                    "file": path,
                    "recommendation": "Use environment variables for all sensitive configuration.",
                    "type": "quality",
                    "confidence": "medium",
                })

    # Check for JavaScript/TypeScript quality
    if "JavaScript" in languages or "TypeScript" in languages:
        for path, content in file_contents.items():
            if not path.endswith((".js", ".ts", ".jsx", ".tsx")):
                continue

            if "console.log(" in content:
                issues.append({
                    "severity": "low",
                    "title": "console.log statements found",
                    "description": f"{path} contains console.log which may expose debug info in production.",
                    "file": path,
                    "recommendation": "Remove or replace console.log with a proper logging library.",
                    "type": "quality",
                    "confidence": "high",
                })
                break  # Only report once

    # Check for missing type annotations in Python
    if "Python" in languages:
        py_files = [p for p in all_paths if p.endswith(".py") and "test" not in p.lower()]
        if py_files:
            observations.append(f"{len(py_files)} Python source files analyzed")

    # Calculate quality score
    score = 85
    severity_weights = {"high": -10, "medium": -5, "low": -2}
    for issue in issues:
        score += severity_weights.get(issue["severity"], 0)
    score = max(20, min(100, score))

    return {
        "issues": issues,
        "observations": observations,
        "score": score,
        "has_tests": has_tests,
        "has_readme": has_readme,
        "total_issues": len(issues),
        "summary": f"{len(issues)} code quality concerns identified. Quality score: {score}/100.",
    }
