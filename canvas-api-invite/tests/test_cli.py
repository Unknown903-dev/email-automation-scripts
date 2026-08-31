from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import Mock, patch

from canvas_inviter.cli import cmd_send, main, normalize_option_command


class CLITests(unittest.TestCase):
    def test_no_arguments_and_help_do_not_create_client(self) -> None:
        with patch("canvas_inviter.cli.make_client") as make_client:
            self.assertEqual(main([]), 0)
            self.assertEqual(main(["--help"]), 0)
        make_client.assert_not_called()

    def test_simple_options_map_to_existing_commands(self) -> None:
        self.assertEqual(normalize_option_command(["--courses"]), ["courses"])
        self.assertEqual(
            normalize_option_command(["--users", "12345", "--role", "ta"]),
            ["users", "--course-id", "12345", "--role", "ta"],
        )
        self.assertEqual(
            normalize_option_command(["--preview", "--course-id", "12345"]),
            ["send", "--course-id", "12345"],
        )
        self.assertEqual(
            normalize_option_command(["--send", "--course-id", "12345"]),
            ["send", "--course-id", "12345", "--send"],
        )

    def test_dry_run_never_calls_send_endpoint(self) -> None:
        client = Mock()
        client.list_course_users.return_value = [{"id": 7, "name": "Test Student"}]

        with tempfile.TemporaryDirectory() as directory:
            message_file = Path(directory) / "message.txt"
            message_file.write_text("Hello {{name}}", encoding="utf-8")
            args = Namespace(
                course_id="12345",
                subject="Invitation",
                message_file=str(message_file),
                recipients_csv=None,
                role="student",
                sent_log=str(Path(directory) / "sent.csv"),
                batch_size=50,
                mode="sync",
                group_conversation=False,
                no_dedupe=False,
                send=False,
            )
            self.assertEqual(cmd_send(client, args), 0)

        client.create_conversation.assert_not_called()


if __name__ == "__main__":
    unittest.main()
