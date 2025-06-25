from typing import Dict, Any, List, Optional
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

def display_tools_list(companies: List[CompanyInfo]) -> str:
    """Display a numbered list of all tools with key details"""
    if not companies:
        return "No tools to display."
    
    output = [f"\n📋 **Tools List** ({len(companies)} tools)\n"]
    
    for i, company in enumerate(companies, 1):
        # Get key details
        pricing = company.pricing_model or "Unknown"
        open_source = "✅ Open Source" if company.is_open_source else "❌ Proprietary"
        api = "✅ API" if company.api_available else "❌ No API"
        languages = ", ".join(company.language_support[:3]) if company.language_support else "None"
        
        # Truncate description if too long
        description = company.description[:80] + "..." if len(company.description) > 80 else company.description
        
        output.append(f"{i}. **{company.name}**")
        output.append(f"   💰 {pricing} | {open_source} | {api}")
        output.append(f"   🌐 Languages: {languages}")
        output.append(f"   📝 {description}")
        output.append("")
    
    return "\n".join(output)

def compare_two_tools(tool1: CompanyInfo, tool2: CompanyInfo) -> str:
    """Create a detailed side-by-side comparison of two tools"""
    comparison = f"""
## 🔄 **{tool1.name} vs {tool2.name}**

| Feature | {tool1.name} | {tool2.name} |
|---------|{'|'.join(['-' * (len(tool1.name) + 2)])}|{'|'.join(['-' * (len(tool2.name) + 2)])}|
| **Pricing Model** | {tool1.pricing_model or 'Unknown'} | {tool2.pricing_model or 'Unknown'} |
| **Open Source** | {'✅ Yes' if tool1.is_open_source else '❌ No'} | {'✅ Yes' if tool2.is_open_source else '❌ No'} |
| **API Available** | {'✅ Yes' if tool1.api_available else '❌ No'} | {'✅ Yes' if tool2.api_available else '❌ No'} |
| **Website** | {tool1.website} | {tool2.website} |
| **Description** | {tool1.description[:50]}{'...' if len(tool1.description) > 50 else ''} | {tool2.description[:50]}{'...' if len(tool2.description) > 50 else ''} |

### 🗣️ **Language Support**
| {tool1.name} | {tool2.name} |
|{'|'.join(['-' * (len(tool1.name) + 2)])}|{'|'.join(['-' * (len(tool2.name) + 2)])}|
| {', '.join(tool1.language_support) if tool1.language_support else 'None'} | {', '.join(tool2.language_support) if tool2.language_support else 'None'} |

### 🛠️ **Tech Stack**
| {tool1.name} | {tool2.name} |
|{'|'.join(['-' * (len(tool1.name) + 2)])}|{'|'.join(['-' * (len(tool2.name) + 2)])}|
| {', '.join(tool1.tech_stack) if tool1.tech_stack else 'None'} | {', '.join(tool2.tech_stack) if tool2.tech_stack else 'None'} |

### 🔗 **Integrations**
| {tool1.name} | {tool2.name} |
|{'|'.join(['-' * (len(tool1.name) + 2)])}|{'|'.join(['-' * (len(tool2.name) + 2)])}|
| {', '.join(tool1.integration_capabilities) if tool1.integration_capabilities else 'None'} | {', '.join(tool2.integration_capabilities) if tool2.integration_capabilities else 'None'} |

### 📊 **Quick Stats**
| Metric | {tool1.name} | {tool2.name} |
|--------|{'|'.join(['-' * (len(tool1.name) + 2)])}|{'|'.join(['-' * (len(tool2.name) + 2)])}|
| Languages Supported | {len(tool1.language_support)} | {len(tool2.language_support)} |
| Tech Stack Items | {len(tool1.tech_stack)} | {len(tool2.tech_stack)} |
| Integrations | {len(tool1.integration_capabilities)} | {len(tool2.integration_capabilities)} |

### 💡 **Recommendation**
"""
    
    # Add a simple recommendation based on key differences
    recommendations = []
    
    if tool1.pricing_model != tool2.pricing_model:
        if tool1.pricing_model == "Free" and tool2.pricing_model != "Free":
            recommendations.append(f"💰 **Budget-friendly**: {tool1.name} is free while {tool2.name} is {tool2.pricing_model}")
        elif tool2.pricing_model == "Free" and tool1.pricing_model != "Free":
            recommendations.append(f"💰 **Budget-friendly**: {tool2.name} is free while {tool1.name} is {tool1.pricing_model}")
    
    if tool1.is_open_source != tool2.is_open_source:
        if tool1.is_open_source:
            recommendations.append(f"🔓 **Open Source**: {tool1.name} is open source")
        else:
            recommendations.append(f"🔓 **Open Source**: {tool2.name} is open source")
    
    if len(tool1.language_support) != len(tool2.language_support):
        if len(tool1.language_support) > len(tool2.language_support):
            recommendations.append(f"🌐 **Language Support**: {tool1.name} supports more languages ({len(tool1.language_support)} vs {len(tool2.language_support)})")
        else:
            recommendations.append(f"🌐 **Language Support**: {tool2.name} supports more languages ({len(tool2.language_support)} vs {len(tool1.language_support)})")
    
    if len(tool1.integration_capabilities) != len(tool2.integration_capabilities):
        if len(tool1.integration_capabilities) > len(tool2.integration_capabilities):
            recommendations.append(f"🔗 **Integrations**: {tool1.name} has more integrations ({len(tool1.integration_capabilities)} vs {len(tool2.integration_capabilities)})")
        else:
            recommendations.append(f"🔗 **Integrations**: {tool2.name} has more integrations ({len(tool2.integration_capabilities)} vs {len(tool1.integration_capabilities)})")
    
    if recommendations:
        comparison += "\n".join(recommendations)
    else:
        comparison += "Both tools are quite similar in their core features. Consider your specific use case and requirements."
    
    return comparison

def save_comparison_as_markdown(tool1: CompanyInfo, tool2: CompanyInfo) -> str:
    """Save a tool comparison as a standalone Markdown file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comparison_{tool1.name}_vs_{tool2.name}_{timestamp}.md"
    
    # Create the full comparison document
    comparison_doc = f"""# Tool Comparison: {tool1.name} vs {tool2.name}

> Generated on: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

This comparison was generated by the Developer Tools Research Agent.

{compare_two_tools(tool1, tool2)}

---

## 📋 **Individual Tool Details**

### {tool1.name}
{format_tool_summary(tool1.model_dump())}

### {tool2.name}
{format_tool_summary(tool2.model_dump())}

---

*This comparison was automatically generated. For the most up-to-date information, please visit the official websites of both tools.*
"""
    
    with open(filename, 'w') as f:
        f.write(comparison_doc)
    
    return filename

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

def calculate_recommendation_score(company: CompanyInfo, preferences: Dict[str, Any]) -> float:
    """Calculate a recommendation score based on user preferences"""
    score = 0.0
    max_score = 100.0
    
    # Pricing preference (0-25 points)
    if preferences.get('prefer_free') and company.pricing_model == "Free":
        score += 25
    elif preferences.get('prefer_freemium') and company.pricing_model == "Freemium":
        score += 20
    elif preferences.get('prefer_paid') and company.pricing_model in ["Paid", "Enterprise"]:
        score += 15
    
    # Open source preference (0-20 points)
    if preferences.get('prefer_open_source') and company.is_open_source:
        score += 20
    elif preferences.get('prefer_proprietary') and not company.is_open_source:
        score += 15
    
    # API preference (0-15 points)
    if preferences.get('need_api') and company.api_available:
        score += 15
    
    # Language support (0-20 points)
    preferred_languages = preferences.get('languages', [])
    if preferred_languages:
        supported_count = sum(1 for lang in preferred_languages if any(lang.lower() in supported.lower() for supported in company.language_support))
        if supported_count > 0:
            score += (supported_count / len(preferred_languages)) * 20
    
    # Tech stack compatibility (0-10 points)
    preferred_tech = preferences.get('tech_stack', [])
    if preferred_tech:
        tech_matches = sum(1 for tech in preferred_tech if any(tech.lower() in stack.lower() for stack in company.tech_stack))
        if tech_matches > 0:
            score += (tech_matches / len(preferred_tech)) * 10
    
    # Integration needs (0-10 points)
    needed_integrations = preferences.get('integrations', [])
    if needed_integrations:
        integration_matches = sum(1 for integration in needed_integrations if any(integration.lower() in cap.lower() for cap in company.integration_capabilities))
        if integration_matches > 0:
            score += (integration_matches / len(needed_integrations)) * 10
    
    return min(score, max_score)

def get_recommendation_preferences() -> Dict[str, Any]:
    """Interactive function to get user preferences for scoring"""
    print("\n🎯 **Recommendation Preferences**")
    print("Let's customize your tool recommendations:")
    
    preferences = {}
    
    # Pricing preference
    pricing = input("Pricing preference (free/freemium/paid/any): ").lower()
    if pricing == "free":
        preferences['prefer_free'] = True
    elif pricing == "freemium":
        preferences['prefer_freemium'] = True
    elif pricing == "paid":
        preferences['prefer_paid'] = True
    
    # Open source preference
    open_source = input("Open source preference (yes/no/any): ").lower()
    if open_source == "yes":
        preferences['prefer_open_source'] = True
    elif open_source == "no":
        preferences['prefer_proprietary'] = True
    
    # API requirement
    api = input("Need API access? (yes/no): ").lower()
    if api == "yes":
        preferences['need_api'] = True
    
    # Programming languages
    languages = input("Programming languages (comma-separated, e.g., python,javascript): ").strip()
    if languages:
        preferences['languages'] = [lang.strip() for lang in languages.split(',')]
    
    # Tech stack
    tech = input("Tech stack requirements (comma-separated, e.g., docker,aws): ").strip()
    if tech:
        preferences['tech_stack'] = [t.strip() for t in tech.split(',')]
    
    # Integrations
    integrations = input("Required integrations (comma-separated, e.g., github,slack): ").strip()
    if integrations:
        preferences['integrations'] = [i.strip() for i in integrations.split(',')]
    
    return preferences

def score_and_rank_tools(companies: List[CompanyInfo], preferences: Dict[str, Any]) -> List[tuple]:
    """Score and rank tools based on preferences"""
    scored_tools = []
    
    for company in companies:
        score = calculate_recommendation_score(company, preferences)
        scored_tools.append((company, score))
    
    # Sort by score (highest first)
    scored_tools.sort(key=lambda x: x[1], reverse=True)
    
    return scored_tools

def display_scored_recommendations(scored_tools: List[tuple], preferences: Dict[str, Any]) -> str:
    """Display scored recommendations in a nice format"""
    if not scored_tools:
        return "No tools to recommend"
    
    output = ["\n🏆 **Personalized Recommendations**\n"]
    
    # Show preferences used
    pref_summary = []
    if preferences.get('prefer_free'):
        pref_summary.append("Free pricing")
    elif preferences.get('prefer_freemium'):
        pref_summary.append("Freemium pricing")
    elif preferences.get('prefer_paid'):
        pref_summary.append("Paid pricing")
    
    if preferences.get('prefer_open_source'):
        pref_summary.append("Open source")
    elif preferences.get('prefer_proprietary'):
        pref_summary.append("Proprietary")
    
    if preferences.get('need_api'):
        pref_summary.append("API required")
    
    if preferences.get('languages'):
        pref_summary.append(f"Languages: {', '.join(preferences['languages'])}")
    
    if pref_summary:
        output.append(f"Based on: {', '.join(pref_summary)}\n")
    
    # Show ranked tools
    for i, (company, score) in enumerate(scored_tools, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        
        output.append(f"{medal} **{company.name}** - {score:.1f}/100")
        output.append(f"   • {company.pricing_model or 'Unknown pricing'} | {'Open Source' if company.is_open_source else 'Proprietary'}")
        output.append(f"   • API: {'Yes' if company.api_available else 'No'} | Languages: {', '.join(company.language_support[:3])}")
        if company.description:
            output.append(f"   • {company.description[:100]}{'...' if len(company.description) > 100 else ''}")
        output.append("")
    
    return "\n".join(output)

def filter_tools(companies: List[CompanyInfo], 
                 pricing: Optional[str] = None,
                 open_source: Optional[bool] = None,
                 api_available: Optional[bool] = None,
                 language: Optional[str] = None,
                 tech_stack: Optional[str] = None) -> List[CompanyInfo]:
    """Filter tools based on specific criteria"""
    filtered = companies.copy()
    
    if pricing:
        filtered = [c for c in filtered if c.pricing_model and pricing.lower() in c.pricing_model.lower()]
    
    if open_source is not None:
        filtered = [c for c in filtered if c.is_open_source == open_source]
    
    if api_available is not None:
        filtered = [c for c in filtered if c.api_available == api_available]
    
    if language:
        filtered = [c for c in filtered if any(lang.lower() in language.lower() for lang in c.language_support)]
    
    if tech_stack:
        filtered = [c for c in filtered if any(tech.lower() in tech_stack.lower() for tech in c.tech_stack)]
    
    return filtered

def sort_tools(companies: List[CompanyInfo], 
               sort_by: str = "name",
               reverse: bool = False) -> List[CompanyInfo]:
    """Sort tools by different criteria"""
    if sort_by == "name":
        return sorted(companies, key=lambda x: x.name.lower(), reverse=reverse)
    elif sort_by == "pricing":
        # Sort by pricing complexity: Free < Freemium < Paid < Enterprise
        pricing_order = {"Free": 0, "Freemium": 1, "Paid": 2, "Enterprise": 3, "Unknown": 4}
        return sorted(companies, key=lambda x: pricing_order.get(x.pricing_model, 4), reverse=reverse)
    elif sort_by == "languages":
        return sorted(companies, key=lambda x: len(x.language_support), reverse=reverse)
    elif sort_by == "integrations":
        return sorted(companies, key=lambda x: len(x.integration_capabilities), reverse=reverse)
    elif sort_by == "tech_stack":
        return sorted(companies, key=lambda x: len(x.tech_stack), reverse=reverse)
    else:
        return companies

def display_filtered_results(companies: List[CompanyInfo], 
                           original_count: int,
                           filters_applied: List[str]) -> str:
    """Display filtered results with applied filters info"""
    if not companies:
        return f"\n❌ No tools match your filters.\nApplied filters: {', '.join(filters_applied)}"
    
    filter_info = f"\n🔍 **Filtered Results** ({len(companies)}/{original_count} tools)"
    if filters_applied:
        filter_info += f"\nApplied filters: {', '.join(filters_applied)}"
    
    tools_list = "\n".join([f"- **{c.name}**: {c.pricing_model or 'Unknown pricing'} | {'Open Source' if c.is_open_source else 'Proprietary'} | API: {'Yes' if c.api_available else 'No'}" for c in companies])
    
    return f"{filter_info}\n\n{tools_list}"

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