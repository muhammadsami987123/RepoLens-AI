"""
Dependency analysis service.
Parses package manifests to extract dependency information.
"""
import json
import re
from typing import Dict, Any, List


def analyze_dependencies(file_contents: Dict[str, str]) -> Dict[str, Any]:
    """Analyze dependency files and return structured dependency info."""
    result = {
        "production": [],
        "development": [],
        "all_dependencies": [],
        "package_manager": None,
        "dependency_files": [],
        "concerns": [],
        "summary": "",
    }

    # Node.js / package.json
    if "package.json" in file_contents:
        result["dependency_files"].append("package.json")
        _parse_package_json(file_contents["package.json"], result)

    # Python / requirements.txt
    for key in ["requirements.txt", "requirements-dev.txt", "requirements-prod.txt"]:
        if key in file_contents:
            result["dependency_files"].append(key)
            _parse_requirements_txt(file_contents[key], result, dev="dev" in key)

    # Python / pyproject.toml
    if "pyproject.toml" in file_contents:
        result["dependency_files"].append("pyproject.toml")
        _parse_pyproject_toml(file_contents["pyproject.toml"], result)

    # Go
    if "go.mod" in file_contents:
        result["dependency_files"].append("go.mod")
        _parse_go_mod(file_contents["go.mod"], result)

    # Rust
    if "Cargo.toml" in file_contents:
        result["dependency_files"].append("Cargo.toml")
        _parse_cargo_toml(file_contents["Cargo.toml"], result)

    total = len(result["production"]) + len(result["development"])
    result["all_dependencies"] = result["production"] + result["development"]
    result["summary"] = (
        f"{total} dependencies found "
        f"({len(result['production'])} production, {len(result['development'])} development)"
    )

    return result


def _parse_package_json(content: str, result: dict) -> None:
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        result["concerns"].append("package.json could not be parsed — may be malformed")
        return

    result["package_manager"] = "npm/yarn/pnpm"

    deps = data.get("dependencies", {})
    dev_deps = data.get("devDependencies", {})

    for name, version in deps.items():
        result["production"].append({"name": name, "version": version, "type": "production"})

    for name, version in dev_deps.items():
        result["development"].append({"name": name, "version": version, "type": "development"})

    # Check for common concerns
    if not deps and not dev_deps:
        result["concerns"].append("No dependencies declared in package.json")

    engines = data.get("engines", {})
    if engines:
        result["engines"] = engines


def _parse_requirements_txt(content: str, result: dict, dev: bool = False) -> None:
    result["package_manager"] = result.get("package_manager") or "pip"
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        # Parse name==version or name>=version or just name
        match = re.match(r"^([a-zA-Z0-9_\-\.]+)\s*([>=<!~^]{1,2}\s*[\d\.\*]+)?", line)
        if match:
            name = match.group(1)
            version = match.group(2) or "any"
            entry = {"name": name, "version": version.strip(), "type": "development" if dev else "production"}
            if dev:
                result["development"].append(entry)
            else:
                result["production"].append(entry)


def _parse_pyproject_toml(content: str, result: dict) -> None:
    result["package_manager"] = result.get("package_manager") or "pip/poetry"
    # Simple TOML parsing for dependencies section
    in_deps = False
    for line in content.splitlines():
        stripped = line.strip()
        if "[tool.poetry.dependencies]" in stripped or "[project.dependencies]" in stripped:
            in_deps = True
            continue
        if in_deps and stripped.startswith("["):
            in_deps = False
        if in_deps and "=" in stripped and not stripped.startswith("#"):
            parts = stripped.split("=", 1)
            name = parts[0].strip().strip('"')
            version = parts[1].strip().strip('"').strip("'")
            if name and name != "python":
                result["production"].append({"name": name, "version": version, "type": "production"})


def _parse_go_mod(content: str, result: dict) -> None:
    result["package_manager"] = "go modules"
    in_require = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped == "require (":
            in_require = True
            continue
        if in_require and stripped == ")":
            in_require = False
            continue
        if stripped.startswith("require ") or in_require:
            parts = stripped.replace("require ", "").strip().split()
            if len(parts) >= 2:
                result["production"].append({
                    "name": parts[0],
                    "version": parts[1],
                    "type": "production",
                })


def _parse_cargo_toml(content: str, result: dict) -> None:
    result["package_manager"] = "cargo"
    in_deps = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped in ("[dependencies]", "[dev-dependencies]"):
            in_deps = stripped
            continue
        if stripped.startswith("[") and stripped not in ("[dependencies]", "[dev-dependencies]"):
            in_deps = False
        if in_deps and "=" in stripped and not stripped.startswith("#"):
            parts = stripped.split("=", 1)
            name = parts[0].strip()
            version = parts[1].strip().strip('"').strip("'").strip("{").strip()
            dep_type = "development" if in_deps == "[dev-dependencies]" else "production"
            result[dep_type].append({"name": name, "version": version, "type": dep_type})
