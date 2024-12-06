from datetime import datetime, UTC
import json
import logging
from typing import Any

from environs import Env
from jinja2 import Environment, FileSystemLoader
import requests

env = Env()
env.read_env()


def get_aoc_leaderboard() -> list[dict[str, Any]]:
    """Get the current leaderboard"""
    logging.info("Fetching leaderboard")
    jar = requests.cookies.RequestsCookieJar()
    jar.set("session", env("AOC_SESSION_COOKIE"), domain="adventofcode.com")
    r = requests.get(env("AOC_LEADERBOARD_URL"), cookies=jar)
    r.raise_for_status()

    data = r.json()
    return sorted(
        data["members"].values(),
        key=lambda d: (d.get("local_score"), d.get("starts"), d.get("name")),
        reverse=True,
    )


def send_slack_message(scoreboard: list[dict[str, Any]]) -> None:
    logging.info("Updating slack")

    template_env = Environment(
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<#",
        comment_end_string="#>",
        loader=FileSystemLoader("templates"),
    )
    template = template_env.get_template("payload.json")
    payload = json.loads(
        template.render(now=datetime.now(tz=UTC), scoreboard=scoreboard)
    )

    r = requests.post(env("SLACK_WEBHOOK_URL"), json=payload)
    r.raise_for_status()


if __name__ == "__main__":
    scoreboard = get_aoc_leaderboard()
    send_slack_message(scoreboard)
