"""Main CLI application for the Job Application Assistant."""

import asyncio
import sys
from pathlib import Path
from typing import Optional
import logging

try:
    import typer
    from rich.console import Console
    from rich.prompt import Confirm, Prompt, IntPrompt
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("Required packages not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)

from job_application_assistant.core.config import get_settings
from job_application_assistant.models.data_models import JobDescription, UserProfile, UserPreferences
from job_application_assistant.agents.job_application_agent import JobApplicationAgent
from job_application_assistant.agents.interview_prep_agent import InterviewPreparationAgent
from job_application_assistant.tools.document_processor import process_cv_file, extract_job_description
from job_application_assistant.utils.streamlit_helpers import get_model_info

# Initialize components
app = typer.Typer(help="Job Application & Interview Preparation Assistant")
console = Console()
settings = get_settings()

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def display_welcome():
    """Display welcome message and system info."""
    welcome_text = """
    # 🚀 Job Application & Interview Assistant
    
    **Powered by Local AI Models**
    
    This assistant helps you:
    - ✨ Create personalized cover letters and motivation letters
    - 📋 Prepare comprehensive interview materials  
    - 🎯 Generate targeted application content
    - 💡 Get mock interview questions and study plans
    
    **Currently using:** {model} via Ollama
    """.format(model=settings.ollama_model)
    
    console.print(Panel(Markdown(welcome_text), title="Welcome", border_style="blue"))


def collect_user_profile() -> UserProfile:
    """Collect user profile information."""
    console.print("\n[bold blue]📝 Let's set up your profile[/bold blue]\n")
    
    name = Prompt.ask("Your full name")
    email = Prompt.ask("Your email address")
    phone = Prompt.ask("Your phone number", default="")
    
    # CV/Resume processing
    cv_text = ""
    has_cv = Confirm.ask("Do you have a CV/resume file to upload?")
    
    if has_cv:
        cv_path = Prompt.ask("Enter the path to your CV/resume file")
        try:
            user_profile = process_cv_file(cv_path)
            user_profile.name = name
            user_profile.email = email
            if phone:
                user_profile.phone = phone
            console.print("[green]✅ CV processed successfully![/green]")
            return user_profile
        except Exception as e:
            console.print(f"[red]❌ Error processing CV: {e}[/red]")
            console.print("Let's continue with manual input...")
    
    # Manual input
    skills_input = Prompt.ask("List your key skills (comma-separated)")
    skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
    
    cv_text = Prompt.ask("Brief summary of your experience and background")
    
    return UserProfile(
        name=name,
        email=email,
        phone=phone or None,
        cv_text=cv_text,
        skills=skills,
        experience=[],
        education=[]
    )


def collect_job_description() -> JobDescription:
    """Collect job description information."""
    console.print("\n[bold blue]🎯 Tell me about the job[/bold blue]\n")
    
    source_type = Prompt.ask(
        "How would you like to provide the job description?",
        choices=["url", "text", "manual"],
        default="text"
    )
    
    if source_type == "url":
        url = Prompt.ask("Enter the job posting URL")
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Extracting job description...", total=1)
                job_desc = extract_job_description(url)
                progress.update(task, completed=1)
            
            console.print("[green]✅ Job description extracted![/green]")
            return job_desc
        except Exception as e:
            console.print(f"[red]❌ Error extracting job description: {e}[/red]")
            console.print("Let's try manual input...")
    
    elif source_type == "text":
        console.print("Paste the full job description (press Enter twice when done):")
        lines = []
        empty_count = 0
        while empty_count < 2:
            line = input()
            if line:
                lines.append(line)
                empty_count = 0
            else:
                empty_count += 1
        
        job_text = "\n".join(lines)
        return extract_job_description(job_text)
    
    # Manual input
    title = Prompt.ask("Job title")
    company = Prompt.ask("Company name")
    description = Prompt.ask("Job description")
    requirements = Prompt.ask("Key requirements (comma-separated)", default="")
    skills = Prompt.ask("Required skills (comma-separated)", default="")
    location = Prompt.ask("Location", default="")
    
    return JobDescription(
        title=title,
        company=company,
        description=description,
        requirements=[req.strip() for req in requirements.split(",") if req.strip()],
        skills=[skill.strip() for skill in skills.split(",") if skill.strip()],
        location=location or None
    )


def collect_user_preferences(job_desc: JobDescription) -> UserPreferences:
    """Collect user preferences about the job."""
    console.print(f"\n[bold blue]💭 Tell me about your interest in this {job_desc.title} role at {job_desc.company}[/bold blue]\n")
    
    interest_level = IntPrompt.ask(
        "On a scale of 1-10, how interested are you in this role?",
        choices=[str(i) for i in range(1, 11)]
    )
    
    motivation = Prompt.ask("What excites you most about this opportunity?")
    
    relevant_experience = Prompt.ask(
        "What's your most relevant experience for this role? (Be specific with examples)"
    )
    
    career_goals = Prompt.ask("How does this role fit with your career goals?")
    
    company_knowledge = Prompt.ask(
        f"What do you know about {job_desc.company}? What attracts you to them?"
    )
    
    concerns = Prompt.ask("Any concerns or questions about the role?", default="")
    
    additional_info = Prompt.ask(
        "Anything else you'd like to highlight in your application?",
        default=""
    )
    
    return UserPreferences(
        job_interest_level=interest_level,
        motivation=motivation,
        relevant_experience=relevant_experience,
        career_goals=career_goals,
        company_knowledge=company_knowledge,
        concerns=concerns or None,
        additional_info=additional_info or None
    )


async def run_job_application_workflow(
    job_desc: JobDescription,
    user_profile: UserProfile,
    user_preferences: UserPreferences
):
    """Run the job application workflow."""
    console.print("\n[bold green]🚀 Generating your application materials...[/bold green]\n")
    
    agent = JobApplicationAgent()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Processing application...", total=1)
        
        result = await agent.process_application(
            job_description=job_desc,
            user_profile=user_profile,
            user_preferences=user_preferences
        )
        
        progress.update(task, completed=1)
    
    if result.get("error"):
        console.print(f"[red]❌ Error: {result['error']}[/red]")
        return
    
    # Display generated documents
    for doc in result.get("generated_documents", []):
        console.print(Panel(
            doc.content,
            title=f"📄 {doc.title}",
            border_style="green"
        ))
        console.print()
    
    # Save documents
    save_docs = Confirm.ask("Would you like to save these documents to files?")
    if save_docs:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        for doc in result.get("generated_documents", []):
            filename = f"{doc.document_type}_{job_desc.company}_{job_desc.title}.txt"
            filename = "".join(c for c in filename if c.isalnum() or c in "._- ")
            
            file_path = output_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc.content)
            
            console.print(f"[green]✅ Saved: {file_path}[/green]")


async def run_interview_preparation(
    job_desc: JobDescription,
    user_profile: UserProfile
):
    """Run the interview preparation workflow."""
    console.print("\n[bold blue]🎯 Preparing your interview materials...[/bold blue]\n")
    
    agent = InterviewPreparationAgent()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Generating interview prep...", total=1)
        
        result = await agent.prepare_for_interview(
            job_description=job_desc,
            user_profile=user_profile
        )
        
        progress.update(task, completed=1)
    
    if result.get("error"):
        console.print(f"[red]❌ Error: {result['error']}[/red]")
        return
    
    prep = result.get("interview_prep")
    if not prep:
        console.print("[red]❌ No interview preparation materials generated[/red]")
        return
    
    # Display preparation materials
    console.print(Panel(
        "\n".join(f"• {item}" for item in prep.confidence_checklist),
        title="🎯 Confidence Checklist - Master These Topics",
        border_style="blue"
    ))
    
    console.print(Panel(
        "\n".join(f"• {q}" for q in prep.technical_questions),
        title="⚙️ Technical Questions to Practice",
        border_style="yellow"
    ))
    
    console.print(Panel(
        "\n".join(f"• {q}" for q in prep.behavioral_questions),
        title="🗣️ Behavioral Questions (Use STAR Method)",
        border_style="magenta"
    ))
    
    console.print(Panel(
        "\n".join(f"• {q}" for q in prep.questions_to_ask),
        title="❓ Questions to Ask the Interviewer",
        border_style="cyan"
    ))


@app.command()
def apply(
    job_url: Optional[str] = typer.Option(None, help="Job posting URL"),
    cv_path: Optional[str] = typer.Option(None, help="Path to CV/resume file")
):
    """Create a job application with personalized documents."""
    display_welcome()
    
    try:
        # Collect information
        user_profile = collect_user_profile()
        job_desc = collect_job_description()
        user_preferences = collect_user_preferences(job_desc)
        
        # Run application workflow
        asyncio.run(run_job_application_workflow(
            job_desc, user_profile, user_preferences
        ))
        
        # Ask about interview preparation
        prep_interview = Confirm.ask("\nWould you like to prepare for the interview?")
        if prep_interview:
            asyncio.run(run_interview_preparation(job_desc, user_profile))
        
        console.print("\n[bold green]🎉 All done! Good luck with your application![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Application cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error: {e}[/red]")
        logger.exception("Unexpected error in apply command")


@app.command()
def interview(
    job_url: Optional[str] = typer.Option(None, help="Job posting URL"),
    cv_path: Optional[str] = typer.Option(None, help="Path to CV/resume file")
):
    """Prepare for a job interview."""
    display_welcome()
    
    try:
        user_profile = collect_user_profile()
        job_desc = collect_job_description()
        
        asyncio.run(run_interview_preparation(job_desc, user_profile))
        
        console.print("\n[bold green]🎉 Interview preparation complete! You've got this![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Interview prep cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error: {e}[/red]")
        logger.exception("Unexpected error in interview command")


@app.command()
def info():
    """Display system information."""
    model_info = get_model_info()
    
    info_text = f"""
    **System Information**
    
    - **Model:** {model_info['model']}
    - **Provider:** {model_info['provider']}
    - **Base URL:** {model_info['base_url']}
    - **Debug Mode:** {settings.debug}
    - **Log Level:** {settings.log_level}
    """
    
    console.print(Panel(Markdown(info_text), title="System Info", border_style="blue"))


if __name__ == "__main__":
    app()
