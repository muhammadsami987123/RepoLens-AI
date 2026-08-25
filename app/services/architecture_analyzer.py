"""
Architecture analyzer: detects project type, frameworks, tech stack, and structure patterns.
"""
import re
from typing import Dict, Any, List


FRAMEWORK_SIGNALS = {
    # Python
    "fastapi": ["fastapi", "from fastapi import", "FastAPI()"],
    "django": ["django", "from django", "DJANGO_SETTINGS_MODULE"],
    "flask": ["flask", "from flask import", "Flask(__name__)"],
    "sqlalchemy": ["sqlalchemy", "from sqlalchemy"],
    "celery": ["celery", "from celery import"],
    # JavaScript/TypeScript
    "react": ["react", "from 'react'", 'from "react"', "ReactDOM"],
    "nextjs": ["next/", "from 'next'", "getServerSideProps", "getStaticProps"],
    "vue": ["vue", "from 'vue'", "createApp"],
    "express": ["express()", "const express", "require('express')"],
    "nestjs": ["@nestjs/", "from '@nestjs"],
    # CSS
    "tailwind": ["tailwindcss", "tailwind.config", "@tailwind"],
    # Databases
    "postgresql": ["postgresql", "postgres", "psycopg2", "pg"],
    "mysql": ["mysql", "pymysql", "mysql2"],
    "mongodb": ["mongodb", "mongoose", "pymongo"],
    "redis": ["redis", "aioredis"],
    "sqlite": ["sqlite", "sqlite3"],
    # Tools
    "docker": ["Dockerfile", "docker-compose"],
    "kubernetes": ["kubernetes", "k8s", "kubectl"],
    "pytest": ["pytest", "import pytest"],
    "jest": ["jest", "describe(", "it(", "test("],
    "openai": ["openai", "from openai", "ChatCompletion"],
    "langchain": ["langchain", "from langchain"],
}

ARCHITECTURE_PATTERNS = {
    "Monorepo": ["packages/", "apps/", "libs/", "turbo.json", "nx.json", "lerna.json"],
    "Microservices": ["services/", "docker-compose", "kubernetes", ".proto"],
    "Serverless": ["vercel.json", "netlify.toml", "serverless.yml", "aws-lambda"],
    "MVC": ["controllers/", "models/", "views/", "routes/"],
    "REST API": ["api/", "routes/", "endpoints/", "swagger", "openapi"],
    "Full-Stack": ["frontend/", "backend/", "client/", "server/"],
    "CLI Tool": ["cli.py", "cli/", "__main__.py", "bin/", "cmd/"],
    "Library/Package": ["__init__.py", "setup.py", "pyproject.toml", "index.js", "src/index.ts"],
}


def analyze_architecture(
    all_paths: List[str],
    file_contents: Dict[str, str],
    metadata: Dict,
    languages: Dict[str, int],
) -> Dict[str, Any]:
    """Detect tech stack, frameworks, and architectural patterns."""

    result = {
        "tech_stack": [],
        "frameworks": [],
        "databases": [],
        "deployment": [],
        "patterns": [],
        "type": "Unknown",
        "frontend": None,
        "backend": None,
        "score": 75,
        "summary": "",
        "entry_points": [],
        "source_directories": [],
    }

    # Combine all content for scanning
    all_content = "\n".join(file_contents.values()).lower()
    paths_str = "\n".join(all_paths).lower()

    # Detect tech stack from languages
    language_tech = {
        "Python": "Python",
        "JavaScript": "JavaScript",
        "TypeScript": "TypeScript",
        "Go": "Go",
        "Rust": "Rust",
        "Java": "Java",
        "Ruby": "Ruby",
        "PHP": "PHP",
        "C#": "C#",
        "Swift": "Swift",
        "Kotlin": "Kotlin",
    }
    for lang, display in language_tech.items():
        if lang in languages:
            result["tech_stack"].append(display)

    # Detect frameworks
    detected_frameworks = []
    for framework, signals in FRAMEWORK_SIGNALS.items():
        for signal in signals:
            if signal.lower() in all_content or signal.lower() in paths_str:
                detected_frameworks.append(framework)
                break

    result["frameworks"] = detected_frameworks

    # Categorize tech stack
    db_frameworks = {"postgresql", "mysql", "mongodb", "redis", "sqlite"}
    deploy_frameworks = {"docker", "kubernetes"}
    for f in detected_frameworks:
        if f in db_frameworks:
            result["databases"].append(f)
        elif f in deploy_frameworks:
            result["deployment"].append(f)
        else:
            if f not in result["tech_stack"]:
                result["tech_stack"].append(f)

    # Detect architectural patterns
    for pattern, signals in ARCHITECTURE_PATTERNS.items():
        for signal in signals:
            if signal.lower() in paths_str or signal.lower() in all_content:
                result["patterns"].append(pattern)
                break

    # Determine project type
    if "nextjs" in detected_frameworks:
        result["type"] = "Next.js Full-Stack Application"
    elif "react" in detected_frameworks and ("fastapi" in detected_frameworks or "django" in detected_frameworks):
        result["type"] = "Full-Stack Web Application"
    elif "fastapi" in detected_frameworks or "flask" in detected_frameworks or "django" in detected_frameworks:
        result["type"] = "Python Web API"
    elif "express" in detected_frameworks or "nestjs" in detected_frameworks:
        result["type"] = "Node.js API"
    elif "react" in detected_frameworks or "vue" in detected_frameworks:
        result["type"] = "Frontend Web Application"
    elif "Python" in languages and "__main__.py" in paths_str:
        result["type"] = "Python CLI Tool / Library"
    elif "Go" in languages:
        result["type"] = "Go Application"
    elif "Rust" in languages:
        result["type"] = "Rust Application"
    else:
        result["type"] = "Software Project"

    # Entry points
    entry_candidates = [
        "main.py", "app.py", "server.py", "run.py",
        "src/main.py", "app/main.py",
        "index.js", "src/index.js", "server.js",
        "index.ts", "src/index.ts",
        "main.go", "main.rs", "Main.java",
    ]
    for candidate in entry_candidates:
        if candidate in all_paths:
            result["entry_points"].append(candidate)

    # Source directories
    source_dirs = ["src", "app", "lib", "api", "pages", "components",
                   "services", "models", "controllers", "routes", "utils"]
    for d in source_dirs:
        if any(p.startswith(f"{d}/") for p in all_paths):
            result["source_directories"].append(d)

    # Score based on signals
    score = 70
    if result["entry_points"]:
        score += 5
    if result["databases"]:
        score += 5
    if result["deployment"]:
        score += 5
    if len(result["frameworks"]) > 2:
        score += 5
    if result["patterns"]:
        score += 5
    result["score"] = min(score, 95)

    result["summary"] = (
        f"{result['type']} using {', '.join(result['tech_stack'][:5]) or 'unknown stack'}. "
        f"Patterns: {', '.join(result['patterns'][:3]) or 'none detected'}."
    )

    return result
