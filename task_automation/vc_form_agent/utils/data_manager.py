"""
Data Manager

Manages company profiles, VC databases, and form templates.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from loguru import logger
from pydantic import BaseModel, Field


class CompanyProfile(BaseModel):
    """Company profile data model."""
    company_name: str
    industry: str
    founding_date: str
    team_size: int
    funding_stage: str
    revenue: Optional[float] = None
    growth_rate: Optional[float] = None
    target_market: str
    competitive_advantage: str
    use_of_funds: str
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    founders: Optional[List[str]] = None
    investors: Optional[List[str]] = None
    traction_metrics: Optional[Dict[str, Any]] = None
    financials: Optional[Dict[str, Any]] = None


class VCFirm(BaseModel):
    """VC firm data model."""
    name: str
    website: str
    application_url: str
    focus_areas: List[str]
    investment_stages: List[str]
    check_size: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    application_deadline: Optional[str] = None
    notes: Optional[str] = None


class FormTemplate(BaseModel):
    """Form template data model."""
    name: str
    description: str
    url_pattern: str
    field_mappings: Dict[str, str]
    required_fields: List[str]
    optional_fields: List[str]
    custom_scripts: Optional[List[str]] = None


class DataManager:
    """
    Manages all data for the VC form filling agent.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize data manager.
        
        Args:
            data_dir: Directory to store data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # File paths
        self.company_profile_path = self.data_dir / "company_profile.json"
        self.vc_database_path = self.data_dir / "vc_database.json"
        self.templates_dir = self.data_dir / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        # Initialize default data
        self._initialize_default_data()
        
        logger.info(f"DataManager initialized with data directory: {self.data_dir}")
    
    def _initialize_default_data(self) -> None:
        """Initialize default data files if they don't exist."""
        if not self.company_profile_path.exists():
            self._create_default_company_profile()
        
        if not self.vc_database_path.exists():
            self._create_default_vc_database()
        
        if not any(self.templates_dir.iterdir()):
            self._create_default_templates()
    
    def _create_default_company_profile(self) -> None:
        """Create default company profile."""
        default_profile = CompanyProfile(
            company_name="Your Startup Inc.",
            industry="SaaS/FinTech",
            founding_date="2023-01-15",
            team_size=25,
            funding_stage="Seed",
            revenue=500000,
            growth_rate=300,
            target_market="SMBs in North America",
            competitive_advantage="AI-powered automation platform",
            use_of_funds="Product development and market expansion",
            website="https://yourstartup.com",
            email="founder@yourstartup.com",
            phone="+1-555-0123",
            address="123 Startup St, San Francisco, CA 94105",
            founders=["John Doe", "Jane Smith"],
            investors=["Angel Investor 1", "Angel Investor 2"],
            traction_metrics={
                "monthly_recurring_revenue": 50000,
                "customer_count": 500,
                "churn_rate": 0.05,
                "customer_acquisition_cost": 150
            },
            financials={
                "burn_rate": 75000,
                "runway_months": 8,
                "total_funding": 1000000
            }
        )
        
        self.save_company_profile(default_profile)
        logger.info("Created default company profile")
    
    def _create_default_vc_database(self) -> None:
        """Create default VC database."""
        default_vcs = [
            VCFirm(
                name="Y Combinator",
                website="https://ycombinator.com",
                application_url="https://apply.ycombinator.com",
                focus_areas=["Technology", "SaaS", "AI/ML"],
                investment_stages=["Seed", "Series A"],
                check_size="$500K - $2M",
                application_deadline="2024-03-15"
            ),
            VCFirm(
                name="Techstars",
                website="https://techstars.com",
                application_url="https://apply.techstars.com",
                focus_areas=["Technology", "Innovation"],
                investment_stages=["Seed", "Early Stage"],
                check_size="$100K - $500K"
            ),
            VCFirm(
                name="500 Startups",
                website="https://500.co",
                application_url="https://500.co/apply",
                focus_areas=["Technology", "Diverse Founders"],
                investment_stages=["Seed", "Series A"],
                check_size="$150K - $500K"
            )
        ]
        
        self.save_vc_database(default_vcs)
        logger.info("Created default VC database")
    
    def _create_default_templates(self) -> None:
        """Create default form templates."""
        templates = {
            "ycombinator": FormTemplate(
                name="Y Combinator",
                description="Y Combinator application form template",
                url_pattern=".*ycombinator.*apply.*",
                field_mappings={
                    "company_name": "company_name",
                    "founder_names": "founders",
                    "company_description": "competitive_advantage",
                    "team_size": "team_size",
                    "funding_stage": "funding_stage",
                    "use_of_funds": "use_of_funds"
                },
                required_fields=["company_name", "founder_names", "company_description"],
                optional_fields=["team_size", "funding_stage", "use_of_funds"]
            ),
            "techstars": FormTemplate(
                name="Techstars",
                description="Techstars application form template",
                url_pattern=".*techstars.*apply.*",
                field_mappings={
                    "startup_name": "company_name",
                    "industry": "industry",
                    "founders": "founders",
                    "description": "competitive_advantage",
                    "team_size": "team_size"
                },
                required_fields=["startup_name", "industry", "founders"],
                optional_fields=["description", "team_size"]
            ),
            "generic": FormTemplate(
                name="Generic VC Form",
                description="Generic template for unknown VC forms",
                url_pattern=".*",
                field_mappings={
                    "company_name": "company_name",
                    "business_name": "company_name",
                    "organization_name": "company_name",
                    "industry": "industry",
                    "sector": "industry",
                    "team_size": "team_size",
                    "employees": "team_size",
                    "funding_stage": "funding_stage",
                    "investment_stage": "funding_stage",
                    "description": "competitive_advantage",
                    "about": "competitive_advantage",
                    "use_of_funds": "use_of_funds",
                    "funding_purpose": "use_of_funds"
                },
                required_fields=["company_name"],
                optional_fields=["industry", "team_size", "funding_stage", "description"]
            )
        }
        
        for name, template in templates.items():
            self.save_template(name, template)
        
        logger.info("Created default form templates")
    
    def load_company_profile(self) -> Dict[str, Any]:
        """
        Load company profile from file.
        
        Returns:
            Company profile as dictionary
        """
        try:
            if self.company_profile_path.exists():
                with open(self.company_profile_path, 'r') as f:
                    data = json.load(f)
                    return data
            else:
                logger.warning("Company profile not found, creating default")
                self._create_default_company_profile()
                return self.load_company_profile()
                
        except Exception as e:
            logger.error(f"Error loading company profile: {str(e)}")
            return {}
    
    def save_company_profile(self, profile: CompanyProfile) -> None:
        """
        Save company profile to file.
        
        Args:
            profile: Company profile to save
        """
        try:
            with open(self.company_profile_path, 'w') as f:
                json.dump(profile.dict(), f, indent=2)
            logger.info("Company profile saved")
            
        except Exception as e:
            logger.error(f"Error saving company profile: {str(e)}")
    
    def update_company_profile(self, updates: Dict[str, Any]) -> None:
        """
        Update company profile with new data.
        
        Args:
            updates: Dictionary of updates to apply
        """
        try:
            current_profile = self.load_company_profile()
            current_profile.update(updates)
            
            # Validate with pydantic
            profile = CompanyProfile(**current_profile)
            self.save_company_profile(profile)
            
            logger.info("Company profile updated")
            
        except Exception as e:
            logger.error(f"Error updating company profile: {str(e)}")
    
    def load_vc_database(self) -> List[Dict[str, Any]]:
        """
        Load VC database from file.
        
        Returns:
            List of VC firms as dictionaries
        """
        try:
            if self.vc_database_path.exists():
                with open(self.vc_database_path, 'r') as f:
                    data = json.load(f)
                    return data
            else:
                logger.warning("VC database not found, creating default")
                self._create_default_vc_database()
                return self.load_vc_database()
                
        except Exception as e:
            logger.error(f"Error loading VC database: {str(e)}")
            return []
    
    def save_vc_database(self, vc_firms: List[VCFirm]) -> None:
        """
        Save VC database to file.
        
        Args:
            vc_firms: List of VC firms to save
        """
        try:
            data = [vc.dict() for vc in vc_firms]
            with open(self.vc_database_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info("VC database saved")
            
        except Exception as e:
            logger.error(f"Error saving VC database: {str(e)}")
    
    def add_vc_firm(self, vc_firm: VCFirm) -> None:
        """
        Add a new VC firm to the database.
        
        Args:
            vc_firm: VC firm to add
        """
        try:
            vc_firms = self.load_vc_database()
            vc_firms.append(vc_firm.dict())
            self.save_vc_database([VCFirm(**vc) for vc in vc_firms])
            logger.info(f"Added VC firm: {vc_firm.name}")
            
        except Exception as e:
            logger.error(f"Error adding VC firm: {str(e)}")
    
    def get_template(self, template_name: str) -> Optional[FormTemplate]:
        """
        Get a form template by name.
        
        Args:
            template_name: Name of the template
            
        Returns:
            FormTemplate object if found, None otherwise
        """
        try:
            template_path = self.templates_dir / f"{template_name}.json"
            if template_path.exists():
                with open(template_path, 'r') as f:
                    data = json.load(f)
                    return FormTemplate(**data)
            return None
            
        except Exception as e:
            logger.error(f"Error loading template {template_name}: {str(e)}")
            return None
    
    def save_template(self, template_name: str, template: FormTemplate) -> None:
        """
        Save a form template.
        
        Args:
            template_name: Name of the template
            template: FormTemplate object to save
        """
        try:
            template_path = self.templates_dir / f"{template_name}.json"
            with open(template_path, 'w') as f:
                json.dump(template.dict(), f, indent=2)
            logger.info(f"Template saved: {template_name}")
            
        except Exception as e:
            logger.error(f"Error saving template {template_name}: {str(e)}")
    
    def get_template_mappings(self, template_name: str) -> Dict[str, str]:
        """
        Get field mappings for a template.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Dictionary of field mappings
        """
        template = self.get_template(template_name)
        if template:
            return template.field_mappings
        return {}
    
    def list_templates(self) -> List[str]:
        """
        List all available templates.
        
        Returns:
            List of template names
        """
        try:
            templates = []
            for template_file in self.templates_dir.glob("*.json"):
                templates.append(template_file.stem)
            return templates
            
        except Exception as e:
            logger.error(f"Error listing templates: {str(e)}")
            return []
    
    def export_vc_list_to_csv(self, output_path: str) -> None:
        """
        Export VC database to CSV file.
        
        Args:
            output_path: Path to save CSV file
        """
        try:
            vc_firms = self.load_vc_database()
            
            if not vc_firms:
                logger.warning("No VC firms to export")
                return
            
            # Get all possible fields
            all_fields = set()
            for vc in vc_firms:
                all_fields.update(vc.keys())
            
            fieldnames = sorted(list(all_fields))
            
            with open(output_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for vc in vc_firms:
                    writer.writerow(vc)
            
            logger.info(f"VC database exported to {output_path}")
            
        except Exception as e:
            logger.error(f"Error exporting VC database: {str(e)}")
    
    def import_vc_list_from_csv(self, csv_path: str) -> None:
        """
        Import VC firms from CSV file.
        
        Args:
            csv_path: Path to CSV file
        """
        try:
            vc_firms = []
            
            with open(csv_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Convert string lists to actual lists
                    for key, value in row.items():
                        if key in ['focus_areas', 'investment_stages', 'founders', 'investors']:
                            if value and value.strip():
                                row[key] = [item.strip() for item in value.split(',')]
                            else:
                                row[key] = []
                    
                    vc_firm = VCFirm(**row)
                    vc_firms.append(vc_firm)
            
            self.save_vc_database(vc_firms)
            logger.info(f"Imported {len(vc_firms)} VC firms from {csv_path}")
            
        except Exception as e:
            logger.error(f"Error importing VC database: {str(e)}")
    
    def search_vc_firms(
        self,
        focus_areas: Optional[List[str]] = None,
        investment_stages: Optional[List[str]] = None,
        min_check_size: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search VC firms by criteria.
        
        Args:
            focus_areas: List of focus areas to filter by
            investment_stages: List of investment stages to filter by
            min_check_size: Minimum check size to filter by
            
        Returns:
            List of matching VC firms
        """
        try:
            vc_firms = self.load_vc_database()
            filtered_firms = []
            
            for vc in vc_firms:
                # Filter by focus areas
                if focus_areas:
                    if not any(area in vc.get('focus_areas', []) for area in focus_areas):
                        continue
                
                # Filter by investment stages
                if investment_stages:
                    if not any(stage in vc.get('investment_stages', []) for stage in investment_stages):
                        continue
                
                # Filter by check size (basic implementation)
                if min_check_size:
                    # This is a simplified check - in practice you'd want more sophisticated parsing
                    vc_check_size = vc.get('check_size', '')
                    if vc_check_size and min_check_size > vc_check_size:
                        continue
                
                filtered_firms.append(vc)
            
            return filtered_firms
            
        except Exception as e:
            logger.error(f"Error searching VC firms: {str(e)}")
            return [] 