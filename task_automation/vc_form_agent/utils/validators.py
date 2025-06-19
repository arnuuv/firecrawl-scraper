"""
Form Validator

Validates form data to ensure completeness and correctness before submission.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from loguru import logger
from pydantic import BaseModel, ValidationError


@dataclass
class ValidationResult:
    """Result of form validation."""
    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    completion_percentage: float


class FormValidator:
    """
    Validates form data for completeness and correctness.
    """
    
    def __init__(self):
        """Initialize form validator."""
        # Common validation patterns
        self.patterns = {
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "phone": r"^[\+]?[1-9][\d]{0,15}$",
            "url": r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$",
            "date": r"^\d{4}-\d{2}-\d{2}$",
            "currency": r"^\$?[\d,]+(\.\d{2})?$",
            "percentage": r"^\d+(\.\d+)?%?$"
        }
        
        # Required field patterns for different form types
        self.required_patterns = {
            "company_info": ["company_name", "industry", "founding_date"],
            "financial": ["revenue", "funding_stage", "use_of_funds"],
            "team": ["team_size", "founders"],
            "contact": ["email", "phone"]
        }
        
        logger.info("FormValidator initialized")
    
    async def validate_form(
        self,
        browser_manager,
        field_mappings: Dict[str, str]
    ) -> ValidationResult:
        """
        Validate a form before submission.
        
        Args:
            browser_manager: Browser manager instance
            field_mappings: Dictionary of field mappings
            
        Returns:
            ValidationResult object
        """
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Get form data from browser
            form_data = await self._extract_form_data(browser_manager)
            
            # Validate required fields
            required_validation = self._validate_required_fields(form_data, field_mappings)
            errors.extend(required_validation.errors)
            warnings.extend(required_validation.warnings)
            
            # Validate field formats
            format_validation = self._validate_field_formats(form_data)
            errors.extend(format_validation.errors)
            warnings.extend(format_validation.warnings)
            
            # Validate data consistency
            consistency_validation = self._validate_data_consistency(form_data)
            errors.extend(consistency_validation.errors)
            warnings.extend(consistency_validation.warnings)
            
            # Generate suggestions
            suggestions = self._generate_suggestions(form_data, errors, warnings)
            
            # Calculate completion percentage
            completion_percentage = self._calculate_completion_percentage(form_data, field_mappings)
            
            valid = len(errors) == 0
            
            return ValidationResult(
                valid=valid,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                completion_percentage=completion_percentage
            )
            
        except Exception as e:
            logger.error(f"Error validating form: {str(e)}")
            return ValidationResult(
                valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=[],
                suggestions=[],
                completion_percentage=0.0
            )
    
    async def _extract_form_data(self, browser_manager) -> Dict[str, str]:
        """
        Extract form data from browser.
        
        Args:
            browser_manager: Browser manager instance
            
        Returns:
            Dictionary of form field values
        """
        try:
            # This would need to be implemented based on the specific browser manager
            # For now, return empty dict as placeholder
            return {}
            
        except Exception as e:
            logger.error(f"Error extracting form data: {str(e)}")
            return {}
    
    def _validate_required_fields(
        self,
        form_data: Dict[str, str],
        field_mappings: Dict[str, str]
    ) -> ValidationResult:
        """
        Validate that all required fields are filled.
        
        Args:
            form_data: Dictionary of form data
            field_mappings: Dictionary of field mappings
            
        Returns:
            ValidationResult for required fields
        """
        errors = []
        warnings = []
        
        # Check if all mapped fields have values
        for field_name, mapped_value in field_mappings.items():
            if not mapped_value or mapped_value.strip() == "":
                errors.append(f"Required field '{field_name}' is empty")
            elif field_name in form_data:
                form_value = form_data[field_name]
                if not form_value or form_value.strip() == "":
                    errors.append(f"Required field '{field_name}' is not filled in form")
        
        # Check for common required fields
        common_required = ["company_name", "email", "description"]
        for field in common_required:
            if field not in field_mappings and field not in form_data:
                warnings.append(f"Common required field '{field}' not found")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=[],
            completion_percentage=0.0
        )
    
    def _validate_field_formats(self, form_data: Dict[str, str]) -> ValidationResult:
        """
        Validate field formats (email, phone, etc.).
        
        Args:
            form_data: Dictionary of form data
            
        Returns:
            ValidationResult for field formats
        """
        errors = []
        warnings = []
        
        for field_name, value in form_data.items():
            if not value:
                continue
            
            # Email validation
            if "email" in field_name.lower():
                if not re.match(self.patterns["email"], value):
                    errors.append(f"Invalid email format in field '{field_name}': {value}")
            
            # Phone validation
            elif "phone" in field_name.lower():
                # Remove common phone formatting
                clean_phone = re.sub(r'[\s\-\(\)]', '', value)
                if not re.match(self.patterns["phone"], clean_phone):
                    warnings.append(f"Potentially invalid phone format in field '{field_name}': {value}")
            
            # URL validation
            elif "url" in field_name.lower() or "website" in field_name.lower():
                if not re.match(self.patterns["url"], value):
                    warnings.append(f"Potentially invalid URL format in field '{field_name}': {value}")
            
            # Date validation
            elif "date" in field_name.lower():
                if not re.match(self.patterns["date"], value):
                    try:
                        # Try to parse various date formats
                        datetime.strptime(value, "%Y-%m-%d")
                    except ValueError:
                        try:
                            datetime.strptime(value, "%m/%d/%Y")
                        except ValueError:
                            warnings.append(f"Potentially invalid date format in field '{field_name}': {value}")
            
            # Currency validation
            elif "revenue" in field_name.lower() or "funding" in field_name.lower():
                if not re.match(self.patterns["currency"], value.replace(",", "")):
                    warnings.append(f"Potentially invalid currency format in field '{field_name}': {value}")
            
            # Percentage validation
            elif "growth" in field_name.lower() or "rate" in field_name.lower():
                if not re.match(self.patterns["percentage"], value):
                    warnings.append(f"Potentially invalid percentage format in field '{field_name}': {value}")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=[],
            completion_percentage=0.0
        )
    
    def _validate_data_consistency(self, form_data: Dict[str, str]) -> ValidationResult:
        """
        Validate data consistency across fields.
        
        Args:
            form_data: Dictionary of form data
            
        Returns:
            ValidationResult for data consistency
        """
        errors = []
        warnings = []
        
        # Check for logical inconsistencies
        if "team_size" in form_data and "revenue" in form_data:
            try:
                team_size = int(form_data["team_size"])
                revenue = float(form_data["revenue"].replace(",", "").replace("$", ""))
                
                # Check if revenue per employee is reasonable
                revenue_per_employee = revenue / team_size
                if revenue_per_employee > 1000000:  # $1M per employee
                    warnings.append("Revenue per employee seems unusually high")
                elif revenue_per_employee < 1000:  # $1K per employee
                    warnings.append("Revenue per employee seems unusually low")
                    
            except (ValueError, ZeroDivisionError):
                pass
        
        # Check funding stage consistency
        if "funding_stage" in form_data and "revenue" in form_data:
            funding_stage = form_data["funding_stage"].lower()
            try:
                revenue = float(form_data["revenue"].replace(",", "").replace("$", ""))
                
                if "seed" in funding_stage and revenue > 1000000:
                    warnings.append("High revenue for seed stage company")
                elif "series a" in funding_stage and revenue < 100000:
                    warnings.append("Low revenue for Series A stage company")
                    
            except ValueError:
                pass
        
        # Check team size consistency
        if "team_size" in form_data:
            try:
                team_size = int(form_data["team_size"])
                if team_size < 1:
                    errors.append("Team size must be at least 1")
                elif team_size > 10000:
                    warnings.append("Team size seems unusually large")
                    
            except ValueError:
                errors.append("Invalid team size format")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=[],
            completion_percentage=0.0
        )
    
    def _generate_suggestions(
        self,
        form_data: Dict[str, str],
        errors: List[str],
        warnings: List[str]
    ) -> List[str]:
        """
        Generate suggestions for improving form data.
        
        Args:
            form_data: Dictionary of form data
            errors: List of validation errors
            warnings: List of validation warnings
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        # Suggest improvements based on errors and warnings
        if any("email" in error.lower() for error in errors):
            suggestions.append("Ensure email addresses follow standard format (user@domain.com)")
        
        if any("phone" in warning.lower() for warning in warnings):
            suggestions.append("Consider using international phone format (+1-555-123-4567)")
        
        if any("revenue" in warning.lower() for warning in warnings):
            suggestions.append("Use consistent currency format (e.g., $1,000,000)")
        
        # Suggest based on missing common fields
        if "company_name" not in form_data:
            suggestions.append("Include company name if not already present")
        
        if "description" not in form_data and "about" not in form_data:
            suggestions.append("Consider adding a company description")
        
        if "team_size" not in form_data:
            suggestions.append("Include team size information")
        
        # Suggest based on data quality
        for field_name, value in form_data.items():
            if value and len(value.strip()) < 10:
                if "description" in field_name.lower() or "about" in field_name.lower():
                    suggestions.append(f"Consider expanding the {field_name} field for better detail")
        
        return suggestions
    
    def _calculate_completion_percentage(
        self,
        form_data: Dict[str, str],
        field_mappings: Dict[str, str]
    ) -> float:
        """
        Calculate form completion percentage.
        
        Args:
            form_data: Dictionary of form data
            field_mappings: Dictionary of field mappings
            
        Returns:
            Completion percentage (0-100)
        """
        total_fields = len(field_mappings)
        if total_fields == 0:
            return 0.0
        
        filled_fields = 0
        for field_name, mapped_value in field_mappings.items():
            if mapped_value and mapped_value.strip():
                filled_fields += 1
        
        return (filled_fields / total_fields) * 100
    
    def validate_company_profile(self, profile_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate company profile data.
        
        Args:
            profile_data: Company profile data
            
        Returns:
            ValidationResult for company profile
        """
        errors = []
        warnings = []
        suggestions = []
        
        # Required fields
        required_fields = ["company_name", "industry", "founding_date", "team_size"]
        for field in required_fields:
            if field not in profile_data or not profile_data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        # Validate specific fields
        if "email" in profile_data:
            email = profile_data["email"]
            if email and not re.match(self.patterns["email"], email):
                errors.append(f"Invalid email format: {email}")
        
        if "website" in profile_data:
            website = profile_data["website"]
            if website and not re.match(self.patterns["url"], website):
                warnings.append(f"Potentially invalid website URL: {website}")
        
        if "team_size" in profile_data:
            try:
                team_size = int(profile_data["team_size"])
                if team_size < 1:
                    errors.append("Team size must be at least 1")
            except (ValueError, TypeError):
                errors.append("Invalid team size format")
        
        if "revenue" in profile_data:
            try:
                revenue = float(str(profile_data["revenue"]).replace(",", "").replace("$", ""))
                if revenue < 0:
                    errors.append("Revenue cannot be negative")
            except (ValueError, TypeError):
                warnings.append("Invalid revenue format")
        
        # Generate suggestions
        if "competitive_advantage" not in profile_data:
            suggestions.append("Consider adding competitive advantage information")
        
        if "use_of_funds" not in profile_data:
            suggestions.append("Consider adding use of funds information")
        
        if "traction_metrics" not in profile_data:
            suggestions.append("Consider adding traction metrics")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            completion_percentage=0.0
        )
    
    def get_validation_summary(self, validation_result: ValidationResult) -> str:
        """
        Get a human-readable validation summary.
        
        Args:
            validation_result: Validation result object
            
        Returns:
            Formatted validation summary
        """
        summary = []
        
        if validation_result.valid:
            summary.append("✅ Form validation passed")
        else:
            summary.append("❌ Form validation failed")
        
        summary.append(f"📊 Completion: {validation_result.completion_percentage:.1f}%")
        
        if validation_result.errors:
            summary.append(f"❌ Errors: {len(validation_result.errors)}")
            for error in validation_result.errors[:3]:  # Show first 3 errors
                summary.append(f"   • {error}")
        
        if validation_result.warnings:
            summary.append(f"⚠️  Warnings: {len(validation_result.warnings)}")
            for warning in validation_result.warnings[:3]:  # Show first 3 warnings
                summary.append(f"   • {warning}")
        
        if validation_result.suggestions:
            summary.append(f"💡 Suggestions: {len(validation_result.suggestions)}")
            for suggestion in validation_result.suggestions[:3]:  # Show first 3 suggestions
                summary.append(f"   • {suggestion}")
        
        return "\n".join(summary) 