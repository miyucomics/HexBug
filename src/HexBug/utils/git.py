import subprocess
from datetime import datetime


def _run_command(args: list[str], cwd: str) -> str:
    result = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    assert not result.stderr, result.stderr
    return result.stdout.strip()


def get_current_commit(cwd: str, short: int | None = 10) -> str:
    if short:
        command = ["git", "rev-parse", f"--short={short}", "HEAD"]
    else:
        command = ["git", "rev-parse", "HEAD"]
    return _run_command(command, cwd)


def _get_commit_tags(cwd: str, commit: str) -> list[str]:
    """Returns tags for the given commit for the git repo in cwd, sorted by descending tag text."""
    return _run_command(
        ["git", "tag", "--sort=-committerdate", "--points-at", commit], cwd
    ).split("\n")


def get_latest_tags(cwd: str, commit: str) -> list[str]:
    """Returns tags for the git repo in cwd, sorted by descending date."""
    tags_before = _run_command(
        ["git", "tag", "--sort=-committerdate", "--no-contains", commit], cwd
    ).split("\n")
    return _get_commit_tags(cwd, commit) + tags_before


def get_commit_message(cwd: str, commit: str) -> str:
    return _run_command(["git", "log", "-1", "--pretty=%B", commit], cwd)


def get_commit_date(cwd: str, commit: str) -> str:
    return _run_command(
        ["git", "log", "-1", r"--date=format:'%Y-%m-%d'", r"--pretty=%cd", commit],
        cwd,
    ).strip("'")


def get_commit_datetime(cwd: str, commit: str) -> datetime:
    timestamp = _run_command(
        ["git", "log", "-1", r"--date=iso-strict", r"--pretty=%cd", commit],
        cwd,
    ).strip("'")
    return datetime.fromisoformat(timestamp)
