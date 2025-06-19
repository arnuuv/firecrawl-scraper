#!/usr/bin/env python3
"""
Example Usage of VC Form Filling AI Agent

This script demonstrates how to use the VC form filling agent
for various scenarios.
"""

import asyncio
import json
from pathlib import Path

from vc_form_agent import FormFillingAgent
from vc_form_agent.utils.data_manager import DataManager
from vc_form_agent.templates.ycombinator import YCombinatorTemplate


async def example_single_form():
    """Example: Fill out a single form."""
    print("=== Example: Single Form Filling ===")
    
    # Initialize the agent
    agent = FormFillingAgent(
        headless=False,  # Set to True for production
        browser_type="chrome",
        ai_model="gpt-4"
    )
    
    # Fill out a form
    result = await agent.fill_form(
        url="https://example-vc-form.com/apply",
        template_name="ycombinator",
        validate_before_submit=True,
        take_screenshot=True
    )
    
    print(f"Success: {result.success}")
    print(f"Fields filled: {result.fields_filled}/{result.total_fields}")
    print(f"Errors: {result.errors}")
    
    return result


async def example_batch_processing():
    """Example: Process multiple forms in batch."""
    print("\n=== Example: Batch Processing ===")
    
    # List of VC application URLs
    urls = [
        "https://vc1.com/apply",
        "https://vc2.com/application",
        "https://vc3.com/apply-now"
    ]
    
    # Initialize the agent
    agent = FormFillingAgent(headless=True)
    
    # Process all forms
    results = await agent.batch_process(
        urls=urls,
        template_name="generic",
        delay_between_forms=30
    )
    
    # Print results
    successful = sum(1 for r in results if r.success)
    print(f"Successfully filled {successful}/{len(urls)} forms")
    
    return results


def example_company_profile_setup():
    """Example: Set up company profile."""
    print("\n=== Example: Company Profile Setup ===")
    
    # Initialize data manager
    data_manager = DataManager()
    
    # Company profile data
    company_data = {
        "company_name": "TechStartup Inc.",
        "industry": "SaaS/FinTech",
        "founding_date": "2023-01-15",
        "team_size": 25,
        "funding_stage": "Seed",
        "revenue": 500000,
        "growth_rate": 300,
        "target_market": "SMBs in North America",
        "competitive_advantage": "AI-powered automation platform that reduces manual work by 80%",
        "use_of_funds": "Product development (60%), market expansion (25%), team growth (15%)",
        "website": "https://techstartup.com",
        "email": "founder@techstartup.com",
        "phone": "+1-555-0123",
        "address": "123 Startup St, San Francisco, CA 94105",
        "founders": ["John Doe", "Jane Smith"],
        "investors": ["Angel Investor 1", "Angel Investor 2"],
        "traction_metrics": {
            "monthly_recurring_revenue": 50000,
            "customer_count": 500,
            "churn_rate": 0.05,
            "customer_acquisition_cost": 150
        },
        "financials": {
            "burn_rate": 75000,
            "runway_months": 8,
            "total_funding": 1000000
        }
    }
    
    # Save company profile
    data_manager.update_company_profile(company_data)
    print("Company profile saved successfully!")
    
    # Display profile
    profile = data_manager.load_company_profile()
    print(f"Company: {profile['company_name']}")
    print(f"Industry: {profile['industry']}")
    print(f"Team Size: {profile['team_size']}")
    print(f"Revenue: ${profile['revenue']:,}")


def example_vc_database_management():
    """Example: Manage VC database."""
    print("\n=== Example: VC Database Management ===")
    
    # Initialize data manager
    data_manager = DataManager()
    
    # Add VC firms
    vc_firms = [
        {
            "name": "Y Combinator",
            "website": "https://ycombinator.com",
            "application_url": "https://apply.ycombinator.com",
            "focus_areas": ["Technology", "SaaS", "AI/ML"],
            "investment_stages": ["Seed", "Series A"],
            "check_size": "$500K - $2M",
            "application_deadline": "2024-03-15"
        },
        {
            "name": "Techstars",
            "website": "https://techstars.com",
            "application_url": "https://apply.techstars.com",
            "focus_areas": ["Technology", "Innovation"],
            "investment_stages": ["Seed", "Early Stage"],
            "check_size": "$100K - $500K"
        },
        {
            "name": "500 Startups",
            "website": "https://500.co",
            "application_url": "https://500.co/apply",
            "focus_areas": ["Technology", "Diverse Founders"],
            "investment_stages": ["Seed", "Series A"],
            "check_size": "$150K - $500K"
        }
    ]
    
    # Save VC firms
    from vc_form_agent.utils.data_manager import VCFirm
    vc_objects = [VCFirm(**vc) for vc in vc_firms]
    data_manager.save_vc_database(vc_objects)
    
    print(f"Added {len(vc_firms)} VC firms to database")
    
    # Search VC firms
    results = data_manager.search_vc_firms(
        focus_areas=["Technology"],
        investment_stages=["Seed"]
    )
    
    print(f"Found {len(results)} VC firms matching criteria")
    for vc in results:
        print(f"  - {vc['name']}: {vc['check_size']}")


def example_template_usage():
    """Example: Using form templates."""
    print("\n=== Example: Template Usage ===")
    
    # Create Y Combinator template
    yc_template = YCombinatorTemplate("ycombinator")
    
    # Customize template
    yc_template.customize_for_yc_batch("winter")
    
    # Get template info
    template_info = yc_template.get_template_info()
    print(f"Template: {template_info['name']}")
    print(f"Fields: {template_info['field_mappings']}")
    print(f"Required: {template_info['required_fields']}")
    
    # Get application tips
    tips = yc_template.get_yc_application_tips()
    print("\nApplication Tips:")
    for i, tip in enumerate(tips[:5], 1):
        print(f"  {i}. {tip}")


async def example_ai_enhanced_filling():
    """Example: AI-enhanced form filling."""
    print("\n=== Example: AI-Enhanced Form Filling ===")
    
    # Initialize agent with AI
    agent = FormFillingAgent(
        headless=False,
        ai_model="gpt-4"
    )
    
    # Custom field mappings
    custom_fields = {
        "company_description": "AI-powered SaaS platform that automates business processes",
        "traction_metrics": "300% YoY growth, 500 customers, $50K MRR",
        "competitive_advantage": "Proprietary AI algorithms, 80% time savings, enterprise-grade security"
    }
    
    # Fill form with custom fields
    result = await agent.fill_form(
        url="https://example-vc.com/apply",
        custom_fields=custom_fields,
        validate_before_submit=True
    )
    
    print(f"AI-enhanced form filling completed: {result.success}")
    return result


def example_data_export():
    """Example: Export data to different formats."""
    print("\n=== Example: Data Export ===")
    
    data_manager = DataManager()
    
    # Export VC database to CSV
    csv_path = "vc_database_export.csv"
    data_manager.export_vc_list_to_csv(csv_path)
    print(f"VC database exported to {csv_path}")
    
    # Export company profile
    profile = data_manager.load_company_profile()
    profile_path = "company_profile.json"
    with open(profile_path, 'w') as f:
        json.dump(profile, f, indent=2)
    print(f"Company profile exported to {profile_path}")


async def main():
    """Run all examples."""
    print("VC Form Filling AI Agent - Examples")
    print("=" * 50)
    
    try:
        # Set up data
        example_company_profile_setup()
        example_vc_database_management()
        example_template_usage()
        
        # Run form filling examples (commented out to avoid actual form submission)
        # await example_single_form()
        # await example_batch_processing()
        # await example_ai_enhanced_filling()
        
        # Export data
        example_data_export()
        
        print("\n✅ All examples completed successfully!")
        print("\nTo run actual form filling, uncomment the form filling examples")
        print("and provide real VC application URLs.")
        
    except Exception as e:
        print(f"❌ Error running examples: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main()) 