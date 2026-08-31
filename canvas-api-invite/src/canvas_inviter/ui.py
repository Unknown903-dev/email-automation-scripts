from __future__ import annotations

from pyfiglet import Figlet
from rich import box
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text


console = Console()
error_console = Console(stderr=True)


def print_help_screen() -> None:
    """Print a styled, non-interactive command summary."""
    logo = Figlet(font="small").renderText("QuickInvite").rstrip()
    console.print(Text(logo, style="bold yellow"))
    console.print("[bold magenta]Usage:[/bold magenta] " + escape("quickinvite [options]") + "\n")
    console.print(
        Panel(
            "[bold]Send Canvas course invitations quickly and safely[/bold]",
            border_style="green",
            box=box.ROUNDED,
            padding=(1, 3),
            expand=False,
        )
    )
    console.print("\n[bold]Options:[/bold]\n")
    options = Table(box=None, show_header=False, padding=(0, 2), collapse_padding=True)
    options.add_column(style="cyan", no_wrap=True)
    options.add_column()
    options.add_row("-c, --courses", "List Canvas courses")
    options.add_row("-u, --users <course_id>", "List users in a course")
    options.add_row("-s, --send", "Send an invitation")
    options.add_row("-p, --preview", "Preview an invitation")
    options.add_row("    --version", "Show version number")
    options.add_row("-h, --help", "Show help")
    console.print(options)


def _print_command(command: str) -> None:
    console.print(Syntax(command, "bash", theme="ansi_dark", word_wrap=True, padding=(0, 2)))


def print_detailed_help() -> None:
    """Print the complete, non-interactive QuickInvite user guide."""
    console.print("[bold yellow]QuickInvite[/bold yellow]")
    console.print("Fast, safe Canvas invitations from your terminal.\n")
    console.print("[bold magenta]Usage[/bold magenta]")
    _print_command("quickinvite [options]")
    console.print(
        Panel(
            "First configure your Canvas environment, then find a course, review its "
            "students, preview the invitation, and only then send it.",
            title="Getting Started",
            border_style="green",
        )
    )

    console.print("\n[bold cyan]1. Configure Your Environment[/bold cyan]")
    console.print("Create a [cyan].env[/cyan] file in the project directory containing:")
    console.print(
        Panel(
            Text(
                "CANVAS_BASE_URL=https://your-school.instructure.com\n"
                "CANVAS_TOKEN=your_canvas_access_token"
            ),
            expand=False,
        )
    )
    console.print("Treat CANVAS_TOKEN like a password; never commit or share it.")

    console.print("\n[bold cyan]2. Find Your Course[/bold cyan]")
    console.print("List the courses visible to your Canvas token:")
    _print_command("quickinvite --courses")

    console.print("\n[bold cyan]3. View Students[/bold cyan]")
    console.print("Use the course ID from the previous step. The default role is student:")
    _print_command("quickinvite --users <course_id>")

    console.print("\n[bold cyan]4. Preview[/bold cyan]")
    console.print("Render the invitation and review its recipients without sending anything:")
    _print_command(
        "quickinvite --preview \\\n"
        "    --course-id <id> \\\n"
        "    --subject \"<subject>\" \\\n"
        "    --message-file <path>"
    )

    console.print("\n[bold cyan]5. Send[/bold cyan]")
    console.print("After reviewing the preview, explicitly request the real Canvas send:")
    _print_command(
        "quickinvite --send \\\n"
        "    --course-id <id> \\\n"
        "    --subject \"<subject>\" \\\n"
        "    --message-file <path>"
    )

    console.print("\n[bold magenta]Options[/bold magenta]")
    options = Table(header_style="bold", box=box.SIMPLE)
    options.add_column("Option", style="cyan", no_wrap=True)
    options.add_column("Purpose")
    options.add_row("-c, --courses", "List courses visible to the configured Canvas token.")
    options.add_row("-u, --users <course_id>", "List active users in a course.")
    options.add_row("-p, --preview", "Run the send workflow as a dry-run preview.")
    options.add_row("-s, --send", "Explicitly perform the real Canvas send.")
    options.add_row("--version", "Show the installed QuickInvite version.")
    options.add_row("-h, --help", "Show this detailed guide.")
    console.print(options)

    console.print("\n[bold magenta]Send Options[/bold magenta]")
    send_options = Table(header_style="bold", box=box.SIMPLE)
    send_options.add_column("Option", style="cyan", no_wrap=True)
    send_options.add_column("Purpose")
    send_options.add_row("--course-id <id>", "Canvas course ID. Required.")
    send_options.add_row("--subject <text>", "Message subject. Required.")
    send_options.add_row("--message-file <path>", "Text file containing the message body. Required.")
    send_options.add_row(
        "--recipients-csv <path>",
        "Only include users matching id, name, sortable_name, login_id, or email values.",
    )
    send_options.add_row(
        "--role <role>",
        "Enrollment role: student, teacher, ta, observer, or designer (default: student).",
    )
    send_options.add_row(
        "--sent-log <path>",
        "CSV used to skip previously sent users (default: data/sent_log.csv).",
    )
    send_options.add_row("--batch-size <number>", "Recipients per Canvas request (default: 50).")
    send_options.add_row("--mode sync|async", "Canvas delivery mode (default: sync).")
    send_options.add_row(
        "--group-conversation", "Create one shared conversation; private messages are the default."
    )
    send_options.add_row("--no-dedupe", "Do not skip users already listed in the sent log.")
    send_options.add_row(
        "--send", "Confirmation flag used by the legacy 'quickinvite send' command."
    )
    console.print(send_options)

    console.print("\n[bold magenta]Message Templates[/bold magenta]")
    console.print("Message files may use these per-recipient placeholders:")
    console.print("[cyan]{{id}}  {{name}}  {{sortable_name}}  {{login_id}}  {{email}}[/cyan]")
    console.print("Example:")
    console.print(Panel(Text("Hi {{name}},\n\nYour invitation goes here."), expand=False))

    console.print("\n[bold magenta]Safety[/bold magenta]")
    console.print(
        "[bold yellow]Preview/dry-run does not send anything.[/bold yellow] "
        "A real message is sent only when you explicitly use [bold red]--send[/bold red]. "
        "Duplicate protection is enabled by default through the sent log."
    )

    console.print("\n[bold magenta]Quick Start[/bold magenta]")
    _print_command(
        "quickinvite --courses\n"
        "quickinvite --users 12345\n"
        "quickinvite --preview --course-id 12345 --subject \"Invitation\" "
        "--message-file message.txt\n"
        "quickinvite --send --course-id 12345 --subject \"Invitation\" "
        "--message-file message.txt"
    )


def print_error(message: object) -> None:
    error_console.print("[bold red]Error:[/bold red]", Text(str(message)))
