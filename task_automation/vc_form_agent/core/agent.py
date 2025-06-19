"""
Main AI Agent for Form Filling

This module contains the core FormFillingAgent class that orchestrates
the entire form filling process using AI and browser automation.
"""

import asyncio
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pydantic import BaseModel

from ..utils.ai_helper import AIHelper
from ..utils.data_manager import DataManager
from ..utils.validators import FormValidator
from .browser import BrowserManager
from .form_analyzer import FormAnalyzer


class FormField(BaseModel):
    """Represents a form field with its properties."""
    name: str
    type: str
    label: str
    required: bool
    value: Optional[str] = None
    options: Optional[List[str]] = None
    xpath: Optional[str] = None
    css_selector: Optional[str] = None


class FormFillingResult(BaseModel):
    """Result of form filling operation."""
    success: bool
    url: str
    fields_filled: int
    total_fields: int
    errors: List[str]
    warnings: List[str]
    screenshot_path: Optional[str] = None
    completion_time: float
    files_uploaded: List[str] = None


class FormFillingAgent:
    """
    Main AI agent for filling out VC application forms.
    
    This agent combines AI-powered form analysis with browser automation
    to intelligently fill out complex application forms.
    """
    
    def __init__(
        self,
        company_profile_path: Optional[str] = None,
        headless: bool = True,
        browser_type: str = "chrome",
        ai_model: str = "gpt-4",
        max_retries: int = 3
    ):
        """
        Initialize the form filling agent.
        
        Args:
            company_profile_path: Path to company profile JSON file
            headless: Whether to run browser in headless mode
            browser_type: Type of browser to use (chrome, firefox, edge)
            ai_model: OpenAI model to use for AI operations
            max_retries: Maximum number of retries for failed operations
        """
        self.console = Console()
        self.headless = headless
        self.browser_type = browser_type
        self.max_retries = max_retries
        
        # Initialize components
        self.data_manager = DataManager(company_profile_path)
        self.ai_helper = AIHelper(model=ai_model)
        self.browser = BrowserManager(
            headless=headless,
            browser_type=browser_type
        )
        self.form_analyzer = FormAnalyzer()
        self.validator = FormValidator()
        
        # Load company data
        self.company_data = self.data_manager.load_company_profile()
        
        logger.info(f"FormFillingAgent initialized with {browser_type} browser")
    
    async def fill_form(
        self,
        url: str,
        template_name: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        file_uploads: Optional[Dict[str, Union[str, Path, List[Union[str, Path]]]]] = None,
        validate_before_submit: bool = True,
        take_screenshot: bool = True,
        auto_navigate_to_apply: bool = True
    ) -> FormFillingResult:
        """
        Fill out a form at the given URL.
        
        Args:
            url: URL of the form to fill
            template_name: Name of template to use (optional)
            custom_fields: Custom field mappings (optional)
            file_uploads: Dictionary mapping field names to file paths for uploads
            validate_before_submit: Whether to validate form before submitting
            take_screenshot: Whether to take screenshot after completion
            auto_navigate_to_apply: Whether to automatically find and click apply links
            
        Returns:
            FormFillingResult with details of the operation
        """
        start_time = time.time()
        result = FormFillingResult(
            success=False,
            url=url,
            fields_filled=0,
            total_fields=0,
            errors=[],
            warnings=[],
            files_uploaded=[]
        )
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                
                # Step 1: Navigate to form
                task = progress.add_task("Navigating to form...", total=None)
                await self.browser.navigate(url)
                await self.browser.wait_for_page_load()
                progress.update(task, description="Form loaded successfully")
                
                # Step 2: Auto-navigate to apply page if needed
                if auto_navigate_to_apply:
                    task = progress.add_task("Looking for apply link...", total=None)
                    apply_clicked = await self.browser.find_and_click_apply_link()
                    if apply_clicked:
                        await self.browser.wait_for_page_load()
                        progress.update(task, description="Navigated to application form")
                    else:
                        progress.update(task, description="No apply link found, continuing with current page")
                
                # Step 3: Analyze form structure
                task = progress.add_task("Analyzing form structure...", total=None)
                form_fields = await self.form_analyzer.analyze_form(self.browser)
                result.total_fields = len(form_fields)
                progress.update(task, description=f"Found {len(form_fields)} form fields")
                
                # Step 4: Map fields to company data
                task = progress.add_task("Mapping fields to company data...", total=None)
                field_mappings = await self._map_fields_to_data(
                    form_fields, template_name, custom_fields
                )
                progress.update(task, description="Field mapping completed")
                
                # Step 5: Fill form fields
                task = progress.add_task("Filling form fields...", total=len(field_mappings))
                filled_count = await self._fill_form_fields(field_mappings, progress, task)
                result.fields_filled = filled_count
                
                # Step 6: Upload files
                if file_uploads:
                    task = progress.add_task("Uploading files...", total=len(file_uploads))
                    uploaded_files = await self._upload_files(file_uploads, progress, task)
                    result.files_uploaded = uploaded_files
                
                # Step 7: Validate form (optional)
                if validate_before_submit:
                    task = progress.add_task("Validating form...", total=None)
                    validation_result = await self.validator.validate_form(
                        self.browser, field_mappings
                    )
                    result.errors.extend(validation_result.errors)
                    result.warnings.extend(validation_result.warnings)
                    progress.update(task, description="Validation completed")
                
                # Step 8: Take screenshot (optional)
                if take_screenshot:
                    task = progress.add_task("Taking screenshot...", total=None)
                    screenshot_path = await self.browser.take_screenshot()
                    result.screenshot_path = screenshot_path
                    progress.update(task, description="Screenshot saved")
                
                result.success = len(result.errors) == 0
                
        except Exception as e:
            logger.error(f"Error filling form: {str(e)}")
            result.errors.append(str(e))
            result.success = False
        
        finally:
            result.completion_time = time.time() - start_time
            await self.browser.close()
        
        return result
    
    async def _map_fields_to_data(
        self,
        form_fields: List[FormField],
        template_name: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Map form fields to company data using AI.
        
        Args:
            form_fields: List of detected form fields
            template_name: Optional template name
            custom_fields: Optional custom field mappings
            
        Returns:
            Dictionary mapping field names to values
        """
        # Start with custom fields if provided
        field_mappings = custom_fields or {}
        
        # Use template if specified
        if template_name:
            template_mappings = self.data_manager.get_template_mappings(template_name)
            field_mappings.update(template_mappings)
        
        # Use AI to map remaining fields
        unmapped_fields = [
            field for field in form_fields 
            if field.name not in field_mappings
        ]
        
        if unmapped_fields:
            ai_mappings = await self.ai_helper.map_fields_to_data(
                unmapped_fields, self.company_data
            )
            field_mappings.update(ai_mappings)
        
        return field_mappings
    
    async def _fill_form_fields(
        self,
        field_mappings: Dict[str, str],
        progress: Progress,
        task_id: int
    ) -> int:
        """
        Fill form fields with mapped data.
        
        Args:
            field_mappings: Dictionary of field names to values
            progress: Progress bar instance
            task_id: Task ID for progress updates
            
        Returns:
            Number of fields successfully filled
        """
        filled_count = 0
        
        for field_name, value in field_mappings.items():
            try:
                # Find the field element
                field_element = await self.browser.find_field(field_name)
                if not field_element:
                    logger.warning(f"Field '{field_name}' not found")
                    continue
                
                # Fill the field
                await self.browser.fill_field(field_element, value)
                filled_count += 1
                
                # Add small delay to avoid detection
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error filling field '{field_name}': {str(e)}")
            
            progress.update(task_id, advance=1)
        
        return filled_count
    
    async def _upload_files(
        self,
        file_uploads: Dict[str, Union[str, Path, List[Union[str, Path]]]],
        progress: Progress,
        task_id: int
    ) -> List[str]:
        """
        Upload files to form fields.
        
        Args:
            file_uploads: Dictionary mapping field names to file paths
            progress: Progress bar instance
            task_id: Task ID for progress updates
            
        Returns:
            List of successfully uploaded files
        """
        uploaded_files = []
        
        for field_name, file_paths in file_uploads.items():
            try:
                # Handle single file or list of files
                if isinstance(file_paths, (str, Path)):
                    file_paths = [file_paths]
                
                # Upload files
                success = await self.browser.upload_multiple_files(field_name, file_paths)
                if success:
                    uploaded_files.extend([str(fp) for fp in file_paths])
                    logger.info(f"Successfully uploaded {len(file_paths)} files to field '{field_name}'")
                else:
                    logger.error(f"Failed to upload files to field '{field_name}'")
                
            except Exception as e:
                logger.error(f"Error uploading files to field '{field_name}': {str(e)}")
            
            progress.update(task_id, advance=1)
        
        return uploaded_files
    
    async def navigate_and_fill_form(
        self,
        main_url: str,
        template_name: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        file_uploads: Optional[Dict[str, Union[str, Path, List[Union[str, Path]]]]] = None,
        apply_link_texts: Optional[List[str]] = None
    ) -> FormFillingResult:
        """
        Navigate to a main page, find the apply link, and fill the form.
        
        Args:
            main_url: URL of the main page
            template_name: Name of template to use
            custom_fields: Custom field mappings
            file_uploads: File uploads configuration
            apply_link_texts: Custom list of apply link texts to look for
            
        Returns:
            FormFillingResult with details of the operation
        """
        try:
            # Navigate to main page
            await self.browser.navigate(main_url)
            await self.browser.wait_for_page_load()
            
            # Find and click apply link
            apply_clicked = await self.browser.find_and_click_apply_link(apply_link_texts)
            if not apply_clicked:
                return FormFillingResult(
                    success=False,
                    url=main_url,
                    fields_filled=0,
                    total_fields=0,
                    errors=["Could not find apply link on the page"],
                    warnings=[],
                    files_uploaded=[]
                )
            
            # Wait for application form to load
            await self.browser.wait_for_page_load()
            
            # Get current URL (should be the application form)
            current_url = self.browser.selenium_driver.current_url if self.browser.selenium_driver else main_url
            
            # Fill the form
            return await self.fill_form(
                url=current_url,
                template_name=template_name,
                custom_fields=custom_fields,
                file_uploads=file_uploads,
                auto_navigate_to_apply=False  # Already navigated
            )
            
        except Exception as e:
            logger.error(f"Error in navigate_and_fill_form: {str(e)}")
            return FormFillingResult(
                success=False,
                url=main_url,
                fields_filled=0,
                total_fields=0,
                errors=[str(e)],
                warnings=[],
                files_uploaded=[]
            )
    
    async def batch_process(
        self,
        urls: List[str],
        template_name: Optional[str] = None,
        file_uploads: Optional[Dict[str, Union[str, Path, List[Union[str, Path]]]]] = None,
        delay_between_forms: int = 30,
        auto_navigate: bool = True
    ) -> List[FormFillingResult]:
        """
        Process multiple forms in batch.
        
        Args:
            urls: List of form URLs to process
            template_name: Template to use for all forms
            file_uploads: File uploads configuration
            delay_between_forms: Delay between forms in seconds
            auto_navigate: Whether to auto-navigate to apply pages
            
        Returns:
            List of results for each form
        """
        results = []
        
        for i, url in enumerate(urls):
            logger.info(f"Processing form {i+1}/{len(urls)}: {url}")
            
            if auto_navigate:
                result = await self.navigate_and_fill_form(
                    url, template_name, file_uploads=file_uploads
                )
            else:
                result = await self.fill_form(
                    url, template_name, file_uploads=file_uploads
                )
            
            results.append(result)
            
            if result.success:
                logger.success(f"Successfully filled form at {url}")
            else:
                logger.error(f"Failed to fill form at {url}: {result.errors}")
            
            # Delay between forms to avoid rate limiting
            if i < len(urls) - 1:
                logger.info(f"Waiting {delay_between_forms} seconds before next form...")
                await asyncio.sleep(delay_between_forms)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the agent's performance."""
        return {
            "company_name": self.company_data.get("company_name"),
            "browser_type": self.browser_type,
            "headless_mode": self.headless,
            "ai_model": self.ai_helper.model,
            "max_retries": self.max_retries
        } 