from typing import Dict, Any
from .models import ComparisonMatrix

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