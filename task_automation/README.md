# VC Form Filling AI Agent

An intelligent AI agent that automatically fills out Venture Capital application forms for your company. This agent uses advanced web automation and AI to streamline the VC application process.

## Features

- 🤖 **AI-Powered Form Analysis**: Automatically detects and understands form fields
- 🎯 **Smart Field Mapping**: Maps company data to appropriate form fields
- 🔄 **Multi-Platform Support**: Works with Selenium and Playwright for maximum compatibility
- 📊 **Data Management**: Centralized company and application data storage
- 🛡️ **Anti-Detection**: Uses undetected browsers to avoid bot detection
- 📝 **Template System**: Pre-built templates for common VC applications
- 🔍 **Form Validation**: Ensures all required fields are completed
- 📈 **Progress Tracking**: Monitors application status and success rates

## Quick Start

1. **Install Dependencies**:

   ```bash
   pip install -e .
   ```

2. **Set up Environment**:

   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key and company details
   ```

3. **Configure Company Data**:

   ```bash
   python -m vc_form_agent.config setup
   ```

4. **Run the Agent**:
   ```bash
   python -m vc_form_agent.main --url "https://vc-application-form.com"
   ```

## Configuration

### Company Profile

The agent uses a comprehensive company profile stored in `data/company_profile.json`:

```json
{
  "company_name": "Your Startup Inc.",
  "industry": "SaaS/FinTech",
  "founding_date": "2023-01-15",
  "team_size": 25,
  "funding_stage": "Seed",
  "revenue": 500000,
  "growth_rate": 300,
  "target_market": "SMBs in North America",
  "competitive_advantage": "AI-powered automation platform",
  "use_of_funds": "Product development and market expansion"
}
```

### VC Database

Maintain a database of VC firms and their application processes in `data/vc_database.json`.

## Usage Examples

### Basic Form Filling

```python
from vc_form_agent import FormFillingAgent

agent = FormFillingAgent()
agent.fill_form("https://example-vc.com/apply", headless=False)
```

### Batch Processing

```python
from vc_form_agent import BatchProcessor

processor = BatchProcessor()
processor.process_vc_list("data/vc_targets.csv")
```

### Custom Form Templates

```python
from vc_form_agent.templates import FormTemplate

template = FormTemplate("ycombinator")
template.customize_fields({
    "company_description": "AI-powered SaaS platform...",
    "traction_metrics": "300% YoY growth..."
})
```

## Architecture

```
vc_form_agent/
├── core/
│   ├── agent.py          # Main AI agent logic
│   ├── browser.py        # Browser automation
│   └── form_analyzer.py  # Form field detection
├── data/
│   ├── company_profile.json
│   ├── vc_database.json
│   └── templates/
├── templates/
│   ├── ycombinator.py
│   ├── techstars.py
│   └── generic.py
├── utils/
│   ├── ai_helper.py      # OpenAI integration
│   ├── data_manager.py   # Data handling
│   └── validators.py     # Form validation
└── main.py
```

## Safety & Ethics

- ✅ **Human Oversight**: All applications are reviewed before submission
- ✅ **Rate Limiting**: Respects website terms of service
- ✅ **Data Privacy**: Secure handling of sensitive company information
- ✅ **Transparency**: Clear logging of all actions taken

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub or contact the development team.
