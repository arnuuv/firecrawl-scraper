#!/usr/bin/env python3
"""
Main entry point for the VC Form Filling AI Agent

This module provides a command-line interface for the form filling agent
and handles the main application logic.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, List

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from loguru import logger

from vc_form_agent import FormFillingAgent
from vc_form_agent.utils.data_manager import DataManager
from vc_form_agent.templates.ycombinator import YCombinatorTemplate


console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    VC Form Filling AI Agent
    
    An intelligent AI agent that automatically fills out Venture Capital application forms.
    """
    pass


@cli.command()
@click.option("--url", "-u", required=True, help="URL of the form to fill")
@click.option("--template", "-t", help="Template to use for form filling")
@click.option("--headless", is_flag=True, default=True, help="Run browser in headless mode")
@click.option("--browser", "-b", default="chrome", help="Browser to use (chrome, firefox, edge, playwright)")
@click.option("--screenshot", is_flag=True, default=True, help="Take screenshot after completion")
@click.option("--validate", is_flag=True, default=True, help="Validate form before submission")
@click.option("--auto-navigate", is_flag=True, default=True, help="Automatically find and click apply links")
@click.option("--file-uploads", "-f", multiple=True, help="File uploads in format 'field_name:file_path'")
def fill_form(url: str, template: Optional[str], headless: bool, browser: str, screenshot: bool, 
              validate: bool, auto_navigate: bool, file_uploads: tuple):
    """Fill out a single form."""
    # Parse file uploads
    file_upload_dict = {}
    for upload in file_uploads:
        if ':' in upload:
            field_name, file_path = upload.split(':', 1)
            file_upload_dict[field_name] = file_path
        else:
            console.print(f"[red]Invalid file upload format: {upload}. Use 'field_name:file_path'[/red]")
            return
    
    asyncio.run(_fill_form_async(url, template, headless, browser, screenshot, validate, 
                                auto_navigate, file_upload_dict))


@cli.command()
@click.option("--url", "-u", required=True, help="URL of the main page")
@click.option("--template", "-t", help="Template to use for form filling")
@click.option("--headless", is_flag=True, default=True, help="Run browser in headless mode")
@click.option("--browser", "-b", default="chrome", help="Browser to use")
@click.option("--file-uploads", "-f", multiple=True, help="File uploads in format 'field_name:file_path'")
@click.option("--apply-links", "-a", multiple=True, help="Custom apply link texts to look for")
def navigate_and_fill(url: str, template: Optional[str], headless: bool, browser: str, 
                     file_uploads: tuple, apply_links: tuple):
    """Navigate to a main page, find apply link, and fill the form."""
    # Parse file uploads
    file_upload_dict = {}
    for upload in file_uploads:
        if ':' in upload:
            field_name, file_path = upload.split(':', 1)
            file_upload_dict[field_name] = file_path
        else:
            console.print(f"[red]Invalid file upload format: {upload}. Use 'field_name:file_path'[/red]")
            return
    
    asyncio.run(_navigate_and_fill_async(url, template, headless, browser, file_upload_dict, list(apply_links)))


@cli.command()
@click.option("--csv-file", "-f", required=True, help="CSV file with list of VC URLs")
@click.option("--template", "-t", help="Template to use for all forms")
@click.option("--delay", "-d", default=30, help="Delay between forms in seconds")
@click.option("--headless", is_flag=True, default=True, help="Run browser in headless mode")
@click.option("--browser", "-b", default="chrome", help="Browser to use")
@click.option("--file-uploads", "-u", multiple=True, help="File uploads in format 'field_name:file_path'")
@click.option("--auto-navigate", is_flag=True, default=True, help="Automatically navigate to apply pages")
def batch_process(csv_file: str, template: Optional[str], delay: int, headless: bool, browser: str,
                 file_uploads: tuple, auto_navigate: bool):
    """Process multiple forms in batch."""
    # Parse file uploads
    file_upload_dict = {}
    for upload in file_uploads:
        if ':' in upload:
            field_name, file_path = upload.split(':', 1)
            file_upload_dict[field_name] = file_path
        else:
            console.print(f"[red]Invalid file upload format: {upload}. Use 'field_name:file_path'[/red]")
            return
    
    asyncio.run(_batch_process_async(csv_file, template, delay, headless, browser, file_upload_dict, auto_navigate))


@cli.command()
@click.option("--name", "-n", required=True, help="Company name")
@click.option("--industry", "-i", required=True, help="Industry/sector")
@click.option("--founding-date", "-d", required=True, help="Founding date (YYYY-MM-DD)")
@click.option("--team-size", "-t", required=True, type=int, help="Team size")
@click.option("--funding-stage", "-s", required=True, help="Funding stage")
@click.option("--email", "-e", required=True, help="Contact email")
@click.option("--website", "-w", help="Company website")
@click.option("--revenue", "-r", type=float, help="Annual revenue")
@click.option("--growth-rate", "-g", type=float, help="Growth rate percentage")
def setup_company(name: str, industry: str, founding_date: str, team_size: int, 
                  funding_stage: str, email: str, website: Optional[str], 
                  revenue: Optional[float], growth_rate: Optional[float]):
    """Set up company profile."""
    _setup_company_profile(name, industry, founding_date, team_size, funding_stage, 
                          email, website, revenue, growth_rate)


@cli.command()
@click.option("--name", "-n", required=True, help="VC firm name")
@click.option("--website", "-w", required=True, help="VC firm website")
@click.option("--application-url", "-u", required=True, help="Application form URL")
@click.option("--focus-areas", "-f", help="Focus areas (comma-separated)")
@click.option("--investment-stages", "-s", help="Investment stages (comma-separated)")
@click.option("--check-size", "-c", help="Typical check size")
def add_vc(name: str, website: str, application_url: str, focus_areas: Optional[str],
           investment_stages: Optional[str], check_size: Optional[str]):
    """Add a VC firm to the database."""
    _add_vc_firm(name, website, application_url, focus_areas, investment_stages, check_size)


@cli.command()
def list_vcs():
    """List all VC firms in the database."""
    _list_vc_firms()


@cli.command()
def show_profile():
    """Show current company profile."""
    _show_company_profile()


@cli.command()
@click.option("--focus-areas", "-f", help="Filter by focus areas (comma-separated)")
@click.option("--stages", "-s", help="Filter by investment stages (comma-separated)")
def search_vcs(focus_areas: Optional[str], stages: Optional[str]):
    """Search VC firms by criteria."""
    _search_vc_firms(focus_areas, stages)


@cli.command()
def list_templates():
    """List available form templates."""
    _list_templates()


@cli.command()
@click.option("--url", "-u", required=True, help="URL to test")
@click.option("--headless", is_flag=True, default=False, help="Run in headless mode")
def test_navigation(url: str, headless: bool):
    """Test navigation and apply link detection."""
    asyncio.run(_test_navigation_async(url, headless))


async def _fill_form_async(url: str, template: Optional[str], headless: bool, 
                          browser: str, screenshot: bool, validate: bool, 
                          auto_navigate: bool, file_uploads: dict):
    """Async wrapper for filling a single form."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Initializing form filling agent...", total=None)
            
            # Initialize agent
            agent = FormFillingAgent(
                headless=headless,
                browser_type=browser
            )
            
            progress.update(task, description="Filling form...")
            
            # Fill the form
            result = await agent.fill_form(
                url=url,
                template_name=template,
                file_uploads=file_uploads if file_uploads else None,
                validate_before_submit=validate,
                take_screenshot=screenshot,
                auto_navigate_to_apply=auto_navigate
            )
            
            # Display results
            _display_form_result(result)
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        logger.error(f"Error filling form: {str(e)}")
        sys.exit(1)


async def _navigate_and_fill_async(url: str, template: Optional[str], headless: bool, 
                                  browser: str, file_uploads: dict, apply_links: list):
    """Async wrapper for navigate and fill."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Initializing agent...", total=None)
            
            # Initialize agent
            agent = FormFillingAgent(
                headless=headless,
                browser_type=browser
            )
            
            progress.update(task, description="Navigating and filling form...")
            
            # Navigate and fill
            result = await agent.navigate_and_fill_form(
                main_url=url,
                template_name=template,
                file_uploads=file_uploads if file_uploads else None,
                apply_link_texts=apply_links if apply_links else None
            )
            
            # Display results
            _display_form_result(result)
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        logger.error(f"Error in navigate and fill: {str(e)}")
        sys.exit(1)


async def _batch_process_async(csv_file: str, template: Optional[str], delay: int, 
                              headless: bool, browser: str, file_uploads: dict, auto_navigate: bool):
    """Async wrapper for batch processing."""
    try:
        # Read URLs from CSV
        urls = _read_urls_from_csv(csv_file)
        
        if not urls:
            console.print("[red]No URLs found in CSV file[/red]")
            return
        
        console.print(f"[green]Processing {len(urls)} forms...[/green]")
        
        # Initialize agent
        agent = FormFillingAgent(
            headless=headless,
            browser_type=browser
        )
        
        # Process forms
        results = await agent.batch_process(
            urls=urls,
            template_name=template,
            file_uploads=file_uploads if file_uploads else None,
            delay_between_forms=delay,
            auto_navigate=auto_navigate
        )
        
        # Display batch results
        _display_batch_results(results)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        logger.error(f"Error in batch processing: {str(e)}")
        sys.exit(1)


async def _test_navigation_async(url: str, headless: bool):
    """Test navigation and apply link detection."""
    try:
        from vc_form_agent.core.browser import BrowserManager
        
        console.print(f"[blue]Testing navigation to: {url}[/blue]")
        
        # Initialize browser
        browser = BrowserManager(headless=headless)
        await browser.start()
        
        try:
            # Navigate to URL
            await browser.navigate(url)
            await browser.wait_for_page_load()
            
            console.print("[green]✓ Successfully navigated to page[/green]")
            
            # Try to find apply link
            apply_found = await browser.find_and_click_apply_link()
            
            if apply_found:
                console.print("[green]✓ Found and clicked apply link[/green]")
                await browser.wait_for_page_load()
                
                # Take screenshot
                screenshot_path = await browser.take_screenshot("navigation_test.png")
                console.print(f"[green]✓ Screenshot saved: {screenshot_path}[/green]")
                
                # Get current URL
                current_url = browser.selenium_driver.current_url if browser.selenium_driver else url
                console.print(f"[blue]Current URL: {current_url}[/blue]")
            else:
                console.print("[yellow]⚠ No apply link found on the page[/yellow]")
                
        finally:
            await browser.close()
            
    except Exception as e:
        console.print(f"[red]Error testing navigation: {str(e)}[/red]")
        logger.error(f"Error testing navigation: {str(e)}")


def _setup_company_profile(name: str, industry: str, founding_date: str, team_size: int,
                          funding_stage: str, email: str, website: Optional[str],
                          revenue: Optional[float], growth_rate: Optional[float]):
    """Set up company profile."""
    try:
        data_manager = DataManager()
        
        profile_data = {
            "company_name": name,
            "industry": industry,
            "founding_date": founding_date,
            "team_size": team_size,
            "funding_stage": funding_stage,
            "email": email,
            "website": website,
            "revenue": revenue,
            "growth_rate": growth_rate,
            "target_market": "To be defined",
            "competitive_advantage": "To be defined",
            "use_of_funds": "To be defined"
        }
        
        # Remove None values
        profile_data = {k: v for k, v in profile_data.items() if v is not None}
        
        data_manager.update_company_profile(profile_data)
        
        console.print("[green]Company profile updated successfully![/green]")
        _show_company_profile()
        
    except Exception as e:
        console.print(f"[red]Error setting up company profile: {str(e)}[/red]")
        logger.error(f"Error setting up company profile: {str(e)}")


def _add_vc_firm(name: str, website: str, application_url: str, focus_areas: Optional[str],
                 investment_stages: Optional[str], check_size: Optional[str]):
    """Add a VC firm to the database."""
    try:
        from vc_form_agent.utils.data_manager import VCFirm
        
        # Parse comma-separated values
        focus_areas_list = [area.strip() for area in focus_areas.split(",")] if focus_areas else []
        stages_list = [stage.strip() for stage in investment_stages.split(",")] if investment_stages else []
        
        vc_firm = VCFirm(
            name=name,
            website=website,
            application_url=application_url,
            focus_areas=focus_areas_list,
            investment_stages=stages_list,
            check_size=check_size or "Not specified"
        )
        
        data_manager = DataManager()
        data_manager.add_vc_firm(vc_firm)
        
        console.print(f"[green]Added VC firm: {name}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error adding VC firm: {str(e)}[/red]")
        logger.error(f"Error adding VC firm: {str(e)}")


def _list_vc_firms():
    """List all VC firms in the database."""
    try:
        data_manager = DataManager()
        vc_firms = data_manager.load_vc_database()
        
        if not vc_firms:
            console.print("[yellow]No VC firms found in database[/yellow]")
            return
        
        table = Table(title="VC Firms Database")
        table.add_column("Name", style="cyan")
        table.add_column("Website", style="blue")
        table.add_column("Focus Areas", style="green")
        table.add_column("Stages", style="yellow")
        table.add_column("Check Size", style="magenta")
        
        for vc in vc_firms:
            table.add_row(
                vc.get("name", ""),
                vc.get("website", ""),
                ", ".join(vc.get("focus_areas", [])),
                ", ".join(vc.get("investment_stages", [])),
                vc.get("check_size", "")
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error listing VC firms: {str(e)}[/red]")
        logger.error(f"Error listing VC firms: {str(e)}")


def _show_company_profile():
    """Show current company profile."""
    try:
        data_manager = DataManager()
        profile = data_manager.load_company_profile()
        
        if not profile:
            console.print("[yellow]No company profile found[/yellow]")
            return
        
        table = Table(title="Company Profile")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        for field, value in profile.items():
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            elif isinstance(value, dict):
                value = str(value)
            table.add_row(field.replace("_", " ").title(), str(value))
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error showing company profile: {str(e)}[/red]")
        logger.error(f"Error showing company profile: {str(e)}")


def _search_vc_firms(focus_areas: Optional[str], stages: Optional[str]):
    """Search VC firms by criteria."""
    try:
        data_manager = DataManager()
        
        focus_areas_list = [area.strip() for area in focus_areas.split(",")] if focus_areas else None
        stages_list = [stage.strip() for stage in stages.split(",")] if stages else None
        
        results = data_manager.search_vc_firms(
            focus_areas=focus_areas_list,
            investment_stages=stages_list
        )
        
        if not results:
            console.print("[yellow]No VC firms found matching criteria[/yellow]")
            return
        
        table = Table(title=f"Search Results ({len(results)} firms)")
        table.add_column("Name", style="cyan")
        table.add_column("Website", style="blue")
        table.add_column("Focus Areas", style="green")
        table.add_column("Stages", style="yellow")
        
        for vc in results:
            table.add_row(
                vc.get("name", ""),
                vc.get("website", ""),
                ", ".join(vc.get("focus_areas", [])),
                ", ".join(vc.get("investment_stages", []))
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error searching VC firms: {str(e)}[/red]")
        logger.error(f"Error searching VC firms: {str(e)}")


def _list_templates():
    """List available form templates."""
    try:
        data_manager = DataManager()
        templates = data_manager.list_templates()
        
        if not templates:
            console.print("[yellow]No templates found[/yellow]")
            return
        
        table = Table(title="Available Templates")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="green")
        
        for template_name in templates:
            template = data_manager.get_template(template_name)
            if template:
                table.add_row(template_name, template.description)
            else:
                table.add_row(template_name, "No description available")
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error listing templates: {str(e)}[/red]")
        logger.error(f"Error listing templates: {str(e)}")


def _read_urls_from_csv(csv_file: str) -> List[str]:
    """Read URLs from CSV file."""
    try:
        import csv
        urls = []
        
        with open(csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'url' in row and row['url']:
                    urls.append(row['url'])
                elif 'application_url' in row and row['application_url']:
                    urls.append(row['application_url'])
        
        return urls
        
    except Exception as e:
        console.print(f"[red]Error reading CSV file: {str(e)}[/red]")
        logger.error(f"Error reading CSV file: {str(e)}")
        return []


def _display_form_result(result):
    """Display form filling result."""
    console.print("\n" + "="*50)
    console.print("FORM FILLING RESULT")
    console.print("="*50)
    
    if result.success:
        console.print(f"[green]✅ SUCCESS[/green]")
    else:
        console.print(f"[red]❌ FAILED[/red]")
    
    console.print(f"URL: {result.url}")
    console.print(f"Fields Filled: {result.fields_filled}/{result.total_fields}")
    console.print(f"Completion Time: {result.completion_time:.2f} seconds")
    
    if result.files_uploaded:
        console.print(f"Files Uploaded: {len(result.files_uploaded)}")
        for file_path in result.files_uploaded:
            console.print(f"  • {file_path}")
    
    if result.screenshot_path:
        console.print(f"Screenshot: {result.screenshot_path}")
    
    if result.errors:
        console.print("\n[red]Errors:[/red]")
        for error in result.errors:
            console.print(f"  • {error}")
    
    if result.warnings:
        console.print("\n[yellow]Warnings:[/yellow]")
        for warning in result.warnings:
            console.print(f"  • {warning}")


def _display_batch_results(results):
    """Display batch processing results."""
    console.print("\n" + "="*50)
    console.print("BATCH PROCESSING RESULTS")
    console.print("="*50)
    
    successful = sum(1 for r in results if r.success)
    total = len(results)
    
    console.print(f"Total Forms: {total}")
    console.print(f"Successful: {successful}")
    console.print(f"Failed: {total - successful}")
    console.print(f"Success Rate: {(successful/total)*100:.1f}%")
    
    # Count total files uploaded
    total_files = sum(len(r.files_uploaded or []) for r in results)
    if total_files > 0:
        console.print(f"Total Files Uploaded: {total_files}")
    
    if successful < total:
        console.print("\n[red]Failed Forms:[/red]")
        for i, result in enumerate(results):
            if not result.success:
                console.print(f"  {i+1}. {result.url} - {', '.join(result.errors)}")


if __name__ == "__main__":
    cli() 