from typing import Dict, Any, List
from .models import ComparisonMatrix, CompanyInfo

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
    
    return f"\n## Comparison Matrix\n\n{table}\n"

def format_tool_summary(company_data: Dict[str, Any]) -> str:
    """Format individual tool summary"""
    summary = f"""
### {company_data.get('name', 'Unknown Tool')}

**Description:** {company_data.get('description', 'No description available')}
**Website:** {company_data.get('website', 'N/A')}
**Pricing:** {company_data.get('pricing_model', 'Unknown')}
**Open Source:** {'Yes' if company_data.get('is_open_source') else 'No'}
**API Available:** {'Yes' if company_data.get('api_available') else 'No'}

**Supported Languages:** {', '.join(company_data.get('language_support', []))}
**Tech Stack:** {', '.join(company_data.get('tech_stack', []))}
**Integrations:** {', '.join(company_data.get('integration_capabilities', []))}
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
    all_languages = []
    for company in companies:
        all_languages.extend(company.language_support)
    
    language_counts = {}
    for lang in all_languages:
        language_counts[lang] = language_counts.get(lang, 0) + 1
    
    top_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    stats = f"""
📈 **Quick Stats**
• Total Tools Analyzed: {total_tools}
• Open Source: {open_source_count}/{total_tools} ({open_source_count/total_tools*100:.0f}%)
• API Available: {api_available_count}/{total_tools} ({api_available_count/total_tools*100:.0f}%)
• Pricing Models: {', '.join([f'{k} ({v})' for k, v in pricing_counts.items()])}
• Top Languages: {', '.join([f'{lang} ({count})' for lang, count in top_languages])}
"""
    return stats 