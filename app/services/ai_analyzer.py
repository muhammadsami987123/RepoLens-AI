"""
OpenAI-powered synthesis service.
Constructs structured prompts and synthesizes AI analysis.
"""
import json
from typing import Dict, Any

from openai import AsyncOpenAI
from app.config import settings


async def synthesize_with_ai(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send structured repository context to OpenAI and receive a comprehensive analysis.
    """
    if not settings.openai_api_key:
        return _fallback_analysis(context)

    client = AsyncOpenAI(api_key=settings.openai_api_key)

    # Build structured prompt
    prompt = _build_analysis_prompt(context)

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior software architect and code reviewer. "
                        "Analyze repository data and produce accurate, evidence-based technical assessments. "
                        "Never hallucinate. If unsure, say so. "
                        "Reference specific files when making claims. "
                        "Use hedged language for potential issues: 'appears to', 'may indicate', 'potential concern'."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=4000,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        result = json.loads(content)
        result["ai_powered"] = True
        return result

    except Exception as e:
        result = _fallback_analysis(context)
        result["ai_error"] = str(e)
        return result


def _build_analysis_prompt(context: Dict[str, Any]) -> str:
    metadata = context.get("metadata", {})
    languages = context.get("languages", {})
    directory_tree = context.get("directory_tree", "")
    file_contents = context.get("file_contents", {})
    deps = context.get("dependencies", {})
    arch = context.get("architecture", {})
    security = context.get("security", {})
    quality = context.get("quality", {})
    completeness = context.get("completeness", {})
    owner = context.get("owner", "")
    repository = context.get("repository", "")

    # Truncate file contents for prompt efficiency
    file_excerpts = []
    for path, content in list(file_contents.items())[:20]:
        truncated = content[:2000] if len(content) > 2000 else content
        file_excerpts.append(f"=== {path} ===\n{truncated}")
    files_str = "\n\n".join(file_excerpts)

    dep_summary = deps.get("summary", "No dependency info")
    arch_summary = arch.get("summary", "Unknown architecture")
    sec_issues = security.get("issues", [])[:5]
    qual_issues = quality.get("issues", [])[:5]

    prompt = f"""Analyze this GitHub repository and return a JSON object with these exact keys.

REPOSITORY: {owner}/{repository}
DESCRIPTION: {metadata.get('description', 'No description')}
STARS: {metadata.get('stargazers_count', 0)}
LANGUAGE: {metadata.get('language', 'Unknown')}
LANGUAGES: {json.dumps(languages)}
CREATED: {metadata.get('created_at', 'Unknown')}
UPDATED: {metadata.get('updated_at', 'Unknown')}
TOTAL FILES: {context.get('total_files', 0)}

ARCHITECTURE SUMMARY: {arch_summary}
TECH STACK: {', '.join(arch.get('tech_stack', []))}
FRAMEWORKS: {', '.join(arch.get('frameworks', []))}
PATTERNS: {', '.join(arch.get('patterns', []))}
ENTRY POINTS: {', '.join(arch.get('entry_points', []))}

DEPENDENCIES: {dep_summary}

STATIC SECURITY FINDINGS: {json.dumps(sec_issues, indent=2)}
STATIC QUALITY FINDINGS: {json.dumps(qual_issues, indent=2)}
COMPLETENESS: {completeness.get('summary', '')}
COMPLETENESS SCORES: Documentation={completeness.get('documentation_score')}, Testing={completeness.get('testing_score')}, Deployment={completeness.get('deployment_score')}

DIRECTORY TREE (partial):
{directory_tree[:3000]}

KEY FILE CONTENTS:
{files_str[:8000]}

Return ONLY valid JSON with these keys:
{{
  "executive_summary": "2-3 paragraph high-level summary of what this project is, what problem it solves, and its overall quality",
  "purpose": "What problem does this repository solve? Who is it for?",
  "architecture_description": "Detailed description of the application architecture, components, and how they interact",
  "data_flow": "Describe how data flows through the system from user input to output",
  "important_files_analysis": [
    {{"file": "path/to/file", "purpose": "...", "role": "...", "concerns": "..."}}
  ],
  "code_quality_assessment": "Detailed assessment of code quality, patterns, and areas for improvement",
  "security_assessment": "Security analysis summary and recommendations",
  "how_to_install": "Step-by-step installation instructions derived from the actual repository files",
  "how_to_run": "How to run this project, derived from actual files (README, Makefile, package.json scripts, etc.)",
  "how_to_build": "Build instructions if applicable",
  "how_to_deploy": "Deployment instructions derived from actual deployment configuration files",
  "potential_issues": [
    {{"severity": "high|medium|low", "title": "...", "description": "...", "file": "...", "recommendation": "..."}}
  ],
  "runtime_errors": "Potential runtime errors or startup failures to watch for",
  "recommended_improvements": "Top 5-10 specific, actionable improvements for this repository",
  "final_assessment": "Overall assessment: is this production-ready, prototype, experimental, etc? Why?",
  "api_structure": "Description of API endpoints and structure if applicable",
  "database_structure": "Database schema and models if applicable",
  "configuration_notes": "Important configuration notes and environment variables"
}}

Be specific. Reference actual files. Do not invent functionality not evident in the code."""

    return prompt


def _fallback_analysis(context: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback when OpenAI is unavailable — use static analysis results only."""
    metadata = context.get("metadata", {})
    arch = context.get("architecture", {})
    deps = context.get("dependencies", {})
    completeness = context.get("completeness", {})
    owner = context.get("owner", "")
    repository = context.get("repository", "")
    languages = context.get("languages", {})

    lang_str = ", ".join(list(languages.keys())[:5]) if languages else "multiple languages"
    tech_str = ", ".join(arch.get("tech_stack", [])[:5]) or lang_str

    return {
        "ai_powered": False,
        "executive_summary": (
            f"{owner}/{repository} is a {arch.get('type', 'software project')} "
            f"built with {tech_str}. "
            f"{metadata.get('description', 'No description available.')} "
            f"The project has {completeness.get('overall_score', 0)}/100 health score "
            f"and is categorized as {completeness.get('category', 'Unknown')}."
        ),
        "purpose": metadata.get("description", "Purpose not described in repository metadata."),
        "architecture_description": arch.get("summary", "Architecture analysis completed via static analysis."),
        "data_flow": "Data flow analysis requires AI synthesis. Enable OpenAI API for detailed analysis.",
        "important_files_analysis": [],
        "code_quality_assessment": context.get("quality", {}).get("summary", ""),
        "security_assessment": context.get("security", {}).get("summary", ""),
        "how_to_install": _infer_install_instructions(context.get("file_contents", {}), arch),
        "how_to_run": _infer_run_instructions(context.get("file_contents", {}), arch),
        "how_to_build": "",
        "how_to_deploy": "",
        "potential_issues": context.get("quality", {}).get("issues", [])[:10],
        "runtime_errors": "Enable OpenAI API for detailed runtime error analysis.",
        "recommended_improvements": completeness.get("missing", []),
        "final_assessment": completeness.get("summary", ""),
        "api_structure": "",
        "database_structure": "",
        "configuration_notes": "",
    }


def _infer_install_instructions(file_contents: Dict[str, str], arch: Dict) -> str:
    lines = ["```bash", "git clone <repository-url>", "cd <repository-name>", ""]

    frameworks = arch.get("frameworks", [])

    if "requirements.txt" in file_contents or "pyproject.toml" in file_contents:
        lines += [
            "# Create virtual environment",
            "python -m venv .venv",
            "source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate",
            "",
            "# Install dependencies",
            "pip install -r requirements.txt",
        ]
    elif "package.json" in file_contents:
        lines += ["npm install  # or: yarn install / pnpm install"]
    elif "go.mod" in file_contents:
        lines += ["go mod download"]
    elif "Cargo.toml" in file_contents:
        lines += ["cargo build"]

    lines += ["", "# Configure environment", "cp .env.example .env", "# Edit .env with your configuration", "```"]
    return "\n".join(lines)


def _infer_run_instructions(file_contents: Dict[str, str], arch: Dict) -> str:
    lines = ["```bash"]

    pkg = file_contents.get("package.json", "")
    if pkg:
        try:
            import json
            data = json.loads(pkg)
            scripts = data.get("scripts", {})
            if "dev" in scripts:
                lines.append("npm run dev")
            elif "start" in scripts:
                lines.append("npm start")
            else:
                lines.append("npm start")
        except Exception:
            lines.append("npm start")
    elif "requirements.txt" in file_contents or "pyproject.toml" in file_contents:
        if "fastapi" in str(file_contents).lower():
            lines.append("uvicorn app.main:app --reload")
        elif "django" in str(file_contents).lower():
            lines.append("python manage.py runserver")
        elif "flask" in str(file_contents).lower():
            lines.append("flask run")
        else:
            lines.append("python main.py")
    elif "go.mod" in file_contents:
        lines.append("go run .")
    elif "Cargo.toml" in file_contents:
        lines.append("cargo run")
    else:
        lines.append("# Refer to README.md for run instructions")

    lines.append("```")
    return "\n".join(lines)
