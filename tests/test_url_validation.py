"""
GitHub URL validation tests.
"""
import pytest
from app.services.github_service import validate_github_url


def test_valid_url():
    valid, owner, repo = validate_github_url("https://github.com/tiangolo/fastapi")
    assert valid is True
    assert owner == "tiangolo"
    assert repo == "fastapi"


def test_valid_url_with_trailing_slash():
    valid, owner, repo = validate_github_url("https://github.com/facebook/react/")
    assert valid is True
    assert owner == "facebook"
    assert repo == "react"


def test_valid_url_with_git_suffix():
    valid, owner, repo = validate_github_url("https://github.com/owner/repo.git")
    assert valid is True
    assert repo == "repo"


def test_invalid_url_not_github():
    valid, _, _ = validate_github_url("https://gitlab.com/owner/repo")
    assert valid is False


def test_invalid_url_missing_repo():
    valid, _, _ = validate_github_url("https://github.com/owner")
    assert valid is False


def test_invalid_url_empty():
    valid, _, _ = validate_github_url("")
    assert valid is False


def test_invalid_url_no_protocol():
    valid, _, _ = validate_github_url("github.com/owner/repo")
    assert valid is False


def test_invalid_url_extra_path():
    # URLs with extra path components after repo should not be valid
    valid, _, _ = validate_github_url("https://github.com/owner/repo/blob/main/file.py")
    assert valid is False
