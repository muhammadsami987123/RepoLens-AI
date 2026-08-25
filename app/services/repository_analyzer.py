"""
Main repository analysis orchestrator.
Coordinates all sub-analyzers and drives the analysis pipeline.
"""
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Callable, Optional

from app.services.github_service import (
    validate_github_url, get_repo_metadata, get_repo_languages,
    get_repo_tree, get_file_content, filter_tree, identify_important_files,
    build_directory_tree,
)
from app.services.dependency_analyzer import analyze_dependencies
from app.services.architecture_analyzer import analyze_architecture
from app.services.security_analyzer import analyze_security
from app.services.quality_analyzer import analyze_code_quality
from app.services.completeness_analyzer import analyze_completeness
from app.services.ai_analyzer import synthesize_with_ai
from app.services.report_generator import generate_report
from app.utils.storage import save_analysis, save_report, get_analysis_by_id
from app.config import settings


async def run_analysis(
    analysis_id: str,
    user_id: str,
    repository_url: str,
    depth: str = "deep",
    progress_callback: Optional[Callable[[str, int, str], None]] = None,
) -> Dict[str, Any]:
    """
    Full analysis pipeline. Updates analysis record with progress.
    Returns the completed analysis dict.
    """

    def update_progress(stage: str, progress: int, message: str):
        analysis = get_analysis_by_id(analysis_id)
        if analysis:
            analysis["stage"] = stage
            analysis["progress"] = progress
            analysis["message"] = message
            analysis["status"] = "running"
            save_analysis(analysis)
        if progress_callback:
            progress_callback(stage, progress, message)

    try:
        # Stage 1: Validate URL
        update_progress("validation", 5, "Validating repository URL...")
        is_valid, owner, repo = validate_github_url(repository_url)
        if not is_valid:
            raise ValueError("Invalid GitHub repository URL")

        # Stage 2: Fetch metadata
        update_progress("metadata", 10, "Fetching repository metadata...")
        metadata = await get_repo_metadata(owner, repo)
        default_branch = metadata.get("default_branch", "HEAD")

        # Stage 3: Fetch languages
        update_progress("languages", 15, "Detecting programming languages...")
        languages = await get_repo_languages(owner, repo)

        # Stage 4: Fetch tree
        update_progress("tree", 20, "Scanning repository structure...")
        raw_tree = await get_repo_tree(owner, repo, default_branch)
        filtered_tree, ignored = filter_tree(raw_tree)
        all_paths = [item["path"] for item in filtered_tree]

        # Stage 5: Identify important files
        update_progress("files", 30, "Identifying important files...")
        important_paths = identify_important_files(all_paths)
        directory_tree = build_directory_tree(all_paths[:500])  # Limit for display

        # Stage 6: Fetch file contents
        update_progress("content", 40, "Reading key configuration files...")
        file_contents: Dict[str, str] = {}
        for path in important_paths[:settings.max_files_to_analyze]:
            content = await get_file_content(owner, repo, path)
            if content:
                file_contents[path] = content

        # Stage 7: Dependency analysis
        update_progress("dependencies", 50, "Analyzing dependencies...")
        deps_result = analyze_dependencies(file_contents)

        # Stage 8: Architecture analysis
        update_progress("architecture", 60, "Mapping application architecture...")
        arch_result = analyze_architecture(all_paths, file_contents, metadata, languages)

        # Stage 9: Security analysis
        update_progress("security", 70, "Checking for security concerns...")
        security_result = analyze_security(file_contents, all_paths)

        # Stage 10: Code quality
        update_progress("quality", 75, "Evaluating code quality...")
        quality_result = analyze_code_quality(file_contents, all_paths, languages)

        # Stage 11: Completeness
        update_progress("completeness", 80, "Assessing project completeness...")
        completeness_result = analyze_completeness(
            file_contents, all_paths, metadata, deps_result, languages
        )

        # Stage 12: AI synthesis
        update_progress("ai_synthesis", 88, "AI is synthesizing findings...")
        context = {
            "metadata": metadata,
            "owner": owner,
            "repository": repo,
            "languages": languages,
            "directory_tree": directory_tree,
            "important_files": important_paths,
            "file_contents": file_contents,
            "dependencies": deps_result,
            "architecture": arch_result,
            "security": security_result,
            "quality": quality_result,
            "completeness": completeness_result,
            "total_files": len(all_paths),
            "depth": depth,
        }
        ai_result = await synthesize_with_ai(context)

        # Stage 13: Generate report
        update_progress("report", 95, "Generating technical report...")
        report_id = generate_report(
            analysis_id=analysis_id,
            user_id=user_id,
            owner=owner,
            repository=repo,
            repository_url=repository_url,
            metadata=metadata,
            languages=languages,
            directory_tree=directory_tree,
            file_contents=file_contents,
            deps_result=deps_result,
            arch_result=arch_result,
            security_result=security_result,
            quality_result=quality_result,
            completeness_result=completeness_result,
            ai_result=ai_result,
            all_paths=all_paths,
        )

        # Stage 14: Complete
        update_progress("completed", 100, "Analysis complete!")

        # Build health score
        health = {
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

        issues = security_result.get("issues", []) + quality_result.get("issues", [])

        # Update analysis record as completed
        analysis = get_analysis_by_id(analysis_id)
        if analysis:
            analysis.update({
                "status": "completed",
                "stage": "completed",
                "progress": 100,
                "message": "Analysis complete",
                "health_score": health,
                "technology_stack": arch_result.get("tech_stack", []),
                "languages": languages,
                "total_files": len(all_paths),
                "total_issues": len(issues),
                "completeness_category": completeness_result.get("category", "Unknown"),
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "report_id": report_id,
            })
            save_analysis(analysis)

        return get_analysis_by_id(analysis_id)

    except Exception as e:
        analysis = get_analysis_by_id(analysis_id)
        if analysis:
            analysis.update({
                "status": "failed",
                "stage": "error",
                "progress": 0,
                "message": str(e),
                "error": str(e),
            })
            save_analysis(analysis)
        raise
