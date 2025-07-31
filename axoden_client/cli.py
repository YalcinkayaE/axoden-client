"""
AxoDen CLI - Command line interface for Claude Code users
"""

import os
import sys
import json
import click
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from pathlib import Path

from .client import AxoDenClient
from .config import AxoDenConfig
from .exceptions import AxoDenError, AuthenticationError


console = Console()


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="0.1.0", prog_name="axoden")
def main(ctx):
    """AxoDen - AI-powered development guidance for Claude Code
    
    Get intelligent development guidance for your challenges,
    optimized for use with Claude Code.
    
    Examples:
        axoden recommend "debug memory leak in production"
        axoden analyze
        axoden config --api-key YOUR_API_KEY
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.argument("problem", required=True)
@click.option("--context", "-c", help="Project context as JSON")
@click.option("--format", "-f", type=click.Choice(["claude", "json"]), default="claude",
              help="Output format (claude for Claude Code, json for raw)")
@click.option("--save", "-s", is_flag=True, help="Save recommendation to file")
def recommend(problem: str, context: Optional[str], format: str, save: bool):
    """Get methodology recommendation for a specific problem
    
    PROBLEM: Description of your development challenge
    
    Examples:
        axoden recommend "optimize database queries"
        axoden recommend "fix flaky tests" --context '{"language": "python"}'
    """
    try:
        client = AxoDenClient()
        
        # Parse context if provided
        project_context = None
        if context:
            try:
                project_context = json.loads(context)
            except json.JSONDecodeError:
                console.print("[red]Error: Invalid JSON in context parameter[/red]")
                sys.exit(1)
        
        # Show loading indicator
        with console.status("[bold green]Consulting AxoDen's methodology database..."):
            recommendation = client.recommend(problem, project_context, format)
        
        # Display recommendation
        if format == "claude":
            # Rich formatted output for Claude Code
            console.print(Panel(
                Markdown(recommendation.format_for_claude_code()),
                title=f"[bold blue]AxoDen Methodology Recommendation[/bold blue]",
                border_style="blue"
            ))
            
            if save:
                filename = f"axoden_recommendation_{recommendation.timestamp.strftime('%Y%m%d_%H%M%S')}.md"
                with open(filename, "w") as f:
                    f.write(recommendation.format_for_claude_code())
                console.print(f"\n[green]✅ Saved to {filename}[/green]")
                
        else:
            # JSON output
            output = json.dumps(recommendation.to_json(), indent=2)
            console.print(output)
            
            if save:
                filename = f"axoden_recommendation_{recommendation.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, "w") as f:
                    f.write(output)
                console.print(f"\n[green]✅ Saved to {filename}[/green]")
                
    except AuthenticationError as e:
        console.print(f"[red]Authentication Error: {e}[/red]")
        console.print("\nRun 'axoden config --api-key YOUR_KEY' to set up authentication")
        sys.exit(1)
    except AxoDenError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.option("--path", "-p", default=".", help="Project path to analyze")
def analyze(path: str):
    """Analyze current project and get methodology recommendations"""
    try:
        client = AxoDenClient()
        
        console.print(f"[bold]Analyzing project at: {os.path.abspath(path)}[/bold]\n")
        
        with console.status("[bold green]Analyzing project structure..."):
            analysis = client.analyze_project(path)
        
        # Display project context
        context_table = Table(title="Project Context", show_header=True)
        context_table.add_column("Property", style="cyan")
        context_table.add_column("Value", style="green")
        
        for key, value in analysis["project_context"].items():
            context_table.add_row(key.replace("_", " ").title(), str(value))
        
        console.print(context_table)
        console.print()
        
        # Display recommendations
        console.print("[bold]Recommended Methodologies:[/bold]")
        for method in analysis["recommended_methodologies"]:
            console.print(f"  • {method}")
        
        console.print(f"\n[dim]Confidence: {analysis['confidence']:.0%}[/dim]")
        
    except AxoDenError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.option("--api-key", help="Set AxoDen API key (or use AXODEN_API_KEY env var)")
@click.option("--base-url", help="Set API base URL")
@click.option("--show", is_flag=True, help="Show current configuration")
@click.option("--test", is_flag=True, help="Test API connection")
def config(api_key: Optional[str], base_url: Optional[str], show: bool, test: bool):
    """Configure AxoDen client settings"""
    config = AxoDenConfig()
    
    if show:
        # Show current configuration
        config_table = Table(title="AxoDen Configuration", show_header=True)
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="green")
        
        config_table.add_row("API Key", f"{'*' * 20}...{config.api_key[-4:]}" if config.api_key else "Not set")
        config_table.add_row("Base URL", config.base_url)
        config_table.add_row("Agent ID", config.agent_id or "Auto-generated")
        config_table.add_row("Config File", str(config.config_file))
        
        console.print(config_table)
        return
    
    if api_key:
        # If API key looks like it might be a file path or env var reference
        if api_key.startswith('$') or api_key.startswith('~') or '/' in api_key:
            console.print("[yellow]⚠️  This looks like a file path or env var. Use the actual API key value.[/yellow]")
            console.print("[yellow]If you meant to use an environment variable, just set it:[/yellow]")
            console.print("[bold]export AXODEN_API_KEY='your_actual_key'[/bold]")
            return
        
        if len(api_key) < 10:
            console.print("[red]❌ API key seems too short. Please check and try again.[/red]")
            return
            
        config.save_api_key(api_key)
        console.print(f"[green]✅ API key saved securely ({len(api_key)} characters)[/green]")
    
    if base_url:
        config.base_url = base_url
        config.save()
        console.print(f"[green]✅ Base URL updated to: {base_url}[/green]")
    
    if test:
        # Test API connection
        console.print("\n[bold]Testing API connection...[/bold]")
        try:
            client = AxoDenClient()
            # Test with simple API call
            with console.status("[bold green]Connecting to AxoDen API..."):
                response = client.session.get(f"{client.base_url}/health")
                
            if response.status_code == 200:
                console.print("[green]✅ API connection successful![/green]")
                health_data = response.json()
                console.print(f"[dim]Status: {health_data.get('status', 'Unknown')}[/dim]")
            else:
                console.print(f"[red]❌ API connection failed (HTTP {response.status_code})[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Connection error: {e}[/red]")


@main.command()
@click.option("--domain", "-d", help="Filter by domain")
def list(domain: Optional[str]):
    """List available methodologies"""
    try:
        client = AxoDenClient()
        
        with console.status("[bold green]Fetching methodologies..."):
            methodologies = client.list_methodologies(domain)
        
        # Display as table
        table = Table(title=f"Available Methodologies{f' ({domain})' if domain else ''}")
        table.add_column("Methodology", style="cyan")
        table.add_column("Domain", style="green")
        
        for method in methodologies:
            table.add_row(method["name"], method["domain"])
        
        console.print(table)
        
    except AxoDenError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command()
def setup_key():
    """Easy API key setup with multiple input options"""
    console.print(Panel(
        "[bold blue]AxoDen API Key Setup[/bold blue]\n\n"
        "Choose the best way to enter your API key:",
        border_style="blue"
    ))
    
    config = AxoDenConfig()
    
    console.print("\n[bold]Choose input method:[/bold]")
    console.print("1. 📋 Paste from clipboard (recommended)")
    console.print("2. ⌨️  Type manually (hidden)")
    console.print("3. 🔧 Set environment variable")
    console.print("4. 📄 Show current status")
    
    choice = click.prompt("\nSelect option (1-4)", type=click.Choice(['1', '2', '3', '4']))
    
    if choice == '1':
        console.print("\n[cyan]📋 Copy your API key to clipboard first, then press Enter...[/cyan]")
        click.pause()
        try:
            import subprocess
            if sys.platform == "darwin":  # macOS
                api_key = subprocess.check_output(["pbpaste"]).decode().strip()
            elif sys.platform == "linux":
                api_key = subprocess.check_output(["xclip", "-selection", "clipboard", "-o"]).decode().strip()
            elif sys.platform == "win32":
                api_key = subprocess.check_output(["powershell", "-command", "Get-Clipboard"]).decode().strip()
            else:
                raise Exception("Unsupported platform")
            
            if len(api_key) < 10:
                console.print("[red]❌ Clipboard content seems too short for an API key[/red]")
                return
                
            console.print(f"[green]✅ Got API key from clipboard ({len(api_key)} characters)[/green]")
            config.save_api_key(api_key)
            console.print("[green]🔐 API key saved securely![/green]")
            
        except Exception as e:
            console.print(f"[red]❌ Could not read from clipboard: {e}[/red]")
            console.print("[yellow]💡 Try option 2 (manual entry) or 3 (environment variable)[/yellow]")
            
    elif choice == '2':
        console.print("\n[yellow]⚠️  Characters will be hidden for security[/yellow]")
        api_key = click.prompt("Enter your API key", hide_input=True)
        if len(api_key) < 10:
            console.print("[red]❌ API key seems too short[/red]")
            return
        config.save_api_key(api_key)
        console.print(f"[green]✅ API key saved ({len(api_key)} characters)[/green]")
        
    elif choice == '3':
        console.print("\n[cyan]🔧 Environment Variable Setup:[/cyan]")
        console.print("Add this line to your shell profile:")
        console.print("[bold green]export AXODEN_API_KEY='your_api_key_here'[/bold green]")
        console.print("\n📁 Shell profile locations:")
        console.print("• macOS/Linux: ~/.bashrc or ~/.zshrc")
        console.print("• Windows: Use System Environment Variables")
        console.print("\n🔄 After adding it, restart your terminal or run:")
        console.print("[bold]source ~/.zshrc[/bold]")
        console.print("\n✨ Then run: [bold]axoden config --test[/bold]")
        
    else:  # choice == '4'
        if config.api_key:
            console.print(f"[green]✅ API key is configured ({len(config.api_key)} characters)[/green]")
            console.print(f"🔧 Base URL: {config.base_url}")
        else:
            console.print("[red]❌ No API key configured[/red]")
            console.print("Run this command again and choose option 1, 2, or 3")


@main.command()
def quickstart():
    """Interactive quickstart guide for new users"""
    console.print(Panel(
        "[bold blue]Welcome to AxoDen Client![/bold blue]\n\n"
        "Let's get you set up to use AI-powered methodology recommendations "
        "with Claude Code.",
        border_style="blue"
    ))
    
    # Check if API key is set
    config = AxoDenConfig()
    if not config.api_key:
        console.print("\n[yellow]First, you'll need an AxoDen API key.[/yellow]")
        console.print("Visit [link]https://axoden.com/beta[/link] to request access.\n")
        
        console.print("[bold]Choose how to enter your API key:[/bold]")
        console.print("1. Type it in (hidden)")
        console.print("2. Paste from clipboard")
        console.print("3. Set environment variable (recommended)")
        
        choice = click.prompt("\nSelect option (1-3)", type=click.Choice(['1', '2', '3']))
        
        if choice == '1':
            api_key = click.prompt("Enter your API key", hide_input=True)
        elif choice == '2':
            console.print("\n[cyan]Copy your API key to clipboard, then press Enter...[/cyan]")
            click.pause()
            try:
                import subprocess
                if sys.platform == "darwin":  # macOS
                    api_key = subprocess.check_output(["pbpaste"]).decode().strip()
                elif sys.platform == "linux":
                    api_key = subprocess.check_output(["xclip", "-selection", "clipboard", "-o"]).decode().strip()
                elif sys.platform == "win32":
                    api_key = subprocess.check_output(["powershell", "-command", "Get-Clipboard"]).decode().strip()
                else:
                    raise Exception("Unsupported platform")
                console.print(f"[green]✅ Got API key from clipboard ({len(api_key)} characters)[/green]")
            except Exception:
                console.print("[red]❌ Could not read from clipboard. Please use option 1 or 3.[/red]")
                api_key = click.prompt("Enter your API key", hide_input=True)
        else:  # choice == '3'
            console.print("\n[cyan]Add this to your shell profile (~/.bashrc, ~/.zshrc, etc.):[/cyan]")
            console.print("[bold]export AXODEN_API_KEY='your_api_key_here'[/bold]")
            console.print("\nThen restart your terminal or run: [bold]source ~/.zshrc[/bold]")
            console.print("\n[yellow]After setting the environment variable, run 'axoden quickstart' again.[/yellow]")
            return
        
        if api_key and len(api_key) > 10:  # Basic validation
            config.save_api_key(api_key)
            console.print("[green]✅ API key saved![/green]\n")
        else:
            console.print("[red]❌ Invalid API key. Please try again.[/red]")
            return
    
    # Show example usage
    console.print("[bold]Example Usage:[/bold]\n")
    
    examples = [
        ("Debug a problem", "axoden recommend \"fix memory leak in production API\""),
        ("Analyze project", "axoden analyze"),
        ("Get specific methodology", "axoden recommend \"optimize database queries\" --format json"),
    ]
    
    for title, command in examples:
        console.print(f"[cyan]{title}:[/cyan]")
        console.print(f"  $ {command}\n")
    
    console.print("[bold]Next Steps:[/bold]")
    console.print("1. Try the examples above")
    console.print("2. Use recommendations in your Claude Code sessions")
    console.print("3. Provide feedback to improve the system\n")
    
    console.print("[dim]For more help: axoden --help[/dim]")


if __name__ == "__main__":
    main()