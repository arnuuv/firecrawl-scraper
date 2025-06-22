from typing import Dict, Any, List
from .models import ComparisonMatrix, CompanyInfo
import json
from datetime import datetime

def display_comparison_matrix(matrix: ComparisonMatrix) -> str:
    """Display comparison matrix in a formatted table"""
    if not matrix or not matrix.tools or not matrix.categories:
        return "No comparison data available"
    
    # Create header
    header = "| Tool | " + " | ".join(matrix.categories) + " |"
    separator = "|------|" + "|".join(["------" for _ in matrix.categories]) + "|"
    
    # Create rows
    rows = []
    for tool in matrix.tools:
        if tool in matrix.matrix:
            values = [matrix.matrix[tool].get(cat, "N/A") for cat in matrix.categories]
            row = f"| {tool} | " + " | ".join(values) + " |"
            rows.append(row)
    
    # Combine all parts
    table = "\n".join([header, separator] + rows)
    
    return f"\n## 📊 Comparison Matrix\n\n{table}\n"

def format_tool_summary(company_data: Dict[str, Any]) -> str:
    """Format individual tool summary into Markdown"""
    summary = f"""
### {company_data.get('name', 'Unknown Tool')}

- **Description**: {company_data.get('description', 'No description available')}
- **Website**: {company_data.get('website', 'N/A')}
- **Pricing**: {company_data.get('pricing_model', 'Unknown')}
- **Open Source**: {'Yes' if company_data.get('is_open_source') else 'No'}
- **API Available**: {'Yes' if company_data.get('api_available') else 'No'}
- **Supported Languages**: {', '.join(company_data.get('language_support', []))}
- **Tech Stack**: {', '.join(company_data.get('tech_stack', []))}
- **Integrations**: {', '.join(company_data.get('integration_capabilities', []))}
"""
    return summary

def generate_quick_stats(companies: List[CompanyInfo]) -> str:
    """Generate quick statistics about analyzed tools"""
    if not companies:
        return "No tools analyzed"
    
    total_tools = len(companies)
    open_source_count = sum(1 for c in companies if c.is_open_source)
    api_available_count = sum(1 for c in companies if c.api_available)
    
    # Count pricing models
    pricing_counts = {}
    for company in companies:
        pricing = company.pricing_model or "Unknown"
        pricing_counts[pricing] = pricing_counts.get(pricing, 0) + 1
    
    # Get most common languages
    all_languages = [lang for company in companies for lang in company.language_support]
    
    language_counts = {}
    for lang in all_languages:
        language_counts[lang] = language_counts.get(lang, 0) + 1
    
    top_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    stats = f"""
## 📈 Quick Stats
- **Total Tools Analyzed**: {total_tools}
- **Open Source**: {open_source_count}/{total_tools} ({open_source_count/total_tools*100:.0f}%)
- **API Available**: {api_available_count}/{total_tools} ({api_available_count/total_tools*100:.0f}%)
- **Pricing Models**: {', '.join([f'{k} ({v})' for k, v in pricing_counts.items()])}
- **Top Languages**: {', '.join([f'{lang} ({count})' for lang, count in top_languages])}
"""
    return stats

def results_to_markdown(result: dict, query: str) -> str:
    """Converts the research results into a Markdown document."""
    markdown_parts = [f"# Research Report for: {query}\n"]
    markdown_parts.append(f"> Generated at: {datetime.now().isoformat()}\n")

    if result.get("companies"):
        stats_str = generate_quick_stats(result["companies"])
        markdown_parts.append(f"\n{stats_str}\n")

    if result.get("analysis"):
        markdown_parts.append("\n## 💡 Analysis & Recommendations\n")
        markdown_parts.append(result["analysis"])

    if result.get("comparison_matrix"):
        matrix_str = display_comparison_matrix(result["comparison_matrix"])
        markdown_parts.append(f"\n{matrix_str}\n")

    if result.get("companies"):
        markdown_parts.append("\n## 🛠️ Detailed Tool Summaries\n")
        for company in result["companies"]:
            summary = format_tool_summary(company.model_dump())
            markdown_parts.append(summary)
            markdown_parts.append("---\n")

    return "\n".join(markdown_parts)

def save_as_markdown(result: dict, query: str) -> str:
    """Saves the research results as a Markdown file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"research_results_{query.replace(' ', '_')}_{timestamp}.md"
    
    markdown_content = results_to_markdown(result, query)
    
    with open(filename, 'w') as f:
        f.write(markdown_content)
    
    return filename

def save_as_json(result: dict, query: str) -> str:
    """Save research results to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"research_results_{query.replace(' ', '_')}_{timestamp}.json"
    
    serializable_result = {}
    for key, value in result.items():
        if hasattr(value, 'model_dump'):
            serializable_result[key] = value.model_dump()
        elif isinstance(value, list) and value and hasattr(value[0], 'model_dump'):
            serializable_result[key] = [item.model_dump() for item in value]
        else:
            serializable_result[key] = value
    
    serializable_result['metadata'] = {
        'query': query,
        'timestamp': timestamp,
        'generated_at': datetime.now().isoformat()
    }
    
    with open(filename, 'w') as f:
        json.dump(serializable_result, f, indent=2)
    
    return filename 