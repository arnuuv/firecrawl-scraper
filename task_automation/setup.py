#!/usr/bin/env python3
"""
Setup script for VC Form Filling AI Agent

This script helps users set up the agent with their company information
and configure the necessary environment variables.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

def get_user_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def create_env_file():
    """Create .env file with user configuration."""
    print("🔧 Setting up environment configuration...")
    
    # Check if .env already exists
    env_path = Path(".env")
    if env_path.exists():
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Skipping .env creation.")
            return
    
    # Get OpenAI API key
    print("\n📝 OpenAI Configuration:")
    openai_key = get_user_input("Enter your OpenAI API key")
    if not openai_key:
        print("❌ OpenAI API key is required!")
        return
    
    # Get browser preferences
    print("\n🌐 Browser Configuration:")
    browser_type = get_user_input("Browser type", "chrome")
    headless = get_user_input("Run in headless mode? (y/N)", "y").lower() == 'y'
    
    # Get form filling preferences
    print("\n📋 Form Filling Configuration:")
    delay = get_user_input("Delay between forms (seconds)", "30")
    take_screenshots = get_user_input("Take screenshots? (Y/n)", "y").lower() != 'n'
    validate_forms = get_user_input("Validate forms before submission? (Y/n)", "y").lower() != 'n'
    
    # Create .env content
    env_content = f"""# VC Form Filling AI Agent Configuration

# OpenAI API Configuration
OPENAI_API_KEY={openai_key}
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.1

# Browser Configuration
BROWSER_TYPE={browser_type}
HEADLESS_MODE={'true' if headless else 'false'}
BROWSER_TIMEOUT=30
USE_UNDETECTED_CHROME=true

# Form Filling Configuration
MAX_RETRIES=3
DELAY_BETWEEN_FORMS={delay}
TAKE_SCREENSHOTS={'true' if take_screenshots else 'false'}
VALIDATE_BEFORE_SUBMIT={'true' if validate_forms else 'false'}

# Data Directory
DATA_DIR=data
SCREENSHOTS_DIR=screenshots

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=vc_form_agent.log

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=10
RATE_LIMIT_DELAY_BETWEEN_REQUESTS=6

# Anti-Detection
USER_AGENT_ROTATION=true
PROXY_ENABLED=false
PROXY_URL=

# Development Mode
DEBUG_MODE=false
DRY_RUN=false
"""
    
    # Write .env file
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("✅ Environment configuration saved to .env")

def create_company_profile():
    """Create company profile with user input."""
    print("\n🏢 Setting up company profile...")
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    profile_path = data_dir / "company_profile.json"
    
    # Check if profile already exists
    if profile_path.exists():
        overwrite = input("⚠️  Company profile already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Skipping company profile creation.")
            return
    
    print("\n📝 Company Information:")
    
    # Required fields
    company_name = get_user_input("Company name")
    industry = get_user_input("Industry/sector")
    founding_date = get_user_input("Founding date (YYYY-MM-DD)")
    team_size = get_user_input("Team size")
    funding_stage = get_user_input("Funding stage (idea, seed, series_a, etc.)")
    email = get_user_input("Contact email")
    
    # Optional fields
    website = get_user_input("Company website (optional)")
    revenue = get_user_input("Annual revenue (optional)")
    growth_rate = get_user_input("Growth rate % (optional)")
    target_market = get_user_input("Target market (optional)")
    competitive_advantage = get_user_input("Competitive advantage (optional)")
    use_of_funds = get_user_input("Use of funds (optional)")
    
    # Create profile
    profile = {
        "company_name": company_name,
        "industry": industry,
        "founding_date": founding_date,
        "team_size": int(team_size) if team_size.isdigit() else 1,
        "funding_stage": funding_stage,
        "email": email,
        "website": website if website else None,
        "revenue": float(revenue) if revenue and revenue.replace('.', '').isdigit() else None,
        "growth_rate": float(growth_rate) if growth_rate and growth_rate.replace('.', '').isdigit() else None,
        "target_market": target_market if target_market else "To be defined",
        "competitive_advantage": competitive_advantage if competitive_advantage else "To be defined",
        "use_of_funds": use_of_funds if use_of_funds else "To be defined"
    }
    
    # Remove None values
    profile = {k: v for k, v in profile.items() if v is not None}
    
    # Save profile
    with open(profile_path, 'w') as f:
        json.dump(profile, f, indent=2)
    
    print("✅ Company profile saved to data/company_profile.json")

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        import subprocess
        
        # Check if pip is available
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
        
        # Install from requirements.txt
        if Path("requirements.txt").exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ Dependencies installed successfully")
        else:
            print("⚠️  requirements.txt not found, installing core dependencies...")
            core_deps = [
                "selenium>=4.15.0",
                "playwright>=1.40.0", 
                "openai>=1.3.0",
                "python-dotenv>=1.0.0",
                "pydantic>=2.5.0",
                "requests>=2.31.0",
                "beautifulsoup4>=4.12.0",
                "loguru>=0.7.0",
                "rich>=13.7.0",
                "click>=8.1.0"
            ]
            for dep in core_deps:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            print("✅ Core dependencies installed successfully")
        
        # Install Playwright browsers
        print("🌐 Installing Playwright browsers...")
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print("✅ Playwright browsers installed")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("Please install dependencies manually: pip install -r requirements.txt")
    except ImportError:
        print("❌ pip not available. Please install dependencies manually.")

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    
    directories = ["data", "screenshots", "logs", "data/templates"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✅ Created {directory}/")

def show_next_steps():
    """Show next steps for the user."""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Review and edit your company profile: data/company_profile.json")
    print("2. Add VC firms to the database: python -m vc_form_agent.main add-vc")
    print("3. Test with a single form: python -m vc_form_agent.main fill-form --url <form_url>")
    print("4. Run batch processing: python -m vc_form_agent.main batch-process --csv-file <urls.csv>")
    print("\n📚 Documentation:")
    print("- Read README.md for detailed usage instructions")
    print("- Run 'python example_usage.py' to see examples")
    print("- Use 'python -m vc_form_agent.main --help' for command help")

def main():
    """Main setup function."""
    print("🚀 VC Form Filling AI Agent Setup")
    print("=" * 50)
    
    try:
        # Create directories
        create_directories()
        
        # Install dependencies
        install_dependencies()
        
        # Create environment file
        create_env_file()
        
        # Create company profile
        create_company_profile()
        
        # Show next steps
        show_next_steps()
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 