"""
AI Helper for Form Analysis

Uses OpenAI API to analyze forms and intelligently map fields to company data.
"""

import json
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from loguru import logger
import openai
from pydantic import BaseModel

from .data_manager import DataManager


@dataclass
class FieldAnalysis:
    """Result of AI field analysis."""
    suggested_name: str
    category: str
    confidence: float
    description: str
    mapping_suggestion: str


class AIHelper:
    """
    Helper class for AI-powered form analysis and field mapping.
    """
    
    def __init__(
        self,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.1
    ):
        """
        Initialize AI helper.
        
        Args:
            model: OpenAI model to use
            api_key: OpenAI API key (will use env var if not provided)
            max_tokens: Maximum tokens for responses
            temperature: Temperature for AI responses
        """
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # Initialize OpenAI client
        if api_key:
            self.client = openai.AsyncOpenAI(api_key=api_key)
        else:
            self.client = openai.AsyncOpenAI()
        
        # Load company data for context
        self.data_manager = DataManager()
        self.company_data = self.data_manager.load_company_profile()
        
        logger.info(f"AI Helper initialized with model: {model}")
    
    async def analyze_form_fields(
        self,
        fields: List[Dict[str, Any]],
        page_source: str
    ) -> List[Dict[str, Any]]:
        """
        Analyze form fields using AI.
        
        Args:
            fields: List of field data
            page_source: HTML page source
            
        Returns:
            List of AI analysis results
        """
        try:
            # Prepare prompt for field analysis
            prompt = self._create_field_analysis_prompt(fields, page_source)
            
            # Get AI response
            response = await self._get_ai_response(prompt)
            
            # Parse response
            analysis = self._parse_field_analysis_response(response)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing form fields: {str(e)}")
            return []
    
    async def map_fields_to_data(
        self,
        fields: List[Dict[str, Any]],
        company_data: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Map form fields to company data using AI.
        
        Args:
            fields: List of form fields
            company_data: Company data dictionary
            
        Returns:
            Dictionary mapping field names to values
        """
        try:
            # Prepare prompt for field mapping
            prompt = self._create_field_mapping_prompt(fields, company_data)
            
            # Get AI response
            response = await self._get_ai_response(prompt)
            
            # Parse response
            mappings = self._parse_field_mapping_response(response)
            
            return mappings
            
        except Exception as e:
            logger.error(f"Error mapping fields to data: {str(e)}")
            return {}
    
    async def generate_field_value(
        self,
        field_name: str,
        field_type: str,
        context: str,
        company_data: Dict[str, Any]
    ) -> str:
        """
        Generate appropriate value for a field using AI.
        
        Args:
            field_name: Name of the field
            field_type: Type of the field
            context: Context about the field
            company_data: Company data
            
        Returns:
            Generated field value
        """
        try:
            prompt = self._create_value_generation_prompt(
                field_name, field_type, context, company_data
            )
            
            response = await self._get_ai_response(prompt)
            
            # Clean up response
            value = response.strip().strip('"').strip("'")
            
            return value
            
        except Exception as e:
            logger.error(f"Error generating field value: {str(e)}")
            return ""
    
    async def validate_form_data(
        self,
        form_data: Dict[str, str],
        form_context: str
    ) -> Dict[str, Any]:
        """
        Validate form data using AI.
        
        Args:
            form_data: Dictionary of form data
            form_context: Context about the form
            
        Returns:
            Validation result
        """
        try:
            prompt = self._create_validation_prompt(form_data, form_context)
            
            response = await self._get_ai_response(prompt)
            
            validation = self._parse_validation_response(response)
            
            return validation
            
        except Exception as e:
            logger.error(f"Error validating form data: {str(e)}")
            return {"valid": False, "errors": [str(e)]}
    
    def _create_field_analysis_prompt(
        self,
        fields: List[Dict[str, Any]],
        page_source: str
    ) -> str:
        """Create prompt for field analysis."""
        fields_json = json.dumps(fields, indent=2)
        
        return f"""
You are an expert at analyzing web forms for venture capital applications. Analyze the following form fields and provide insights about each field.

Form Fields:
{fields_json}

Page Context (HTML snippet):
{page_source[:2000]}...

For each field, provide:
1. suggested_name: A standardized name for the field
2. category: What type of data this field expects (company_info, financial, team, etc.)
3. confidence: Confidence level (0-100) in your categorization
4. description: Brief description of what this field is for
5. mapping_suggestion: Suggested key from company data that should fill this field

Respond with a JSON array of objects with these fields. Example:
[
  {{
    "suggested_name": "company_name",
    "category": "company_info",
    "confidence": 95,
    "description": "Official company name",
    "mapping_suggestion": "company_name"
  }}
]
"""
    
    def _create_field_mapping_prompt(
        self,
        fields: List[Dict[str, Any]],
        company_data: Dict[str, Any]
    ) -> str:
        """Create prompt for field mapping."""
        fields_json = json.dumps(fields, indent=2)
        company_json = json.dumps(company_data, indent=2)
        
        return f"""
You are mapping form fields to company data for a VC application. Match each form field to the most appropriate company data field.

Form Fields:
{fields_json}

Company Data:
{company_json}

For each form field, provide the best matching value from the company data. If no good match exists, suggest a reasonable default value.

Respond with a JSON object mapping field names to values. Example:
{{
  "company_name": "TechStartup Inc.",
  "industry": "SaaS/FinTech",
  "team_size": "25"
}}
"""
    
    def _create_value_generation_prompt(
        self,
        field_name: str,
        field_type: str,
        context: str,
        company_data: Dict[str, Any]
    ) -> str:
        """Create prompt for value generation."""
        company_json = json.dumps(company_data, indent=2)
        
        return f"""
Generate an appropriate value for a form field in a VC application.

Field Name: {field_name}
Field Type: {field_type}
Context: {context}

Company Data:
{company_json}

Generate a value that:
1. Matches the field type and context
2. Uses relevant company data when possible
3. Is professional and appropriate for VC applications
4. Is concise but informative

Return only the value, no additional text.
"""
    
    def _create_validation_prompt(
        self,
        form_data: Dict[str, str],
        form_context: str
    ) -> str:
        """Create prompt for form validation."""
        data_json = json.dumps(form_data, indent=2)
        
        return f"""
Validate the following form data for a VC application.

Form Data:
{data_json}

Form Context: {form_context}

Check for:
1. Completeness - all required fields filled
2. Consistency - data makes sense together
3. Professionalism - appropriate for VC applications
4. Accuracy - reasonable values

Respond with JSON:
{{
  "valid": true/false,
  "errors": ["list of errors"],
  "warnings": ["list of warnings"],
  "suggestions": ["list of improvements"]
}}
"""
    
    async def _get_ai_response(self, prompt: str) -> str:
        """
        Get response from OpenAI API.
        
        Args:
            prompt: Prompt to send to AI
            
        Returns:
            AI response text
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing and filling out venture capital application forms."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            raise
    
    def _parse_field_analysis_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse AI response for field analysis."""
        try:
            # Extract JSON from response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                return []
            
            json_str = response[json_start:json_end]
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Error parsing field analysis response: {str(e)}")
            return []
    
    def _parse_field_mapping_response(self, response: str) -> Dict[str, str]:
        """Parse AI response for field mapping."""
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                return {}
            
            json_str = response[json_start:json_end]
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Error parsing field mapping response: {str(e)}")
            return {}
    
    def _parse_validation_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for validation."""
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                return {"valid": False, "errors": ["Could not parse validation response"]}
            
            json_str = response[json_start:json_end]
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Error parsing validation response: {str(e)}")
            return {"valid": False, "errors": [str(e)]}
    
    async def get_form_template_suggestions(self, url: str, page_source: str) -> Dict[str, Any]:
        """
        Get suggestions for form templates based on URL and content.
        
        Args:
            url: Form URL
            page_source: Page HTML source
            
        Returns:
            Template suggestions
        """
        try:
            prompt = f"""
Analyze this VC application form and suggest the best template to use.

URL: {url}
Page Content: {page_source[:3000]}...

Suggest:
1. template_name: Name of the best matching template
2. confidence: Confidence level (0-100)
3. customizations: List of customizations needed
4. field_mappings: Specific field mappings for this form

Respond with JSON:
{{
  "template_name": "template_name",
  "confidence": 85,
  "customizations": ["list of needed changes"],
  "field_mappings": {{"field": "value"}}
}}
"""
            
            response = await self._get_ai_response(prompt)
            return self._parse_field_mapping_response(response)
            
        except Exception as e:
            logger.error(f"Error getting template suggestions: {str(e)}")
            return {} 