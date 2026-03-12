"""
main.py — PySec Suite v2.0
Entry point. Renders the banner, displays the tool menu, and routes
user selection to the correct module's run() function.

Each module exposes a single run() interface — main.py calls nothing else.
"""

from utils.display import console, print_banner, print_menu, print_summary

MENU_OPTIONS = {
    "1": "Subdomain Scanner",
    "2": "Directory Scanner",
    "3": "Network Scanner",
    "4": "Port Scanner",
    "5": "File Fetcher",
    "6": "Hash Cracker",
    "0": "Exit",
}


def _load_module(choice: str):
    """Lazy-import and return the selected module's run function."""
    if choice == "1":
        from modules.subdomain_scanner import run
    elif choice == "2":
        from modules.directory_scanner import run
    elif choice == "3":
        from modules.network_scanner import run
    elif choice == "4":
        from modules.port_scanner import run
    elif choice == "5":
        from modules.file_fetcher import run
    elif choice == "6":
        from modules.hash_cracker import run
    else:
        return None
    return run


def _post_tool_prompt() -> bool:
    """Ask the user whether to return to the menu or exit.

    Returns True to continue (return to menu), False to exit.
    """
    console.print("\n  [bold cyan]What next?[/bold cyan]")
    console.print("  [1]  Return to main menu")
    console.print("  [0]  Exit")
    while True:
        choice = console.input("  [bold white]>[/bold white] ").strip()
        if choice == "1":
            return True
        elif choice == "0":
            return False
        console.print("  [dim]Enter 1 to return to menu or 0 to exit.[/dim]")


def main():
    print_banner()

    while True:
        print_menu(MENU_OPTIONS)

        choice = console.input("  [bold white]>[/bold white] ").strip()

        if choice == "0":
            print_summary("Goodbye.")
            break

        run_func = _load_module(choice)
        if run_func is None:
            console.print("  [yellow]Invalid choice — enter a number from the menu.[/yellow]\n")
            continue

        console.print()
        try:
            run_func()
        except KeyboardInterrupt:
            console.print("\n\n  [yellow]Interrupted.[/yellow]")

        if not _post_tool_prompt():
            print_summary("Goodbye.")
            break

        console.print()


if __name__ == "__main__":
    main()
