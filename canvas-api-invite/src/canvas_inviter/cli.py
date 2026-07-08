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

#loads the .env and create the api client
def make_client() -> CanvasClient:
    settings = load_settings()
    return CanvasClient(settings.canvas_base_url, settings.canvas_token)

# grabs courses from the api and prints them to the console
def cmd_courses(client: CanvasClient) -> int:
    courses = client.list_courses()
    if not courses:
        print("No courses returned. Check your token permissions.")
        return 0
    for course in courses:
        print(f"{course.get('id')}\t{course.get('name', '(no name)')}")
    return 0

# grabs the users from the api and prints them to the console
def cmd_users(client: CanvasClient, args: argparse.Namespace) -> int:
    users = client.list_course_users(args.course_id, enrollment_type=args.role)
    if not users:
        print("No users returned. Check the course ID, role filter, and token permissions.")
        return 0
    for user in users:
        pieces = [str(user.get("id", "")), user.get("name", "")]
        if user.get("login_id"):
            pieces.append(user["login_id"])
        if user.get("email"):
            pieces.append(user["email"])
        print("\t".join(pieces))
    return 0

# sends the message to the users in the course with the specified role 
def cmd_send(client: CanvasClient, args: argparse.Namespace) -> int:
    template = read_text_file(args.message_file)
    users = client.list_course_users(args.course_id, enrollment_type=args.role)
    # apply optional csv filter
    users = filter_users(users, read_filter_values(args.recipients_csv))

    #remove sent users
    if not args.no_dedupe:
        users = remove_already_sent(users, load_sent_ids(args.sent_log))

    
    users = sorted(users, key=lambda u: str(u.get("name", "")).lower())


    if not users:
        print("No eligible recipients after filtering/dedupe.")
        return 0
    print(f"Recipients ready: {len(users)}")


    for user in users[:20]:
        print(f"- {user.get('id')} | {user.get('name', '(no name)')}")
    if len(users) > 20:
        print(f"...and {len(users) - 20} more")

    # do a dry run and show user how it will look with the first recipient, unless --send is specified
    if not args.send:
        preview_user = users[0]
        print("\nDRY RUN ONLY. Nothing was sent.")
        print("Add --send when you are ready to send.")
        print("\nPreview with first recipient:")
        print(render_template(template, preview_user))
        return 0

    for batch in chunks(users, args.batch_size):
        # If the template has per-user placeholders, send individually so each user gets their own name.
        per_user_template = any(token in template for token in ("{{name}}", "{{email}}", "{{login_id}}", "{{id}}"))

        if per_user_template:
            for user in batch:
                client.create_conversation(
                    recipients=[user["id"]],
                    subject=args.subject,
                    body=render_template(template, user),
                    course_id=args.course_id,
                    group_conversation=False,
                    force_new=True,
                    mode=args.mode,
                )
        else:
            client.create_conversation(
                recipients=[u["id"] for u in batch],
                subject=args.subject,
                body=template,
                course_id=args.course_id,
                group_conversation=args.group_conversation,
                force_new=True,
                mode=args.mode,
            )
        append_sent_log(args.sent_log, batch, args.course_id, args.subject)
        print(f"Sent/logged batch of {len(batch)}")

    print("Done.")
    return 0

# It parses arguments, creates a client, and dispatches to the appropriate command function.
def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        client = make_client()
        if args.command == "courses":
            return cmd_courses(client)
        if args.command == "users":
            return cmd_users(client, args)
        if args.command == "send":
            return cmd_send(client, args)
        parser.error("Unknown command")
        return 2
    except (CanvasAPIError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
