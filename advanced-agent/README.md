# Developer Tools Research Agent

An intelligent agent that researches and compares developer tools, libraries, and technologies using web scraping and AI analysis.

## Features

### 🔍 **Research & Analysis**

- Extracts tool names from articles and documentation
- Researches company websites and official documentation
- Analyzes pricing models, tech stacks, and developer features
- Provides structured analysis of tools and technologies

### 📊 **Comparison Matrix**

- **NEW**: Side-by-side comparison of tools
- Visual table format for easy comparison
- Key categories: Pricing, Open Source, API, Languages, Learning Curve
- Community size and documentation quality assessment

### 📋 **Comprehensive Reports**

- Executive summaries
- Detailed tool analysis with pros/cons
- Implementation recommendations
- Getting started guides

### 💾 **Save Results**

- **NEW**: Save research results to JSON files
- Timestamped files for easy organization
- Complete data export including comparison matrices

## Usage

```bash
python main.py
```

### Example Queries

- "database ORM tools"
- "deployment platforms"
- "authentication services"
- "monitoring tools"
- "CI/CD platforms"

## Output Format

The agent provides three types of output:

1. **Report**: Comprehensive analysis with sections
2. **Analysis**: Quick recommendations and insights
3. **Comparison Matrix**: Visual table comparing tools side-by-side

## File Structure

```
src/
├── workflow.py      # Main workflow orchestration
├── models.py        # Data models and structures
├── prompts.py       # AI prompts for analysis
├── firecrawl.py     # Web scraping service
└── utils.py         # Utility functions (NEW)
```

## Requirements

- Python 3.8+
- OpenAI API key
- Firecrawl API key
- Required packages in `pyproject.toml`

## Configuration

Set up your environment variables:

```bash
OPENAI_API_KEY=your_openai_key
FIRECRAWL_API_KEY=your_firecrawl_key
```

## Recent Updates

### v2.0 - Comparison Matrix Feature

- Added structured comparison matrix generation
- Visual table format for easy tool comparison
- Enhanced data models for better analysis
- Save results functionality
- Improved user interface with emojis and better formatting

