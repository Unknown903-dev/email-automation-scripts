from __future__ import annotations

from pyfiglet import Figlet
from rich import box
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
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


def print_error(message: object) -> None:
    error_console.print("[bold red]Error:[/bold red]", Text(str(message)))
