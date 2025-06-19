"""
Base Form Template

Base class for form templates that provides common functionality
for handling different types of VC application forms.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from loguru import logger
from pydantic import BaseModel


@dataclass
class FieldMapping:
    """Represents a field mapping configuration."""
    form_field: str
    company_field: str
    required: bool = True
    default_value: Optional[str] = None
    transformation: Optional[str] = None  # e.g., "uppercase", "title_case", "format_currency"


class FormTemplate(BaseModel):
    """Base form template model."""
    name: str
    description: str
    url_pattern: str
    field_mappings: Dict[str, str]
    required_fields: List[str]
    optional_fields: List[str]
    custom_scripts: Optional[List[str]] = None
    validation_rules: Optional[Dict[str, Any]] = None


class BaseFormTemplate(ABC):
    """
    Base class for form templates.
    
    This class provides common functionality for handling different types
    of VC application forms and can be extended for specific VC firms.
    """
    
    def __init__(self, template_name: str):
        """
        Initialize base template.
        
        Args:
            template_name: Name of the template
        """
        self.template_name = template_name
        self.field_mappings = {}
        self.required_fields = []
        self.optional_fields = []
        self.custom_scripts = []
        self.validation_rules = {}
        
        # Initialize template-specific configurations
        self._initialize_template()
        
        logger.info(f"Initialized template: {template_name}")
    
    @abstractmethod
    def _initialize_template(self) -> None:
        """
        Initialize template-specific configurations.
        
        This method should be implemented by subclasses to set up
        field mappings, validation rules, and other template-specific settings.
        """
        pass
    
    def get_field_mappings(self) -> Dict[str, str]:
        """
        Get field mappings for this template.
        
        Returns:
            Dictionary mapping form fields to company data fields
        """
        return self.field_mappings.copy()
    
    def get_required_fields(self) -> List[str]:
        """
        Get list of required fields for this template.
        
        Returns:
            List of required field names
        """
        return self.required_fields.copy()
    
    def get_optional_fields(self) -> List[str]:
        """
        Get list of optional fields for this template.
        
        Returns:
            List of optional field names
        """
        return self.optional_fields.copy()
    
    def add_field_mapping(self, form_field: str, company_field: str, required: bool = True) -> None:
        """
        Add a field mapping to the template.
        
        Args:
            form_field: Name of the form field
            company_field: Name of the company data field
            required: Whether this field is required
        """
        self.field_mappings[form_field] = company_field
        
        if required:
            if form_field not in self.required_fields:
                self.required_fields.append(form_field)
        else:
            if form_field not in self.optional_fields:
                self.optional_fields.append(form_field)
        
        logger.debug(f"Added field mapping: {form_field} -> {company_field}")
    
    def remove_field_mapping(self, form_field: str) -> None:
        """
        Remove a field mapping from the template.
        
        Args:
            form_field: Name of the form field to remove
        """
        if form_field in self.field_mappings:
            del self.field_mappings[form_field]
        
        if form_field in self.required_fields:
            self.required_fields.remove(form_field)
        
        if form_field in self.optional_fields:
            self.optional_fields.remove(form_field)
        
        logger.debug(f"Removed field mapping: {form_field}")
    
    def customize_field_mappings(self, custom_mappings: Dict[str, str]) -> None:
        """
        Customize field mappings for specific use cases.
        
        Args:
            custom_mappings: Dictionary of custom field mappings
        """
        for form_field, company_field in custom_mappings.items():
            self.add_field_mapping(form_field, company_field)
        
        logger.info(f"Customized {len(custom_mappings)} field mappings")
    
    def add_custom_script(self, script: str) -> None:
        """
        Add a custom JavaScript script to run on the form page.
        
        Args:
            script: JavaScript code to execute
        """
        self.custom_scripts.append(script)
        logger.debug(f"Added custom script to template: {self.template_name}")
    
    def add_validation_rule(self, field_name: str, rule: Dict[str, Any]) -> None:
        """
        Add a validation rule for a specific field.
        
        Args:
            field_name: Name of the field to validate
            rule: Validation rule configuration
        """
        self.validation_rules[field_name] = rule
        logger.debug(f"Added validation rule for field: {field_name}")
    
    def transform_field_value(self, field_name: str, value: str) -> str:
        """
        Transform a field value based on template rules.
        
        Args:
            field_name: Name of the field
            value: Original value
            
        Returns:
            Transformed value
        """
        # Apply common transformations
        if field_name in self.validation_rules:
            rule = self.validation_rules[field_name]
            
            # Case transformations
            if rule.get("case") == "uppercase":
                value = value.upper()
            elif rule.get("case") == "lowercase":
                value = value.lower()
            elif rule.get("case") == "title_case":
                value = value.title()
            
            # Length transformations
            max_length = rule.get("max_length")
            if max_length and len(value) > max_length:
                value = value[:max_length]
            
            # Format transformations
            if rule.get("format") == "currency":
                try:
                    # Convert to currency format
                    num_value = float(value.replace(",", "").replace("$", ""))
                    value = f"${num_value:,.2f}"
                except ValueError:
                    pass
        
        return value
    
    def validate_template_completeness(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that company data has all required fields for this template.
        
        Args:
            company_data: Company data dictionary
            
        Returns:
            Validation result
        """
        missing_fields = []
        available_fields = []
        
        for form_field, company_field in self.field_mappings.items():
            if form_field in self.required_fields:
                if company_field not in company_data or not company_data[company_field]:
                    missing_fields.append(f"{form_field} (maps to {company_field})")
                else:
                    available_fields.append(form_field)
        
        completion_percentage = (
            len(available_fields) / len(self.required_fields) * 100
            if self.required_fields else 100
        )
        
        return {
            "complete": len(missing_fields) == 0,
            "missing_fields": missing_fields,
            "available_fields": available_fields,
            "completion_percentage": completion_percentage,
            "total_required": len(self.required_fields),
            "total_optional": len(self.optional_fields)
        }
    
    def get_template_info(self) -> Dict[str, Any]:
        """
        Get information about this template.
        
        Returns:
            Dictionary with template information
        """
        return {
            "name": self.template_name,
            "description": self.get_description(),
            "field_mappings": self.field_mappings,
            "required_fields": self.required_fields,
            "optional_fields": self.optional_fields,
            "custom_scripts_count": len(self.custom_scripts),
            "validation_rules_count": len(self.validation_rules)
        }
    
    def get_description(self) -> str:
        """
        Get template description.
        
        Returns:
            Template description
        """
        return f"Template for {self.template_name} applications"
    
    def export_template(self) -> Dict[str, Any]:
        """
        Export template configuration.
        
        Returns:
            Template configuration dictionary
        """
        return {
            "name": self.template_name,
            "description": self.get_description(),
            "field_mappings": self.field_mappings,
            "required_fields": self.required_fields,
            "optional_fields": self.optional_fields,
            "custom_scripts": self.custom_scripts,
            "validation_rules": self.validation_rules
        }
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'BaseFormTemplate':
        """
        Create template from configuration.
        
        Args:
            config: Template configuration dictionary
            
        Returns:
            Template instance
        """
        template = cls(config["name"])
        template.field_mappings = config.get("field_mappings", {})
        template.required_fields = config.get("required_fields", [])
        template.optional_fields = config.get("optional_fields", [])
        template.custom_scripts = config.get("custom_scripts", [])
        template.validation_rules = config.get("validation_rules", {})
        
        return template
    
    def __str__(self) -> str:
        """String representation of template."""
        return f"{self.template_name} Template ({len(self.field_mappings)} fields)"
    
    def __repr__(self) -> str:
        """Detailed string representation of template."""
        return f"<{self.__class__.__name__} name='{self.template_name}' fields={len(self.field_mappings)}>" 