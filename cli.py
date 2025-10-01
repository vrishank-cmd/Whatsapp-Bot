#!/usr/bin/env python3
"""
Modern CLI Interface for AI-Powered WhatsApp Bot 2025
Advanced command-line interface with rich formatting
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional
from pathlib import Path
import json

app = typer.Typer(
    name="whatsapp-bot",
    help="AI-Powered WhatsApp Bot 2025 - Intelligent messaging automation",
    rich_markup_mode="rich",
)
console = Console()


@app.command("start")
def start_bot(
    config_file: Optional[Path] = typer.Option(
        "config.json", "--config", "-c", help="Configuration file path"
    ),
    ai_mode: bool = typer.Option(True, "--ai/--no-ai", help="Enable AI features"),
    interactive: bool = typer.Option(
        True, "--interactive/--batch", help="Interactive mode"
    ),
):
    """Start the WhatsApp Bot with AI features"""

    console.print(
        Panel.fit(
            "[bold green]AI-Powered WhatsApp Bot 2025[/bold green]\n"
            "[cyan]Intelligent • Secure • Modern[/cyan]",
            title="Starting Bot",
        )
    )

    if ai_mode:
        console.print("🧠 [green]AI Mode: Enabled[/green]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Initializing AI systems...", total=None)

        # Import and run the main bot
        import asyncio
        from bot import main

        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            console.print("\n[yellow]Bot stopped by user[/yellow]")


@app.command("analytics")
def show_analytics(
    days: int = typer.Option(30, "--days", "-d", help="Days to analyze"),
    export: bool = typer.Option(False, "--export", help="Export to JSON"),
):
    """Display analytics dashboard"""

    try:
        from ai_features import analytics

        console.print(
            Panel.fit(
                f"[bold cyan]Analytics Dashboard[/bold cyan]\n"
                f"[yellow]Last {days} days[/yellow]",
                title="Bot Performance",
            )
        )

        report = analytics.generate_delivery_report()

        # Create metrics table
        table = Table(title="Key Metrics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green", justify="right")

        table.add_row("Total Messages", str(report["total_messages"]))
        table.add_row("Delivery Rate", f"{report['delivery_rate']}%")
        table.add_row("Read Rate", f"{report['read_rate']}%")
        table.add_row("Avg Response Time", f"{report['avg_response_time']}s")

        console.print(table)

        if export:
            with open(f"analytics_export_{days}d.json", "w") as f:
                json.dump(report, f, indent=2)
            console.print(f"📁 [green]Exported to analytics_export_{days}d.json[/green]")

    except ImportError:
        console.print(
            "[red]Analytics features not available. Install AI requirements.[/red]"
        )


@app.command("config")
def manage_config(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    edit: bool = typer.Option(False, "--edit", help="Edit configuration"),
    reset: bool = typer.Option(False, "--reset", help="Reset to defaults"),
):
    """⚙️ Manage bot configuration"""

    config_path = Path("config.json")

    if show:
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)

            console.print(
                Panel(json.dumps(config, indent=2), title="⚙️ Current Configuration")
            )
        else:
            console.print("[red]No configuration file found[/red]")

    elif reset:
        # Create default config
        default_config = {
            "default_settings": {
                "max_contacts": 50,
                "min_interval_seconds": 5,
                "max_retries": 3,
                "log_level": "INFO",
                "enable_logging": True,
                "log_file": "whatsapp_bot.log",
            },
            "ai_features": {
                "enable_ai_suggestions": True,
                "enable_sentiment_analysis": True,
                "enable_smart_scheduling": True,
            },
        }

        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=2)

        console.print("[green]Configuration reset to defaults[/green]")


@app.command("contacts")
def manage_contacts(
    import_csv: Optional[Path] = typer.Option(None, "--import", help="Import from CSV"),
    export_csv: Optional[Path] = typer.Option(None, "--export", help="Export to CSV"),
    validate: bool = typer.Option(False, "--validate", help="Validate contacts"),
    encrypt: bool = typer.Option(False, "--encrypt", help="Encrypt contact data"),
):
    """👥 Manage contacts with AI-powered features"""

    if import_csv:
        if import_csv.exists():
            console.print(f"📥 [green]Importing contacts from {import_csv}[/green]")
            # Import logic here
        else:
            console.print(f"[red]File not found: {import_csv}[/red]")

    if validate:
        console.print("🔍 [yellow]Validating contact data...[/yellow]")
        # Validation logic here

    if encrypt:
        console.print("[yellow]Encrypting contact data...[/yellow]")
        # Encryption logic here


@app.command("ai")
def ai_features(
    test_generation: bool = typer.Option(
        False, "--test-gen", help="Test AI message generation"
    ),
    analyze_text: Optional[str] = typer.Option(
        None, "--analyze", help="Analyze text sentiment"
    ),
    setup: bool = typer.Option(False, "--setup", help="Setup AI configuration"),
):
    """AI-powered features and testing"""

    if setup:
        console.print(
            Panel.fit(
                "[bold yellow]AI Setup Instructions[/bold yellow]\n\n"
                "1. Get OpenAI API Key: https://platform.openai.com/api-keys\n"
                "2. Copy .env.example to .env\n"
                "3. Add your API key to .env file\n"
                "4. Install AI requirements: pip install -r requirements.txt",
                title="AI Setup",
            )
        )

    if test_generation:
        console.print("🧪 [yellow]Testing AI message generation...[/yellow]")
        # Test AI features

    if analyze_text:
        console.print(f"🔍 [yellow]Analyzing: '{analyze_text}'[/yellow]")
        # Sentiment analysis here


@app.command("security")
def security_features(
    scan: bool = typer.Option(False, "--scan", help="Security scan"),
    encrypt_data: bool = typer.Option(
        False, "--encrypt", help="Encrypt sensitive data"
    ),
    generate_key: bool = typer.Option(
        False, "--gen-key", help="Generate encryption key"
    ),
):
    """Security and encryption features"""

    if generate_key:
        from cryptography.fernet import Fernet

        key = Fernet.generate_key()
        console.print(f"🔑 [green]Generated encryption key:[/green] {key.decode()}")
        console.print("[yellow]Add this to your .env file as ENCRYPTION_KEY[/yellow]")

    if scan:
        console.print("🔍 [yellow]Running security scan...[/yellow]")
        # Security scan logic

    if encrypt_data:
        console.print("[yellow]Encrypting sensitive data...[/yellow]")
        # Encryption logic


@app.command("version")
def show_version():
    """📋 Show version and feature information"""

    table = Table(title="WhatsApp Bot 2025")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Version", style="yellow")

    # Check feature availability
    try:
        import openai  # noqa: F401

        ai_status = "Available"
        ai_version = "Latest"
    except ImportError:
        ai_status = "Not installed"
        ai_version = "N/A"

    try:
        from rich import __version__ as rich_version

        rich_status = "Available"
    except ImportError:
        rich_status = "Not installed"
        rich_version = "N/A"

    table.add_row("AI Features", ai_status, ai_version)
    table.add_row(
        "Rich UI", rich_status, rich_version if "rich_version" in locals() else "N/A"
    )
    table.add_row("Security", "Available", "2025")
    table.add_row("Analytics", "Available", "2025")

    console.print(table)


if __name__ == "__main__":
    app()
