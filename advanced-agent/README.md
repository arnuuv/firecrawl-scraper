# Developer Tools Research Agent

An intelligent agent that researches and compares developer tools, libraries, and technologies using web scraping and AI analysis.

## Features

### 🔍 **Research & Analysis**

- Extracts tool names from articles and documentation
- Researches company websites and official documentation
- Analyzes pricing models, tech stacks, and developer features
- Provides structured analysis of tools and technologies

### 📊 **Comparison Matrix**

- Side-by-side comparison of tools
- Visual table format for easy comparison
- Key categories: Pricing, Open Source, API, Languages, Learning Curve
- Community size and documentation quality assessment

### 🎯 **Interactive Features**

- **Filtering**: Filter tools by pricing, open source status, API availability, language, and tech stack
- **Sorting**: Sort by name, pricing, languages, integrations, or tech stack size
- **Personalized Scoring**: Get recommendations based on your preferences
- **Tool Details**: View detailed summaries of individual tools
- **Side-by-Side Comparison**: Compare two tools in detail
- **Export Comparisons**: Save comparisons as standalone markdown files
- **List View**: Display numbered list of all tools with key details
- **Search Within Results**: Search for keywords across tool data

### 📋 **Comprehensive Reports**

- Executive summaries
- Detailed tool analysis with pros/cons
- Implementation recommendations
- Getting started guides

### 💾 **Save Results**

- Save research results to JSON files
- Export comparisons as markdown files
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

### Interactive Commands

After running a query, you can use these commands:

#### 🔍 **Filtering & Sorting**

```bash
filter pricing=free          # Filter by pricing model
filter opensource=true       # Filter open source tools
filter api=true              # Filter tools with API
filter language=python       # Filter by programming language
filter tech=docker           # Filter by tech stack
sort name                    # Sort by name (A-Z)
sort pricing                 # Sort by pricing complexity
sort languages               # Sort by number of languages
sort integrations            # Sort by number of integrations
sort tech_stack              # Sort by tech stack size
```

#### 🎯 **Analysis & Comparison**

```bash
score                        # Get personalized recommendations
details <name|number>        # Show details for a tool
compare <tool1> <tool2>      # Compare two tools side-by-side
export-compare <tool1> <tool2> # Export comparison as Markdown file
```

#### 📋 **Viewing & Searching**

```bash
list                         # Show numbered list of all tools
search <keyword>             # Search within tool data
clear                        # Clear all filters
help                         # Show help
```

#### 💾 **Saving Results**

```bash
save                         # Save last results (JSON or Markdown)
```

## Output Format

The agent provides multiple types of output:

1. **Report**: Comprehensive analysis with sections
2. **Analysis**: Quick recommendations and insights
3. **Comparison Matrix**: Visual table comparing tools side-by-side
4. **Quick Stats**: Summary of tools analyzed
5. **Filtered Results**: Customized views based on criteria
6. **Scored Recommendations**: Personalized tool rankings
7. **Detailed Comparisons**: Side-by-side tool analysis

## File Structure

```
src/
├── workflow.py      # Main workflow orchestration
├── models.py        # Data models and structures
├── prompts.py       # AI prompts for analysis
├── firecrawl.py     # Web scraping service
└── utils.py         # Utility functions and interactive features
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

### v3.0 - Interactive Features & Enhanced Analysis

- **Interactive Filtering & Sorting**: Filter tools by various criteria and sort results
- **Personalized Scoring**: Get recommendations based on user preferences
- **Tool Details**: View detailed summaries of individual tools
- **Side-by-Side Comparison**: Compare two tools with detailed analysis
- **Export Comparisons**: Save comparisons as standalone markdown files
- **List View**: Display numbered list of all tools
- **Search Within Results**: Search for keywords across tool data
- **Enhanced CLI**: Improved user interface with clear commands and help

### v2.0 - Comparison Matrix Feature

- Added structured comparison matrix generation
- Visual table format for easy tool comparison
- Enhanced data models for better analysis
- Save results functionality
- Improved user interface with emojis and better formatting

## Example Workflow

1. **Run a query**: `"database ORM tools"`
2. **View quick stats**: See summary of analyzed tools
3. **Filter results**: `filter pricing=free` to see free tools
4. **Get recommendations**: `score` for personalized suggestions
5. **Compare tools**: `compare Supabase PlanetScale`
6. **Export comparison**: `export-compare Supabase PlanetScale`
7. **Search within results**: `search python` to find Python-related tools
8. **Save results**: `save` to export all data

The agent provides a comprehensive research experience with powerful filtering, analysis, and export capabilities for developer tool evaluation.
