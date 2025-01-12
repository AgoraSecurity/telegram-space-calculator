import asyncio

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import IntPrompt
from rich.table import Table

from .telegram_client import TelegramAnalyzer

console = Console()


def format_size(size_bytes):
    """Convert bytes to human readable format"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0


def display_analysis_results(group_name, result):
    """Display the analysis results in a formatted panel"""
    total_files = sum(result["media_count"].values())

    details = [
        f"[bold green]Total Storage Required:[/] {format_size(result['total_size'])}",
        f"[bold blue]Total Files:[/] {total_files}",
        "\n[bold yellow]Media Breakdown:[/]",
    ]

    for media_type, count in result["media_count"].items():
        if count > 0:
            percentage = (count / total_files * 100) if total_files > 0 else 0
            details.append(f"• {media_type.title()}: {count} ({percentage:.1f}%)")

    console.print(
        Panel(
            "\n".join(details),
            title=f"Analysis Results for {group_name}",
            border_style="green",
        )
    )


async def main():
    try:
        analyzer = TelegramAnalyzer()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Connect to Telegram
            progress.add_task(description="Connecting to Telegram...", total=None)
            await analyzer.connect()

            # Fetch groups
            progress.add_task(description="Fetching groups...", total=None)
            groups = await analyzer.get_groups()

        if not groups:
            console.print("[red]No groups found![/]")
            return

        while True:
            # Display groups table
            table = Table(title="Your Telegram Groups")
            table.add_column("Index", justify="right", style="cyan", no_wrap=True)
            table.add_column("Name", style="green")
            table.add_column("Type", justify="center", style="magenta")
            table.add_column("Members", justify="right", style="yellow")

            for idx, group in enumerate(groups, 1):
                table.add_row(
                    str(idx), group["name"], group["type"], str(group["members_count"])
                )

            console.clear()
            console.print(table)
            console.print("\n[bold cyan]Options:[/]")
            console.print("• Enter a number to analyze a group")
            console.print("• Enter 0 to exit")
            console.print("• Enter -1 to refresh groups list")

            try:
                selection = IntPrompt.ask("\nEnter your choice", default=0)

                if selection == 0:
                    break
                elif selection == -1:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                    ) as progress:
                        progress.add_task(
                            description="Refreshing groups...", total=None
                        )
                        groups = await analyzer.get_groups()
                    continue
                elif 1 <= selection <= len(groups):
                    group = groups[selection - 1]

                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=console,
                    ) as progress:
                        progress.add_task(
                            description=f"Analyzing {group['name']}...", total=None
                        )
                        result = await analyzer.analyze_group_media(group["id"])

                    display_analysis_results(group["name"], result)

                    # Ask if user wants to analyze another group
                    if (
                        not console.input("\nPress Enter to continue or 'q' to quit: ")
                        .lower()
                        .startswith("q")
                    ):
                        continue
                    break
                else:
                    console.print("[red]Invalid selection. Please try again.[/]")
                    await asyncio.sleep(1)
            except ValueError:
                console.print("[red]Please enter a valid number.[/]")
                await asyncio.sleep(1)

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/]")
    finally:
        if hasattr(analyzer, "client"):
            await analyzer.client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
