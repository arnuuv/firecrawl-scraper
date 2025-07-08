# Developer Tools Research Agent

An AI-powered tool that researches, analyzes, compares, and scores developer tools to help you make informed decisions.

## 🚀 Features

### Core Research

- **Intelligent Research**: AI-powered tool discovery and analysis
- **Comprehensive Analysis**: Detailed insights into each tool's capabilities
- **Comparison Matrix**: Side-by-side comparison of multiple tools
- **Trend Analysis**: Track tool popularity, community activity, and market position

### Advanced Filtering & Sorting

- **Multi-criteria Filtering**: Filter by pricing, open source status, API availability, programming languages, tech stack
- **Flexible Sorting**: Sort by name, pricing complexity, language support, integrations, tech stack size
- **Smart Search**: Search within tool data using keywords

### Personalized Recommendations

- **Scoring System**: Get personalized tool recommendations based on your preferences
- **Preference Collection**: Interactive preference gathering for accurate scoring
- **Ranked Results**: Tools ranked by relevance to your specific needs

### Detailed Analysis

- **Tool Details**: Get comprehensive information about individual tools
- **Side-by-side Comparison**: Compare two tools in detail
- **Export Comparisons**: Save comparisons as Markdown files for sharing

### Research Templates

- **Pre-defined Scenarios**: 8 research templates for common use cases
- **Customizable Parameters**: Templates with placeholders for customization
- **Guided Research**: Step-by-step research process with best practices
- **Time Estimates**: Know how long each research task will take

### Export & Sharing

- **Multiple Formats**: Export results as JSON or Markdown
- **Comparison Reports**: Generate detailed comparison reports
- **Shareable Outputs**: Easy-to-share research findings

## 📋 Research Templates

The agent includes 8 pre-defined research templates:

1. **Database Comparison** - Compare database solutions for new projects
2. **CI/CD Tools** - Find the best CI/CD pipeline tools
3. **Monitoring Solutions** - Research application monitoring and observability tools
4. **Frontend Frameworks** - Compare modern frontend frameworks
5. **Cloud Providers** - Compare cloud service providers
6. **API Development** - Find tools for API development and management
7. **Testing Frameworks** - Research testing frameworks and tools
8. **Security Tools** - Find security and compliance tools

Each template includes:

- Pre-defined query structure
- Recommended filters and sorting
- Target audience and complexity level
- Estimated research time
- Customizable parameters

## 🛠️ Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd firecrawl-scraper/advanced-agent
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the agent:

```bash
python main.py
```

## 📖 Usage

### Basic Research

```bash
# Start the agent
python main.py

# Enter a query
🔍 Enter a query: "Compare database solutions for web applications"
```

### Using Research Templates

```bash
# Show available templates
templates

# Apply a template by number
template 1

# Apply a template by name
template database

# Customize template parameters when prompted
```

### Filtering and Sorting

```bash
# Filter by criteria
filter pricing=free
filter opensource=true
filter api=true
filter language=python
filter tech=docker

# Sort results
sort name
sort pricing
sort languages
sort integrations
sort tech_stack
```

### Advanced Features

```bash
# Get personalized recommendations
score

# Show tool details
details Supabase
details 1

# Compare two tools
compare Supabase PlanetScale
compare 1 2

# Export comparison
export-compare Supabase PlanetScale

# Search within results
search python
search real-time

# Show trend analysis
trends

# List all tools
list

# Save results
save
```

## 🎯 Research Templates Usage

### Template Categories

**Beginner Level:**

- Frontend Frameworks (6-10 minutes)
- Testing Frameworks (6-10 minutes)

**Intermediate Level:**

- Database Comparison (10-15 minutes)
- CI/CD Tools (8-12 minutes)
- Cloud Providers (15-20 minutes)
- API Development (8-12 minutes)

**Advanced Level:**

- Monitoring Solutions (12-18 minutes)
- Security Tools (12-18 minutes)

### Template Customization

Templates use placeholders that you can customize:

```bash
# Example: Database Comparison template
template 1

# Customize parameters:
Enter database type: NoSQL
Enter use case: real-time analytics

# Generated query: "Compare NoSQL databases for real-time analytics"
```

### Template Features

- **Smart Defaults**: Pre-configured filters and sorting for each use case
- **Best Practices**: Templates follow industry best practices for tool selection
- **Time Optimization**: Focused research that saves time
- **Consistent Results**: Standardized approach for comparable research

## 📊 Output Formats

### Console Output

- Quick statistics and overview
- Detailed analysis and insights
- Comparison matrices
- Trend analysis
- Personalized recommendations

### Export Options

- **JSON**: Machine-readable format for further processing
- **Markdown**: Human-readable format for documentation and sharing

### Comparison Reports

- Side-by-side tool comparisons
- Detailed feature analysis
- Pros and cons for each tool
- Recommendation summary

## 🔧 Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key

# Optional
LOG_LEVEL=INFO
MAX_RESULTS=20
```

### Customization

- Modify templates in `src/utils.py`
- Adjust scoring weights in `src/utils.py`
- Customize prompts in `src/prompts.py`

## 🎨 Example Workflows

### 1. Database Selection for New Project

```bash
# Use database comparison template
template 1
# Enter: database_type=PostgreSQL, use_case=web application

# Filter for open source options
filter opensource=true

# Get personalized recommendations
score

# Compare top choices
compare 1 2

# Export comparison
export-compare 1 2
```

### 2. CI/CD Pipeline Setup

```bash
# Use CI/CD template
template 2
# Enter: language=Python

# Filter for free options
filter pricing=free

# Sort by community activity
sort community_activity

# Show trend analysis
trends
```

### 3. Monitoring Solution Research

```bash
# Use monitoring template
template 3
# Enter: tech_stack=Node.js

# Filter for API availability
filter api=true

# Get detailed analysis
details 1

# Search for specific features
search real-time
```

## 🚀 Advanced Features

### Trend Analysis

- **Popularity Tracking**: Monitor tool popularity over time
- **Community Activity**: Assess developer community engagement
- **Market Position**: Understand competitive landscape
- **Trend Status**: Identify rising, hot, or emerging tools

### Smart Filtering

- **Multi-criteria**: Combine multiple filter criteria
- **Dynamic Results**: Real-time filtering and sorting
- **Context-Aware**: Filters adapt to current results

### Personalized Scoring

- **Preference-Based**: Score tools based on your specific needs
- **Weighted Criteria**: Different importance for different factors
- **Contextual Recommendations**: Recommendations based on use case

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Check the documentation
- Review example usage
- Open an issue on GitHub

---

**Happy Researching! 🚀**
