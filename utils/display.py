"""
utils/display.py — PySec Suite v2.0
All rich-based formatting lives here. No module imports rich directly.
"""

import sys
import io
import pyfiglet
from rich.console import Console

# Force UTF-8 output on Windows so Unicode symbols (✔ ✘ ⚠) render correctly
if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
)

console = Console(legacy_windows=False, highlight=False)


def print_banner():
    """Render pyfiglet banner with slant font and subtitle."""
    banner = pyfiglet.figlet_format("PySec Suite", font="slant")
    console.print(f"[bold cyan]{banner}[/bold cyan]", end="")
    console.print("[dim]  v2.0 | Security Toolkit | Educational Use Only[/dim]\n")


def print_menu(options: dict):
    """Render numbered tool selection menu.

    Args:
        options: dict mapping key (str) to label (str), e.g. {"1": "Port Scanner", "0": "Exit"}
    """
    console.print("\n  [bold cyan]Select a tool:[/bold cyan]\n")
    for key, label in options.items():
        console.print(f"  [[bold white]{key}[/bold white]]  {label}")
    console.print()


def print_tool_header(name: str):
    """Render a panel header for the active tool."""
    console.print(Panel(f"[bold cyan]{name}[/bold cyan]", expand=False))
    console.print()


def print_table(headers: list, rows: list, title: str = ""):
    """Render a rich table.

    Args:
        headers: list of column header strings
        rows: list of tuples/lists, one per row
        title: optional table title string
    """
    table = Table(title=f"[bold cyan]{title}[/bold cyan]" if title else "", show_header=True)
    for header in headers:
        table.add_column(f"[bold cyan]{header}[/bold cyan]")
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
    console.print(table)


def print_success(msg: str):
    """Print a green ✔ status line."""
    console.print(f"  [green]✔[/green]  {msg}")


def print_error(msg: str):
    """Print a red ✘ status line."""
    console.print(f"  [red]✘[/red]  {msg}")


def print_warning(msg: str):
    """Print a yellow ⚠ status line."""
    console.print(f"  [yellow]⚠[/yellow]  {msg}")


def print_summary(msg: str):
    """Print a dim summary/footer line."""
    console.print(f"\n  [dim]{msg}[/dim]")


def get_progress_bar(description: str = "Working...", total: int = 100) -> Progress:
    """Return a configured rich Progress instance.

    Usage:
        with get_progress_bar("Scanning", total=1024) as progress:
            task = progress.add_task("scan", total=1024)
            progress.advance(task)
    """
    return Progress(
        TextColumn("  [bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=40),
        MofNCompleteColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=False,
    )
