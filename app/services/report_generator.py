"""
Report generation service: combines all analysis results into a structured report.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List

from app.utils.storage import save_report


def generate_report(
    analysis_id: str,
    user_id: str,
    owner: str,
    repository: str,
    repository_url: str,
    metadata: Dict,
    languages: Dict,
    directory_tree: str,
    file_contents: Dict,
    deps_result: Dict,
    arch_result: Dict,
    security_result: Dict,
    quality_result: Dict,
    completeness_result: Dict,
    ai_result: Dict,
    all_paths: List[str],
) -> str:
    """Generate and persist the complete analysis report. Returns report_id."""
    report_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    health_score = {
        "overall": completeness_result.get("overall_score", 75),
        "architecture": arch_result.get("score", 75),
        "code_quality": quality_result.get("score", 70),
        "testing": completeness_result.get("testing_score", 60),
        "documentation": completeness_result.get("documentation_score", 70),
        "security": security_result.get("score", 75),
        "configuration": completeness_result.get("configuration_score", 75),
        "deployment_readiness": completeness_result.get("deployment_score", 65),
        "completeness": completeness_result.get("completeness_score", 70),
    }

    all_issues = (
        security_result.get("issues", []) +
        quality_result.get("issues", []) +
        ai_result.get("potential_issues", [])
    )

    # De-duplicate by title
    seen_titles = set()
    unique_issues = []
    for issue in all_issues:
        title = issue.get("title", "")
        if title not in seen_titles:
            seen_titles.add(title)
            unique_issues.append(issue)

    # Generate Markdown report
    markdown = _generate_markdown(
        owner=owner,
        repository=repository,
        repository_url=repository_url,
        metadata=metadata,
        languages=languages,
        directory_tree=directory_tree,
        health_score=health_score,
        arch_result=arch_result,
        deps_result=deps_result,
        security_result=security_result,
        quality_result=quality_result,
        completeness_result=completeness_result,
        ai_result=ai_result,
        all_issues=unique_issues,
        all_paths=all_paths,
    )

    report = {
        "id": report_id,
        "analysis_id": analysis_id,
        "user_id": user_id,
        "owner": owner,
        "repository": repository,
        "repository_url": repository_url,
        "created_at": now,
        "health_score": health_score,
        "executive_summary": ai_result.get("executive_summary", ""),
        "repository_overview": (
            f"**Repository:** {owner}/{repository}\n"
            f"**Description:** {metadata.get('description', 'N/A')}\n"
            f"**Stars:** {metadata.get('stargazers_count', 0)} | "
            f"**Forks:** {metadata.get('forks_count', 0)} | "
            f"**Open Issues:** {metadata.get('open_issues_count', 0)}\n"
            f"**Primary Language:** {metadata.get('language', 'N/A')}\n"
            f"**License:** {metadata.get('license', {}).get('name', 'None') if metadata.get('license') else 'None'}"
        ),
        "purpose": ai_result.get("purpose", ""),
        "technology_stack": arch_result.get("tech_stack", []),
        "languages": languages,
        "repository_structure": directory_tree,
        "architecture": ai_result.get("architecture_description", arch_result.get("summary", "")),
        "data_flow": ai_result.get("data_flow", ""),
        "important_files": ai_result.get("important_files_analysis", []),
        "dependencies": deps_result,
        "configuration": ai_result.get("configuration_notes", ""),
        "api_structure": ai_result.get("api_structure", ""),
        "database_structure": ai_result.get("database_structure", ""),
        "authentication_analysis": "",
        "code_quality": ai_result.get("code_quality_assessment", quality_result.get("summary", "")),
        "security_findings": security_result.get("issues", []),
        "performance_considerations": "",
        "issues": unique_issues,
        "runtime_errors": ai_result.get("runtime_errors", ""),
        "completeness": completeness_result,
        "how_to_install": ai_result.get("how_to_install", ""),
        "how_to_run": ai_result.get("how_to_run", ""),
        "how_to_build": ai_result.get("how_to_build", ""),
        "how_to_deploy": ai_result.get("how_to_deploy", ""),
        "recommended_improvements": ai_result.get("recommended_improvements", ""),
        "final_assessment": ai_result.get("final_assessment", completeness_result.get("summary", "")),
        "markdown_report": markdown,
        "raw_analysis": {
            "arch": arch_result,
            "deps": deps_result,
            "security": security_result,
            "quality": quality_result,
            "completeness": completeness_result,
        },
    }

    save_report(report)
    return report_id


def _generate_markdown(
    owner: str, repository: str, repository_url: str,
    metadata: Dict, languages: Dict, directory_tree: str,
    health_score: Dict, arch_result: Dict, deps_result: Dict,
    security_result: Dict, quality_result: Dict, completeness_result: Dict,
    ai_result: Dict, all_issues: List, all_paths: List[str],
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lang_str = ", ".join(list(languages.keys())[:8]) if languages else "Unknown"
    tech_str = ", ".join(arch_result.get("tech_stack", [])[:8]) or "Unknown"
    overall = health_score.get("overall", 0)
    bar = _progress_bar(overall)

    issues_md = ""
    for issue in all_issues[:20]:
        sev = issue.get("severity", "low").upper()
        title = issue.get("title", "")
        desc = issue.get("description", "")
        file_ref = f"\n- **File:** `{issue['file']}`" if issue.get("file") else ""
        rec = f"\n- **Recommendation:** {issue.get('recommendation', '')}" if issue.get("recommendation") else ""
        issues_md += f"\n### [{sev}] {title}\n{desc}{file_ref}{rec}\n"

    sec_issues_md = ""
    for finding in security_result.get("issues", [])[:10]:
        sev = finding.get("severity", "low").upper()
        title = finding.get("title", "")
        desc = finding.get("description", "")
        file_ref = f"\n- **File:** `{finding['file']}`" if finding.get("file") else ""
        sec_issues_md += f"\n### [{sev}] {title}\n{desc}{file_ref}\n"

    deps_prod = deps_result.get("production", [])[:20]
    deps_dev = deps_result.get("development", [])[:15]
    deps_prod_md = "\n".join(f"- `{d['name']}` {d.get('version', '')}" for d in deps_prod) or "None detected"
    deps_dev_md = "\n".join(f"- `{d['name']}` {d.get('version', '')}" for d in deps_dev) or "None detected"

    completeness_bars = f"""
| Dimension | Score |
|-----------|-------|
| Architecture | {completeness_result.get('architecture_score', 0)}/100 |
| Documentation | {completeness_result.get('documentation_score', 0)}/100 |
| Testing | {completeness_result.get('testing_score', 0)}/100 |
| Configuration | {completeness_result.get('configuration_score', 0)}/100 |
| Deployment | {completeness_result.get('deployment_score', 0)}/100 |
| Security | {completeness_result.get('security_score', 0)}/100 |
| CI/CD | {completeness_result.get('cicd_score', 0)}/100 |
"""

    missing = completeness_result.get("missing", [])
    missing_md = "\n".join(f"- {m}" for m in missing) if missing else "No major gaps identified."

    improvements = ai_result.get("recommended_improvements", "")
    if isinstance(improvements, list):
        improvements = "\n".join(f"- {i}" for i in improvements)

    return f"""# Repository Analysis Report

> Generated by RepoLens AI on {now}

---

## Repository

**{owner}/{repository}**
{repository_url}

**Description:** {metadata.get('description', 'No description provided.')}
**Stars:** {metadata.get('stargazers_count', 0)} | **Forks:** {metadata.get('forks_count', 0)} | **Open Issues:** {metadata.get('open_issues_count', 0)}
**Primary Language:** {metadata.get('language', 'N/A')}
**License:** {metadata.get('license', {}).get('name', 'None') if metadata.get('license') else 'None'}
**Created:** {metadata.get('created_at', 'N/A')[:10]}
**Last Updated:** {metadata.get('updated_at', 'N/A')[:10]}

---

## 1. Executive Summary

{ai_result.get('executive_summary', 'Analysis completed using static analysis.')}

---

## 2. Project Health Score

```
Overall Health: {bar} {overall}/100
```

{completeness_bars}

**Category:** {completeness_result.get('category', 'Unknown')}

---

## 3. Purpose

{ai_result.get('purpose', metadata.get('description', 'Not determined.'))}

---

## 4. Technology Stack

**Languages:** {lang_str}

**Frameworks & Libraries:** {tech_str}

**Package Manager:** {deps_result.get('package_manager', 'Unknown')}

**Architecture Patterns:** {', '.join(arch_result.get('patterns', [])) or 'None detected'}

---

## 5. Repository Structure

```
{directory_tree[:3000]}
```

---

## 6. Architecture

{ai_result.get('architecture_description', arch_result.get('summary', 'Architecture analysis completed.'))}

---

## 7. Data Flow

{ai_result.get('data_flow', 'Data flow analysis requires AI synthesis.')}

---

## 8. Dependencies

**{deps_result.get('summary', 'No dependency information available.')}**

### Production Dependencies
{deps_prod_md}

### Development Dependencies
{deps_dev_md}

---

## 9. Configuration

{ai_result.get('configuration_notes', 'No specific configuration notes.')}

---

## 10. API Structure

{ai_result.get('api_structure', 'No API structure detected or described.')}

---

## 11. Database Structure

{ai_result.get('database_structure', 'No database structure detected.')}

---

## 12. Code Quality

{ai_result.get('code_quality_assessment', quality_result.get('summary', ''))}

---

## 13. Security Analysis

**Security Score:** {security_result.get('score', 0)}/100

{sec_issues_md or 'No significant security issues detected.'}

---

## 14. Potential Issues

{issues_md or 'No significant issues detected.'}

---

## 15. Possible Runtime Errors

{ai_result.get('runtime_errors', 'No specific runtime errors identified.')}

---

## 16. Project Completeness

{completeness_result.get('summary', '')}

### Missing Components
{missing_md}

---

## 17. How To Install

{ai_result.get('how_to_install', 'Refer to the repository README for installation instructions.')}

---

## 18. How To Run

{ai_result.get('how_to_run', 'Refer to the repository README for run instructions.')}

---

## 19. How To Build

{ai_result.get('how_to_build', 'No build process detected.')}

---

## 20. How To Deploy

{ai_result.get('how_to_deploy', 'No deployment configuration detected.')}

---

## 21. Recommended Improvements

{improvements or 'Enable AI synthesis for specific recommendations.'}

---

## 22. Final Assessment

{ai_result.get('final_assessment', completeness_result.get('summary', ''))}

---

*Report generated by [RepoLens AI](https://github.com) — AI-powered repository intelligence.*
"""


def _progress_bar(score: int, width: int = 20) -> str:
    filled = int((score / 100) * width)
    return "█" * filled + "░" * (width - filled)
