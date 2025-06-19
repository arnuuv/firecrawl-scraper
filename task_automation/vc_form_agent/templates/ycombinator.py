"""
Y Combinator Form Template

Template for Y Combinator application forms with specific field mappings
and validation rules for their application process.
"""

from typing import Dict, List, Any
from loguru import logger

from .base import BaseFormTemplate


class YCombinatorTemplate(BaseFormTemplate):
    """
    Template for Y Combinator application forms.
    
    Y Combinator has a specific application format with unique field names
    and requirements. This template handles their standard application process.
    """
    
    def _initialize_template(self) -> None:
        """Initialize Y Combinator specific template configuration."""
        # Core company information
        self.add_field_mapping("company_name", "company_name", required=True)
        self.add_field_mapping("founder_names", "founders", required=True)
        self.add_field_mapping("company_description", "competitive_advantage", required=True)
        self.add_field_mapping("team_size", "team_size", required=True)
        self.add_field_mapping("funding_stage", "funding_stage", required=True)
        self.add_field_mapping("use_of_funds", "use_of_funds", required=True)
        
        # Contact information
        self.add_field_mapping("email", "email", required=True)
        self.add_field_mapping("phone", "phone", required=False)
        self.add_field_mapping("website", "website", required=False)
        
        # Financial information
        self.add_field_mapping("revenue", "revenue", required=False)
        self.add_field_mapping("monthly_recurring_revenue", "traction_metrics.monthly_recurring_revenue", required=False)
        self.add_field_mapping("customer_count", "traction_metrics.customer_count", required=False)
        self.add_field_mapping("churn_rate", "traction_metrics.churn_rate", required=False)
        
        # Market and competition
        self.add_field_mapping("target_market", "target_market", required=True)
        self.add_field_mapping("competitive_advantage", "competitive_advantage", required=True)
        self.add_field_mapping("competitors", "competitive_advantage", required=False)
        
        # Product and technology
        self.add_field_mapping("product_description", "competitive_advantage", required=True)
        self.add_field_mapping("technology_stack", "competitive_advantage", required=False)
        self.add_field_mapping("development_stage", "funding_stage", required=False)
        
        # Traction and metrics
        self.add_field_mapping("traction_metrics", "traction_metrics", required=False)
        self.add_field_mapping("growth_rate", "growth_rate", required=False)
        self.add_field_mapping("key_metrics", "traction_metrics", required=False)
        
        # Team information
        self.add_field_mapping("founder_backgrounds", "founders", required=False)
        self.add_field_mapping("team_experience", "founders", required=False)
        self.add_field_mapping("advisors", "investors", required=False)
        
        # Funding information
        self.add_field_mapping("previous_funding", "financials.total_funding", required=False)
        self.add_field_mapping("investors", "investors", required=False)
        self.add_field_mapping("valuation", "financials.total_funding", required=False)
        
        # YC specific fields
        self.add_field_mapping("yc_batch_preference", "funding_stage", required=False)
        self.add_field_mapping("relocation_willingness", "target_market", required=False)
        self.add_field_mapping("cofounder_relationship", "founders", required=False)
        
        # Add validation rules
        self._add_validation_rules()
        
        # Add custom scripts for YC specific behavior
        self._add_custom_scripts()
        
        logger.info("Y Combinator template initialized")
    
    def _add_validation_rules(self) -> None:
        """Add Y Combinator specific validation rules."""
        # Company name validation
        self.add_validation_rule("company_name", {
            "max_length": 100,
            "case": "title_case",
            "required": True
        })
        
        # Email validation
        self.add_validation_rule("email", {
            "format": "email",
            "required": True
        })
        
        # Team size validation
        self.add_validation_rule("team_size", {
            "min_value": 1,
            "max_value": 50,
            "type": "integer"
        })
        
        # Revenue validation
        self.add_validation_rule("revenue", {
            "format": "currency",
            "min_value": 0
        })
        
        # Description validation
        self.add_validation_rule("company_description", {
            "min_length": 50,
            "max_length": 1000,
            "required": True
        })
        
        # Use of funds validation
        self.add_validation_rule("use_of_funds", {
            "min_length": 20,
            "max_length": 500,
            "required": True
        })
    
    def _add_custom_scripts(self) -> None:
        """Add custom JavaScript scripts for YC form behavior."""
        # Script to handle dynamic form fields
        dynamic_fields_script = """
        // Handle dynamic field visibility based on funding stage
        function handleFundingStageChange() {
            const fundingStage = document.querySelector('[name="funding_stage"]');
            const revenueFields = document.querySelectorAll('[name*="revenue"]');
            const customerFields = document.querySelectorAll('[name*="customer"]');
            
            if (fundingStage && fundingStage.value === 'idea') {
                revenueFields.forEach(field => {
                    field.closest('.form-group').style.display = 'none';
                });
                customerFields.forEach(field => {
                    field.closest('.form-group').style.display = 'none';
                });
            } else {
                revenueFields.forEach(field => {
                    field.closest('.form-group').style.display = 'block';
                });
                customerFields.forEach(field => {
                    field.closest('.form-group').style.display = 'block';
                });
            }
        }
        
        // Auto-format currency fields
        function formatCurrencyFields() {
            const currencyFields = document.querySelectorAll('[name*="revenue"], [name*="funding"]');
            currencyFields.forEach(field => {
                field.addEventListener('blur', function() {
                    const value = this.value.replace(/[^0-9.]/g, '');
                    if (value) {
                        const numValue = parseFloat(value);
                        if (!isNaN(numValue)) {
                            this.value = '$' + numValue.toLocaleString();
                        }
                    }
                });
            });
        }
        
        // Initialize scripts
        document.addEventListener('DOMContentLoaded', function() {
            handleFundingStageChange();
            formatCurrencyFields();
            
            // Add event listeners
            const fundingStageField = document.querySelector('[name="funding_stage"]');
            if (fundingStageField) {
                fundingStageField.addEventListener('change', handleFundingStageChange);
            }
        });
        """
        
        self.add_custom_script(dynamic_fields_script)
    
    def get_description(self) -> str:
        """Get Y Combinator template description."""
        return "Template for Y Combinator application forms with specific field mappings and validation rules"
    
    def get_yc_specific_mappings(self) -> Dict[str, str]:
        """
        Get Y Combinator specific field mappings.
        
        Returns:
            Dictionary of YC specific field mappings
        """
        return {
            # YC specific field names
            "startup_name": "company_name",
            "founder_name": "founders",
            "startup_description": "competitive_advantage",
            "team_members": "team_size",
            "funding_round": "funding_stage",
            "funding_purpose": "use_of_funds",
            "contact_email": "email",
            "contact_phone": "phone",
            "startup_website": "website",
            "monthly_revenue": "traction_metrics.monthly_recurring_revenue",
            "total_customers": "traction_metrics.customer_count",
            "customer_churn": "traction_metrics.churn_rate",
            "target_audience": "target_market",
            "competitive_edge": "competitive_advantage",
            "competitor_analysis": "competitive_advantage",
            "product_overview": "competitive_advantage",
            "tech_stack": "competitive_advantage",
            "development_phase": "funding_stage",
            "growth_metrics": "traction_metrics",
            "growth_percentage": "growth_rate",
            "key_performance_indicators": "traction_metrics",
            "founder_bios": "founders",
            "team_expertise": "founders",
            "advisory_board": "investors",
            "previous_investments": "financials.total_funding",
            "current_investors": "investors",
            "company_valuation": "financials.total_funding",
            "batch_preference": "funding_stage",
            "relocation_ok": "target_market",
            "cofounder_details": "founders"
        }
    
    def customize_for_yc_batch(self, batch_type: str = "winter") -> None:
        """
        Customize template for specific YC batch.
        
        Args:
            batch_type: Type of YC batch (winter, summer, etc.)
        """
        if batch_type.lower() == "winter":
            # Winter batch specific customizations
            self.add_field_mapping("winter_batch_preference", "funding_stage", required=False)
            self.add_field_mapping("winter_relocation", "target_market", required=False)
        elif batch_type.lower() == "summer":
            # Summer batch specific customizations
            self.add_field_mapping("summer_batch_preference", "funding_stage", required=False)
            self.add_field_mapping("summer_relocation", "target_market", required=False)
        
        logger.info(f"Customized template for YC {batch_type} batch")
    
    def get_yc_application_tips(self) -> List[str]:
        """
        Get tips for Y Combinator applications.
        
        Returns:
            List of application tips
        """
        return [
            "Keep company description concise but compelling (50-100 words)",
            "Focus on traction metrics if you have them",
            "Be specific about use of funds",
            "Highlight unique competitive advantages",
            "Include founder backgrounds and experience",
            "Be honest about current stage and challenges",
            "Show market understanding and opportunity size",
            "Demonstrate product-market fit if applicable",
            "Include customer testimonials or case studies if available",
            "Be prepared for follow-up questions about technical details"
        ]
    
    def validate_yc_specific_requirements(self, form_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Validate Y Combinator specific requirements.
        
        Args:
            form_data: Form data dictionary
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        # Check for YC specific requirements
        if "company_description" in form_data:
            desc = form_data["company_description"]
            if len(desc) < 50:
                errors.append("Company description should be at least 50 characters")
            elif len(desc) > 1000:
                warnings.append("Company description is quite long, consider being more concise")
        
        if "use_of_funds" in form_data:
            funds_desc = form_data["use_of_funds"]
            if len(funds_desc) < 20:
                errors.append("Use of funds description should be more detailed")
        
        if "team_size" in form_data:
            try:
                team_size = int(form_data["team_size"])
                if team_size > 10:
                    warnings.append("Large team size for early stage - consider highlighting key roles")
            except ValueError:
                errors.append("Invalid team size format")
        
        # Check for founder information
        if "founder_names" not in form_data or not form_data["founder_names"]:
            errors.append("Founder information is required")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "completion_percentage": 100 if len(errors) == 0 else 80
        } 