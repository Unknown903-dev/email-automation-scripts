from __future__ import annotations

import argparse
import sys
from typing import Any

from .client import CanvasAPIError, CanvasClient
from .config import load_settings
from .files import (
    append_sent_log,
    chunks,
    filter_users,
    load_sent_ids,
    read_filter_values,
    read_text_file,
    remove_already_sent,
    render_template,
)

# defines all commands and their arguments for the command line interface
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="canvas-inviter",
        description="Send course invitation messages through the Canvas Conversations API.",
    )
    #creates command
    subparsers = parser.add_subparsers(dest="command", required=True)
    #list courses
    subparsers.add_parser("courses", help="List courses visible to your Canvas token")

    #list users in a course with there specified role (default is student)
    users = subparsers.add_parser("users", help="List active users in a course")
    users.add_argument("--course-id", required=True, help="Canvas course ID")
    users.add_argument("--role", default="student", choices=["student", "teacher", "ta", "observer", "designer"])

    #sends the message to the users in the course with the specified role (default is student)
    send = subparsers.add_parser("send", help="Send a Canvas Inbox message to course users")
    send.add_argument("--course-id", required=True, help="Canvas course ID")
    send.add_argument("--subject", required=True, help="Message subject")
    send.add_argument("--message-file", required=True, help="Text file containing the message body")
    send.add_argument("--recipients-csv", help="Optional CSV filter with id/name/login_id/email columns")
    send.add_argument("--role", default="student", choices=["student", "teacher", "ta", "observer", "designer"])
    send.add_argument("--sent-log", default="data/sent_log.csv", help="CSV file used to skip already-sent users")
    send.add_argument("--batch-size", type=int, default=50, help="Recipients per Canvas request")
    send.add_argument("--mode", choices=["sync", "async"], default="sync", help="Canvas delivery mode")
   
    # send group conversation instead of individual messages
    send.add_argument(
        "--group-conversation",
        action="store_true",
        help="Make one shared group conversation. Default creates private messages.",
    )
    #avoid sending to users already listed in the sent log
    send.add_argument(
        "--no-dedupe",
        action="store_true",
        help="Do not skip users already listed in the sent log.",
    )
    # send the email
    send.add_argument(
        "--send",
        action="store_true",
        help="Actually send. Without this flag, the command is a dry run.",
    )

    return parser

