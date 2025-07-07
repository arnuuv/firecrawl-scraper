# 🚀 Developer Tools Research Agent

An advanced AI-powered research agent that analyzes developer tools, provides detailed comparisons, and offers personalized recommendations. Built with LangGraph, Firecrawl, and OpenAI.

## ✨ Features

### 🔍 Core Research

- **Web Scraping**: Automatically scrapes and analyzes developer tool websites
- **Intelligent Analysis**: AI-powered analysis of tool features, pricing, and capabilities
- **Comparison Matrix**: Side-by-side comparison of multiple tools
- **Trend Analysis**: Track tool popularity, community activity, and market position

### 📊 Data Export & Management

- **JSON Export**: Save research results in structured JSON format
- **Markdown Export**: Generate comprehensive Markdown reports
- **Comparison Export**: Export side-by-side comparisons as standalone files

### 🎯 Advanced Filtering & Search

- **Multi-criteria Filtering**: Filter by pricing, open source status, API availability, language, tech stack
- **Smart Sorting**: Sort by name, pricing complexity, languages, integrations, tech stack size
- **Keyword Search**: Search within tool descriptions, features, and metadata
- **Personalized Scoring**: Get recommendations based on your preferences

### 🔧 Interactive Features

- **Tool Details**: View detailed summaries of individual tools
- **Side-by-side Comparison**: Compare any two tools with detailed analysis
- **Numbered List View**: Browse all tools with key details
- **Trend Insights**: View trending tools and market analysis

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- OpenAI API key

### Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd firecrawl-scraper/advanced-agent
   ```

2. **Install dependencies**:

   ```bash
   pip install -e .
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🚀 Usage

### Basic Usage

```bash
python main.py
```

### Available Commands

#### 🔍 Research Commands

- **Query**: Enter any research question about developer tools
  ```
  > database tools for startups
  > python web frameworks
  > real-time collaboration tools
  ```

#### 📊 Data Management

- **`save`**: Save current results (JSON or Markdown format)
- **`list`**: Show numbered list of all tools
- **`clear`**: Clear all applied filters

#### 🔍 Search & Filter

- **`search <keyword>`**: Search within tool data

  ```
  > search python
  > search docker
  > search real-time
  ```

- **`filter <criteria>`**: Filter tools by specific criteria

  ```
  > filter pricing=free
  > filter opensource=true
  > filter api=true
  > filter language=python
  > filter tech=docker
  ```

- **`sort <field>`**: Sort tools by specific fields
  ```
  > sort name
  > sort pricing
  > sort languages
  > sort integrations
  > sort tech_stack
  ```

#### 🎯 Analysis & Comparison

- **`score`**: Get personalized recommendations based on preferences
- **`details <name|number>`**: Show detailed information about a specific tool

  ```
  > details Supabase
  > details 1
  ```

- **`compare <tool1> <tool2>`**: Compare two tools side-by-side

  ```
  > compare Supabase PlanetScale
  > compare 1 2
  ```

- **`export-compare <tool1> <tool2>`**: Export comparison as Markdown file

  ```
  > export-compare Supabase PlanetScale
  > export-compare 1 2
  ```

- **`trends`**: Show trend analysis and market insights

#### 📚 Help

- **`help`**: Show detailed help for all commands
- **`exit`**: Exit the application

## 📁 Project Structure

```
advanced-agent/
├── main.py              # Main application entry point
├── pyproject.toml       # Project dependencies and metadata
├── README.md           # This file
└── src/
    ├── __init__.py
    ├── firecrawl.py    # Firecrawl web scraping integration
    ├── models.py       # Pydantic data models
    ├── prompts.py      # AI prompts and templates
    ├── utils.py        # Utility functions and helpers
    └── workflow.py     # LangGraph workflow definition
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Customization

You can customize the AI prompts in `src/prompts.py` to adjust the analysis style and depth.

## 📊 Output Formats

### JSON Export

```json
{
  "companies": [...],
  "analysis": "...",
  "comparison_matrix": {...},
  "metadata": {
    "query": "...",
    "timestamp": "...",
    "generated_at": "..."
  }
}
```

### Markdown Export

- Comprehensive tool analysis
- Feature comparisons
- Pricing information
- Integration details
- Recommendations

## 🎯 Example Workflows

### 1. Database Tool Research

```
> database tools for startups
> filter pricing=free
> sort integrations
> compare Supabase PlanetScale
> export-compare Supabase PlanetScale
```

### 2. Framework Comparison

```
> python web frameworks
> filter language=python
> score
> details FastAPI
> trends
```

### 3. Real-time Tools Analysis

```
> real-time collaboration tools
> search websocket
> filter api=true
> list
> save
```

## 🔍 Advanced Features

### Trend Analysis

The agent tracks:

- **Popularity Score**: Tool adoption and usage trends
- **Community Activity**: GitHub stars, contributors, recent updates
- **Market Position**: Competitive analysis and positioning
- **Trend Status**: Rising, Hot, Emerging, or Stable

### Personalized Scoring

Get recommendations based on:

- **Budget**: Free vs paid preferences
- **Team Size**: Startup vs enterprise needs
- **Tech Stack**: Preferred languages and frameworks
- **Use Case**: Specific project requirements

### Smart Filtering

Filter by multiple criteria:

- **Pricing Models**: Free, Freemium, Paid, Enterprise
- **Open Source**: Open source vs proprietary
- **API Availability**: REST API, GraphQL, SDK availability
- **Programming Languages**: Python, JavaScript, Go, etc.
- **Tech Stack**: Docker, Kubernetes, AWS, etc.

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed

   ```bash
   pip install -e .
   ```

2. **API Key Issues**: Verify your OpenAI API key is set in `.env`

3. **Scraping Errors**: Some websites may block automated scraping. The agent will handle this gracefully.

### Getting Help

- Use the `help` command for detailed command information
- Check the console output for error messages
- Ensure your OpenAI API key has sufficient credits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Web scraping powered by [Firecrawl](https://firecrawl.dev)
- AI capabilities provided by [OpenAI](https://openai.com)
- Data models built with [Pydantic](https://pydantic.dev)

---

**Happy researching! 🚀**

