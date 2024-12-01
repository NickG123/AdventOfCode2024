"""Helpers related to interacting with the AOC website."""
import json
import os
import sqlite3
from pathlib import Path
from typing import BinaryIO

import requests

INPUT_URL = "https://adventofcode.com/{year}/day/{day}/input"
COOKIE_HOST = ".adventofcode.com"
COOKIE_NAME = "session"


def get_firefox_session() -> str:
    """Steal a session cookie from the firefox sqlite database."""
    cookie_files = find_firefox_cookie_db_paths()
    for cookie_file in cookie_files:
        try:
            print(cookie_file)
            session = get_session_cookie_from_db(cookie_file)
            return session
        except Exception:
            pass
    raise Exception("Failed to find session cookie")


def find_firefox_cookie_db_paths() -> list[Path]:
    """Find the path to the firefox cookie database."""
    if os.name == "nt":
        app_data_path = Path(os.environ["APPDATA"])
        firefox_profiles = app_data_path / "Mozilla" / "Firefox" / "Profiles"
    else:
        firefox_profiles = (
            Path(os.environ["HOME"])
            / "Library"
            / "Application Support"
            / "Firefox"
            / "Profiles"
        )

    cookie_candidates = [
        subfolder / "cookies.sqlite"
        for subfolder in firefox_profiles.iterdir()
        if (subfolder / "cookies.sqlite").is_file()
    ]

    match cookie_candidates:
        case []:
            raise Exception("Failed to find Firefox profile")
        case _:
            return sorted(
                cookie_candidates, key=lambda p: p.stat().st_mtime, reverse=True
            )


def get_session_cookie_from_db(sqlite_file: Path) -> str:
    """Retrieve the session cookie from the firefox cookie database."""
    conn = sqlite3.connect(sqlite_file)
    try:
        cur = conn.cursor()
        for row in cur.execute(
            "SELECT value FROM moz_cookies WHERE name=? AND host=?",
            (COOKIE_NAME, COOKIE_HOST),
        ):
            return str(row[0])
        raise Exception("No session cookie found")
    finally:
        conn.close()


def download_problem_input(filelike: BinaryIO, year: int, day: int) -> None:
    """Download the input file for a problem."""
    config_path = Path() / "config.json"
    if config_path.exists():
        session = json.loads(config_path.read_text())["Session"]
    else:
        session = get_firefox_session()
    resp = requests.get(
        INPUT_URL.format(year=year, day=day), cookies={"session": session}
    )
    resp.raise_for_status()
    filelike.write(resp.content)
