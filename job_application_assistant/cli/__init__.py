"""Command-line interface for job application assistant."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from job_application_assistant.core.config import Settings
from job_application_assistant.core.llm import get_llm_manager
from job_application_assistant.core.logging import setup_logging
from job_application_assistant.core.exceptions import JobAssistantError

app = typer.Typer(
    name="job-assistant",
    help="AI-powered job application and interview preparation assistant",
    add_completion=False,
)
console = Console()

# Global settings
settings = Settings()


@app.callback()
def main(
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging"),
    log_file: Optional[Path] = typer.Option(None, "--log-file", help="Log file path"),
):
    """Job Application Assistant CLI."""
    # Setup logging
    log_level = "DEBUG" if debug else "INFO"
    setup_logging(level=log_level, log_file=log_file)


@app.command()
def status():
    """Show system status and model information."""
    try:
        console.print("🔍 [bold blue]Job Application Assistant Status[/bold blue]")
        console.print()
        
        # Get system status
        status_info = settings.get_system_status()
        
        # Create status table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details")
        
        # Ollama status
        ollama_status = "✅ Available" if status_info["ollama_available"] else "❌ Not Available"
        table.add_row("Ollama", ollama_status, status_info["ollama_url"])
        
        # Models
        available_models = status_info["available_models"]
        if available_models:
            models_text = ", ".join(available_models[:3])
            if len(available_models) > 3:
                models_text += f" (+{len(available_models) - 3} more)"
            table.add_row("Models", f"✅ {len(available_models)} available", models_text)
        else:
            table.add_row("Models", "❌ None available", "Run 'ollama pull <model>' to download")
        
        # Primary model
        primary_model = status_info["primary_model"]
        primary_status = "✅ Available" if primary_model in available_models else "❌ Not available"
        table.add_row("Primary Model", primary_status, primary_model)
        
        console.print(table)
        console.print()
        
        # Directories
        console.print("📁 [bold blue]Data Directories[/bold blue]")
        console.print(f"Data: {status_info['data_directory']}")
        console.print(f"Logs: {status_info['logs_directory']}")
        
    except Exception as e:
        console.print(f"❌ Error getting status: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def models():
    """List available and recommended models."""
    try:
        console.print("🤖 [bold blue]Available Models[/bold blue]")
        console.print()
        
        available = settings.get_available_models()
        
        if not available:
            console.print("❌ No models available. Download models with:")
            console.print("   ollama pull llama3.1:8b")
            console.print("   ollama pull gemma2:9b")
            return
        
        # Create models table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Model", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Recommended Use")
        
        for model in available:
            if "llama3.1" in model:
                model_type = "Primary"
                use_case = "General applications, excellent quality"
            elif "gemma" in model:
                model_type = "Fallback"
                use_case = "Creative writing, good quality"
            elif "qwen" in model:
                model_type = "Fallback"
                use_case = "Technical content, multilingual"
            else:
                model_type = "Other"
                use_case = "Various use cases"
            
            # Mark current primary model
            if model == settings.primary_model_name:
                model = f"⭐ {model}"
                model_type = f"{model_type} (Active)"
            
            table.add_row(model, model_type, use_case)
        
        console.print(table)
        console.print()
        console.print("💡 [bold yellow]Recommendations:[/bold yellow]")
        console.print("• For 8GB RAM: llama3.1:8b + gemma2:9b")
        console.print("• For 16GB+ RAM: llama3.1:70b")
        console.print("• For 4GB RAM: phi3:mini")
        
    except Exception as e:
        console.print(f"❌ Error listing models: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def web(
    host: str = typer.Option("localhost", "--host", help="Host to bind to"),
    port: int = typer.Option(8501, "--port", help="Port to bind to"),
):
    """Start the web interface."""
    try:
        console.print("🌐 [bold blue]Starting Web Interface[/bold blue]")
        console.print(f"Host: {host}")
        console.print(f"Port: {port}")
        console.print()
        
        # Import and run Streamlit
        import subprocess
        import sys
        
        app_path = Path(__file__).parent.parent / "web" / "app.py"
        cmd = [
            sys.executable, "-m", "streamlit", "run", str(app_path),
            "--server.address", host,
            "--server.port", str(port),
            "--server.headless", "true",
        ]
        
        console.print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        console.print("\n👋 Web interface stopped")
    except Exception as e:
        console.print(f"❌ Error starting web interface: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def apply(
    job_url: Optional[str] = typer.Option(None, "--job-url", help="Job posting URL"),
    job_file: Optional[Path] = typer.Option(None, "--job-file", help="Job description file"),
    cv_file: Optional[Path] = typer.Option(None, "--cv-file", help="CV/resume file"),
    output_dir: Path = typer.Option(Path.cwd(), "--output", help="Output directory"),
):
    """Generate job application materials."""
    async def _apply():
        try:
            console.print("📝 [bold blue]Generating Application Materials[/bold blue]")
            console.print()
            
            if not job_url and not job_file:
                console.print("❌ Please provide either --job-url or --job-file", style="red")
                raise typer.Exit(1)
            
            # Initialize LLM manager
            llm_manager = get_llm_manager()
            await llm_manager.initialize()
            
            console.print("✅ LLM initialized")
            
            # TODO: Implement job application generation
            console.print("🚧 Application generation coming soon!")
            
        except JobAssistantError as e:
            console.print(f"❌ Job Assistant Error: {e.message}", style="red")
            if e.details:
                console.print(f"Details: {e.details}", style="yellow")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"❌ Unexpected error: {e}", style="red")
            raise typer.Exit(1)
    
    asyncio.run(_apply())


@app.command()
def interview(
    company: str = typer.Argument(help="Company name"),
    role: str = typer.Argument(help="Job role/title"),
    output_dir: Path = typer.Option(Path.cwd(), "--output", help="Output directory"),
):
    """Generate interview preparation materials."""
    async def _interview():
        try:
            console.print("🎤 [bold blue]Generating Interview Preparation[/bold blue]")
            console.print(f"Company: {company}")
            console.print(f"Role: {role}")
            console.print()
            
            # Initialize LLM manager
            llm_manager = get_llm_manager()
            await llm_manager.initialize()
            
            console.print("✅ LLM initialized")
            
            # TODO: Implement interview preparation generation
            console.print("🚧 Interview preparation coming soon!")
            
        except JobAssistantError as e:
            console.print(f"❌ Job Assistant Error: {e.message}", style="red")
            if e.details:
                console.print(f"Details: {e.details}", style="yellow")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"❌ Unexpected error: {e}", style="red")
            raise typer.Exit(1)
    
    asyncio.run(_interview())


if __name__ == "__main__":
    app()
