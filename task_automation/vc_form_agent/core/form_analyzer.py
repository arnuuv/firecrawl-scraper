"""
Form Analyzer

Analyzes web forms to detect and understand form fields using AI and web scraping.
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from loguru import logger
from bs4 import BeautifulSoup
from pydantic import BaseModel

from ..utils.ai_helper import AIHelper


@dataclass
class FieldContext:
    """Context information about a form field."""
    label: str
    placeholder: str
    description: str
    required: bool
    field_type: str
    options: List[str] = None


class FormField(BaseModel):
    """Represents a detected form field."""
    name: str
    type: str
    label: str
    required: bool
    value: Optional[str] = None
    options: Optional[List[str]] = None
    xpath: Optional[str] = None
    css_selector: Optional[str] = None
    context: Optional[FieldContext] = None


class FormAnalyzer:
    """
    Analyzes web forms to detect and understand form fields.
    """
    
    def __init__(self, ai_helper: Optional[AIHelper] = None):
        """
        Initialize the form analyzer.
        
        Args:
            ai_helper: AI helper instance for field analysis
        """
        self.ai_helper = ai_helper or AIHelper()
        
        # Common field patterns
        self.field_patterns = {
            "company_name": [
                r"company\s*name",
                r"business\s*name",
                r"organization\s*name",
                r"startup\s*name"
            ],
            "industry": [
                r"industry",
                r"sector",
                r"business\s*type",
                r"market\s*segment"
            ],
            "funding_stage": [
                r"funding\s*stage",
                r"investment\s*stage",
                r"round",
                r"capital\s*stage"
            ],
            "team_size": [
                r"team\s*size",
                r"employees",
                r"headcount",
                r"staff\s*size"
            ],
            "revenue": [
                r"revenue",
                r"annual\s*revenue",
                r"monthly\s*revenue",
                r"sales"
            ],
            "description": [
                r"description",
                r"about",
                r"overview",
                r"summary",
                r"pitch"
            ],
            "use_of_funds": [
                r"use\s*of\s*funds",
                r"funding\s*purpose",
                r"investment\s*use",
                r"capital\s*allocation"
            ]
        }
    
    async def analyze_form(self, browser_manager) -> List[FormField]:
        """
        Analyze a form to detect all fields.
        
        Args:
            browser_manager: Browser manager instance
            
        Returns:
            List of detected form fields
        """
        try:
            # Get page source
            page_source = await browser_manager.get_page_source()
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find all form elements
            forms = soup.find_all('form')
            if not forms:
                logger.warning("No forms found on the page")
                return []
            
            all_fields = []
            
            for form in forms:
                fields = await self._analyze_form_element(form, browser_manager)
                all_fields.extend(fields)
            
            # Use AI to enhance field understanding
            enhanced_fields = await self._enhance_fields_with_ai(all_fields, page_source)
            
            logger.info(f"Analyzed {len(enhanced_fields)} form fields")
            return enhanced_fields
            
        except Exception as e:
            logger.error(f"Error analyzing form: {str(e)}")
            return []
    
    async def _analyze_form_element(self, form_element, browser_manager) -> List[FormField]:
        """
        Analyze a specific form element.
        
        Args:
            form_element: BeautifulSoup form element
            browser_manager: Browser manager instance
            
        Returns:
            List of form fields in this form
        """
        fields = []
        
        # Find all input elements
        inputs = form_element.find_all(['input', 'textarea', 'select'])
        
        for input_elem in inputs:
            try:
                field = await self._extract_field_info(input_elem, browser_manager)
                if field:
                    fields.append(field)
            except Exception as e:
                logger.warning(f"Error extracting field info: {str(e)}")
                continue
        
        return fields
    
    async def _extract_field_info(self, input_elem, browser_manager) -> Optional[FormField]:
        """
        Extract information from an input element.
        
        Args:
            input_elem: BeautifulSoup input element
            browser_manager: Browser manager instance
            
        Returns:
            FormField object if valid, None otherwise
        """
        # Get basic attributes
        field_name = input_elem.get('name') or input_elem.get('id') or ''
        field_type = input_elem.get('type', 'text')
        field_id = input_elem.get('id', '')
        
        if not field_name and not field_id:
            return None
        
        # Determine if required
        required = (
            input_elem.get('required') is not None or
            'required' in input_elem.get('class', []) or
            '*' in str(input_elem.find_parent())
        )
        
        # Get label
        label = await self._find_label(input_elem, browser_manager)
        
        # Get placeholder
        placeholder = input_elem.get('placeholder', '')
        
        # Get options for select elements
        options = None
        if input_elem.name == 'select':
            options = [
                option.get('value', option.text.strip())
                for option in input_elem.find_all('option')
                if option.get('value') or option.text.strip()
            ]
        
        # Create field context
        context = FieldContext(
            label=label,
            placeholder=placeholder,
            description='',
            required=required,
            field_type=field_type,
            options=options
        )
        
        # Generate CSS selector
        css_selector = self._generate_css_selector(input_elem)
        
        return FormField(
            name=field_name,
            type=field_type,
            label=label,
            required=required,
            options=options,
            css_selector=css_selector,
            context=context
        )
    
    async def _find_label(self, input_elem, browser_manager) -> str:
        """
        Find the label for an input element.
        
        Args:
            input_elem: BeautifulSoup input element
            browser_manager: Browser manager instance
            
        Returns:
            Label text
        """
        # Method 1: Check for 'for' attribute
        field_id = input_elem.get('id')
        if field_id:
            label_elem = input_elem.find_parent().find('label', attrs={'for': field_id})
            if label_elem:
                return label_elem.get_text(strip=True)
        
        # Method 2: Check for nested label
        parent = input_elem.find_parent()
        if parent:
            label_elem = parent.find('label')
            if label_elem:
                return label_elem.get_text(strip=True)
        
        # Method 3: Check for aria-label
        aria_label = input_elem.get('aria-label')
        if aria_label:
            return aria_label
        
        # Method 4: Check for title attribute
        title = input_elem.get('title')
        if title:
            return title
        
        # Method 5: Use placeholder as fallback
        placeholder = input_elem.get('placeholder')
        if placeholder:
            return placeholder
        
        return ""
    
    def _generate_css_selector(self, element) -> str:
        """
        Generate a CSS selector for an element.
        
        Args:
            element: BeautifulSoup element
            
        Returns:
            CSS selector string
        """
        selectors = []
        
        # Add tag name
        selectors.append(element.name)
        
        # Add ID if present
        if element.get('id'):
            selectors.append(f"#{element['id']}")
        
        # Add name if present
        if element.get('name'):
            selectors.append(f"[name='{element['name']}']")
        
        # Add type if present
        if element.get('type'):
            selectors.append(f"[type='{element['type']}']")
        
        return ''.join(selectors)
    
    async def _enhance_fields_with_ai(self, fields: List[FormField], page_source: str) -> List[FormField]:
        """
        Use AI to enhance field understanding.
        
        Args:
            fields: List of detected fields
            page_source: Full page source
            
        Returns:
            Enhanced list of fields
        """
        try:
            # Prepare field data for AI analysis
            field_data = []
            for field in fields:
                field_data.append({
                    "name": field.name,
                    "label": field.label,
                    "placeholder": field.context.placeholder if field.context else "",
                    "type": field.type,
                    "required": field.required
                })
            
            # Use AI to analyze fields
            ai_analysis = await self.ai_helper.analyze_form_fields(field_data, page_source)
            
            # Apply AI insights
            for i, field in enumerate(fields):
                if i < len(ai_analysis):
                    analysis = ai_analysis[i]
                    
                    # Update field with AI insights
                    if analysis.get('suggested_name'):
                        field.name = analysis['suggested_name']
                    
                    if analysis.get('category'):
                        field.context.description = analysis['category']
                    
                    if analysis.get('confidence'):
                        field.context.description += f" (AI confidence: {analysis['confidence']}%)"
            
            return fields
            
        except Exception as e:
            logger.warning(f"AI enhancement failed: {str(e)}")
            return fields
    
    def categorize_field(self, field: FormField) -> str:
        """
        Categorize a field based on its properties.
        
        Args:
            field: FormField object
            
        Returns:
            Category string
        """
        field_text = f"{field.name} {field.label} {field.context.placeholder if field.context else ''}".lower()
        
        for category, patterns in self.field_patterns.items():
            for pattern in patterns:
                if re.search(pattern, field_text, re.IGNORECASE):
                    return category
        
        return "other"
    
    def get_field_mapping_suggestions(self, fields: List[FormField]) -> Dict[str, str]:
        """
        Get suggestions for mapping fields to company data.
        
        Args:
            fields: List of form fields
            
        Returns:
            Dictionary mapping field names to suggested data keys
        """
        suggestions = {}
        
        for field in fields:
            category = self.categorize_field(field)
            if category != "other":
                suggestions[field.name] = category
        
        return suggestions
    
    def validate_form_completeness(self, fields: List[FormField], filled_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Validate if all required fields are filled.
        
        Args:
            fields: List of form fields
            filled_data: Dictionary of filled data
            
        Returns:
            Validation result
        """
        missing_required = []
        filled_count = 0
        total_required = 0
        
        for field in fields:
            if field.required:
                total_required += 1
                if field.name not in filled_data or not filled_data[field.name]:
                    missing_required.append(field.name)
                else:
                    filled_count += 1
        
        return {
            "complete": len(missing_required) == 0,
            "filled_required": filled_count,
            "total_required": total_required,
            "missing_required": missing_required,
            "completion_percentage": (filled_count / total_required * 100) if total_required > 0 else 100
        } 