from dotenv import load_dotenv
from src.workflow import Workflow
from src.utils import (
    display_comparison_matrix, 
    generate_quick_stats, 
    save_as_json, 
    save_as_markdown,
    filter_tools,
    sort_tools,
    display_filtered_results,
    get_recommendation_preferences,
    score_and_rank_tools,
    display_scored_recommendations,
    format_tool_summary,
    compare_two_tools,
    save_comparison_as_markdown,
    display_tools_list,
    search_within_tools,
    display_search_results,
    get_research_templates,
    display_research_templates,
    apply_research_template,
    search_templates_by_name
)
import json
from datetime import datetime
import os

load_dotenv()

def show_filter_help():
    """Display help for filtering and sorting commands"""
    print("""
🔍 **Filtering & Sorting Commands:**
- filter pricing=free          # Filter by pricing model
- filter opensource=true       # Filter open source tools
- filter api=true              # Filter tools with API
- filter language=python       # Filter by programming language
- filter tech=docker           # Filter by tech stack
- sort name                    # Sort by name (A-Z)
- sort pricing                 # Sort by pricing complexity
- sort languages               # Sort by number of languages
- sort integrations            # Sort by number of integrations
- sort tech_stack              # Sort by tech stack size
- score                        # Get personalized recommendations
- details <name|number>        # Show details for a tool
- compare <tool1> <tool2>      # Compare two tools side-by-side
- export-compare <tool1> <tool2> # Export comparison as Markdown file
- list                         # Show numbered list of all tools
- search <keyword>             # Search within tool data
- trends                       # Show trend analysis and insights
- templates                    # Show research templates
- template <number|name>       # Apply a research template
- clear                        # Clear all filters
- help                         # Show this help
""")

def parse_filter_command(command: str, companies: list) -> tuple:
    """Parse filter command and return filtered companies"""
    parts = command.lower().split()
    if len(parts) < 2:
        return companies, []
    
    filters_applied = []
    filtered = companies.copy()
    
    if parts[0] == "filter":
        if "pricing=" in command:
            pricing = command.split("pricing=")[1].split()[0]
            filtered = filter_tools(filtered, pricing=pricing)
            filters_applied.append(f"pricing={pricing}")
        
        if "opensource=" in command:
            open_source = "true" in command.lower()
            filtered = filter_tools(filtered, open_source=open_source)
            filters_applied.append(f"opensource={open_source}")
        
        if "api=" in command:
            api_available = "true" in command.lower()
            filtered = filter_tools(filtered, api_available=api_available)
            filters_applied.append(f"api={api_available}")
        
        if "language=" in command:
            language = command.split("language=")[1].split()[0]
            filtered = filter_tools(filtered, language=language)
            filters_applied.append(f"language={language}")
        
        if "tech=" in command:
            tech = command.split("tech=")[1].split()[0]
            filtered = filter_tools(filtered, tech_stack=tech)
            filters_applied.append(f"tech={tech}")
    
    elif parts[0] == "sort":
        sort_by = parts[1] if len(parts) > 1 else "name"
        reverse = "reverse" in command.lower()
        filtered = sort_tools(filtered, sort_by=sort_by, reverse=reverse)
        filters_applied.append(f"sort={sort_by}{' reverse' if reverse else ''}")
    
    return filtered, filters_applied


    
def show_tool_details(companies, arg):
    """Show details for a tool by name or number."""
    if not companies:
        print("No tools to show details for.")
        return
    if arg.isdigit():
        idx = int(arg) - 1
        if 0 <= idx < len(companies):
            print(format_tool_summary(companies[idx].model_dump()))
        else:
            print(f"No tool at position {arg}.")
    else:
        matches = [c for c in companies if c.name.lower() == arg.lower()]
        if matches:
            print(format_tool_summary(matches[0].model_dump()))
        else:
            print(f"No tool found with name '{arg}'.")

def compare_tools(companies, command):
    """Compare two tools by name or number."""
    if not companies:
        print("No tools to compare.")
        return
    
    # Extract tool names/numbers from command
    parts = command.split()
    if len(parts) < 3:
        print("Usage: compare <tool1> <tool2>")
        print("Example: compare Supabase PlanetScale")
        print("Example: compare 1 2")
        return
    
    tool1_arg = parts[1]
    tool2_arg = parts[2]
    
    # Find first tool
    tool1 = None
    if tool1_arg.isdigit():
        idx = int(tool1_arg) - 1
        if 0 <= idx < len(companies):
            tool1 = companies[idx]
        else:
            print(f"No tool at position {tool1_arg}.")
            return
    else:
        matches = [c for c in companies if c.name.lower() == tool1_arg.lower()]
        if matches:
            tool1 = matches[0]
        else:
            print(f"No tool found with name '{tool1_arg}'.")
            return
    
    # Find second tool
    tool2 = None
    if tool2_arg.isdigit():
        idx = int(tool2_arg) - 1
        if 0 <= idx < len(companies):
            tool2 = companies[idx]
        else:
            print(f"No tool at position {tool2_arg}.")
            return
    else:
        matches = [c for c in companies if c.name.lower() == tool2_arg.lower()]
        if matches:
            tool2 = matches[0]
        else:
            print(f"No tool found with name '{tool2_arg}'.")
            return
    
    # Compare the tools
    comparison = compare_two_tools(tool1, tool2)
    print(comparison)

def export_comparison(companies, command):
    """Export a tool comparison as a Markdown file."""
    if not companies:
        print("No tools to compare.")
        return
    
    # Extract tool names/numbers from command
    parts = command.split()
    if len(parts) < 3:
        print("Usage: export-compare <tool1> <tool2>")
        print("Example: export-compare Supabase PlanetScale")
        print("Example: export-compare 1 2")
        return
    
    tool1_arg = parts[1]
    tool2_arg = parts[2]
    
    # Find first tool
    tool1 = None
    if tool1_arg.isdigit():
        idx = int(tool1_arg) - 1
        if 0 <= idx < len(companies):
            tool1 = companies[idx]
        else:
            print(f"No tool at position {tool1_arg}.")
            return
    else:
        matches = [c for c in companies if c.name.lower() == tool1_arg.lower()]
        if matches:
            tool1 = matches[0]
        else:
            print(f"No tool found with name '{tool1_arg}'.")
            return
    
    # Find second tool
    tool2 = None
    if tool2_arg.isdigit():
        idx = int(tool2_arg) - 1
        if 0 <= idx < len(companies):
            tool2 = companies[idx]
        else:
            print(f"No tool at position {tool2_arg}.")
            return
    else:
        matches = [c for c in companies if c.name.lower() == tool2_arg.lower()]
        if matches:
            tool2 = matches[0]
        else:
            print(f"No tool found with name '{tool2_arg}'.")
            return
    
    # Export the comparison
    try:
        filename = save_comparison_as_markdown(tool1, tool2)
        print(f"📄 Comparison exported to: {filename}")
        print(f"📊 Comparing: {tool1.name} vs {tool2.name}")
    except Exception as e:
        print(f"❌ Error exporting comparison: {e}")

def search_tools(companies, command):
    """Search within tool data for specific keywords."""
    if not companies:
        print("No tools to search in.")
        return
    
    # Extract search term from command
    parts = command.split()
    if len(parts) < 2:
        print("Usage: search <keyword>")
        print("Example: search python")
        print("Example: search docker")
        print("Example: search real-time")
        return
    
    search_term = " ".join(parts[1:])
    
    # Perform the search
    search_matches = search_within_tools(companies, search_term)
    search_results = display_search_results(search_matches, search_term, len(companies))
    print(search_results)

def handle_template_command(command: str) -> tuple:
    """Handle template commands and return query and template info"""
    parts = command.lower().split()
    if len(parts) < 2:
        return None, None
    
    template_arg = parts[1]
    templates = get_research_templates()
    
    # Try to find template by number
    if template_arg.isdigit():
        idx = int(template_arg) - 1
        if 0 <= idx < len(templates):
            template = templates[idx]
        else:
            print(f"❌ No template at position {template_arg}")
            return None, None
    else:
        # Try to find template by name
        matches = search_templates_by_name(templates, template_arg)
        if len(matches) == 1:
            template = matches[0]
        elif len(matches) > 1:
            print(f"🔍 Multiple templates found for '{template_arg}':")
            for i, match in enumerate(matches, 1):
                print(f"  {i}. {match.name} - {match.description}")
            return None, None
        else:
            print(f"❌ No template found matching '{template_arg}'")
            return None, None
    
    # Get custom parameters from user
    custom_params = {}
    print(f"\n📋 Applying template: {template.name}")
    print(f"📝 Description: {template.description}")
    print(f"🎯 Use Case: {template.use_case}")
    
    # Extract placeholders from query template
    import re
    placeholders = re.findall(r'\{(\w+)\}', template.query_template)
    
    if placeholders:
        print(f"\n🔧 Customize template parameters:")
        for placeholder in placeholders:
            value = input(f"  Enter {placeholder.replace('_', ' ')}: ").strip()
            if value:
                custom_params[placeholder] = value
    
    # Apply template
    template_result = apply_research_template(template, custom_params)
    query = template_result["query"]
    template_info = template_result["template_info"]
    
    print(f"\n🚀 Generated query: {query}")
    if template_result["filters"]:
        print(f"🔍 Applied filters: {template_result['filters']}")
    if template_result["sort_by"]:
        print(f"📈 Sort by: {template_result['sort_by']}")
    
    return query, template_info

def main():
    workflow = Workflow()
    print("🚀 Developer Tools Research Agent")
    print("Features: Research, Analysis, Report, Comparison Matrix, MD/JSON Export, Filtering, Scoring, Details, Compare, Export Compare, List, Search, Trend Analysis, Research Templates")
    print("Commands: 'exit' to quit, 'save' to save last result, 'filter' to filter results, 'score' for recommendations, 'details <name|number>' for tool details, 'compare <tool1> <tool2>' for side-by-side comparison, 'export-compare <tool1> <tool2>' to save comparison as file, 'list' to show all tools, 'search <keyword>' to search within results, 'trends' for trend analysis, 'templates' to show research templates, 'template <number|name>' to apply a template")
    
    last_result = None
    last_companies = None
    original_companies = None
    current_preferences = None
    
    while True:
        if last_companies:
            print(f"\n📊 Current results: {len(last_companies)} tools")
            command = input("🔍 Enter query, 'filter <criteria>', 'sort <field>', 'score', 'details <name|number>', 'compare <tool1> <tool2>', 'export-compare <tool1> <tool2>', 'list', 'search <keyword>', 'trends', 'templates', 'template <number|name>', 'save', or 'exit': ")
        else:
            command = input("\n🔍 Enter a query (or 'exit' to quit): ")
        
        if command.lower() == "exit":
            print("👋 Exiting...")
            break
        
        if command.lower() == "help":
            show_filter_help()
            continue
            
        if command.lower() == "clear":
            if original_companies:
                last_companies = original_companies.copy()
                print("🧹 Filters cleared!")
            continue
            
        if command.lower() == "templates":
            templates = get_research_templates()
            templates_display = display_research_templates(templates)
            print(templates_display)
            continue
            
        if command.lower().startswith("template"):
            query, template_info = handle_template_command(command)
            if query:
                try:
                    print("🔬 Researching with template... This may take a moment.")
                    result = workflow.run(query, template_info)
                    last_result = result
                    last_companies = result.get("companies", [])
                    original_companies = last_companies.copy() if last_companies else None
                    current_preferences = None
                    
                    print("\n" + "="*50)
                    print("📊 TEMPLATE RESEARCH RESULTS")
                    print("="*50)
                    
                    if template_info:
                        print(f"📋 Template: {template_info['name']}")
                        print(f"🎯 Use Case: {template_info['use_case']}")
                        print(f"👥 Target: {template_info['target_audience']}")
                        print(f"📊 Complexity: {template_info['complexity'].title()}")
                        print(f"⏱️ Estimated Time: {template_info['estimated_time']}")
                        print("")
                    
                    if result.get("companies"):
                        stats = generate_quick_stats(result["companies"])
                        print(stats)
                    
                    if result.get("analysis"):
                        print("\n💡 ANALYSIS:")
                        print(result["analysis"])
                    
                    if result.get("comparison_matrix"):
                        comparison_display = display_comparison_matrix(result["comparison_matrix"])
                        print(comparison_display)
                    
                    if result.get("companies"):
                        print(f"\n✅ Analyzed {len(result['companies'])} tools successfully!")
                        print("💡 Use 'list', 'search <keyword>', 'filter <criteria>', 'sort <field>', 'score', 'details <name|number>', 'compare <tool1> <tool2>', or 'export-compare <tool1> <tool2>' to refine results!")
                        
                except Exception as e:
                    print(f"❌ An error occurred: {e}")
                    last_result = None
                    last_companies = None
                    original_companies = None
                    current_preferences = None
            continue
            
        if command.lower() == "list":
            if not last_companies:
                print("⚠️ No results to list. Please run a query first.")
            else:
                tools_list = display_tools_list(last_companies)
                print(tools_list)
            continue
            
        if command.lower() == "trends":
            if not last_companies:
                print("⚠️ No results to analyze trends for. Please run a query first.")
            else:
                from src.utils import generate_trend_stats
                trend_analysis = generate_trend_stats(last_companies)
                print(trend_analysis)
                
                # Show trending tools in detail
                trending_tools = [c for c in last_companies if c.trend_status in ["Rising", "Hot", "Emerging"]]
                if trending_tools:
                    print(f"\n🔥 **Trending Tools Details** ({len(trending_tools)} tools)")
                    for i, tool in enumerate(trending_tools, 1):
                        print(f"{i}. **{tool.name}** - {tool.trend_status}")
                        print(f"   📊 Popularity: {tool.popularity_score}/10 | Community: {tool.community_activity} | Market: {tool.market_position}")
                        print(f"   📝 {tool.description[:100]}{'...' if len(tool.description) > 100 else ''}")
                        print("")
            continue
            
        if command.lower() == "score":
            if not last_companies:
                print("⚠️ No results to score. Please run a query first.")
                continue
            
            print("🎯 Let's get personalized recommendations!")
            try:
                preferences = get_recommendation_preferences()
                current_preferences = preferences
                
                scored_tools = score_and_rank_tools(last_companies, preferences)
                recommendations = display_scored_recommendations(scored_tools, preferences)
                print(recommendations)
                
                # Update last_companies to show scored order
                last_companies = [company for company, score in scored_tools]
                
            except KeyboardInterrupt:
                print("\n⚠️ Scoring cancelled.")
            continue
            
        if command.lower() == "save":
            if last_result:
                format_choice = input("Choose format (json/md): ").lower()
                if format_choice == 'json':
                    filename = save_as_json(last_result, last_result.get('metadata', {}).get('query', 'unknown'))
                    print(f"💾 Results saved to: {filename}")
                elif format_choice == 'md':
                    filename = save_as_markdown(last_result, last_result.get('metadata', {}).get('query', 'unknown'))
                    print(f"💾 Results saved to: {filename}")
                else:
                    print("⚠️ Invalid format. Skipping save.")
            else:
                print("⚠️ No results to save. Please run a query first.")
            continue
        
        # Handle details command
        if last_companies and command.lower().startswith("details"):
            arg = command[len("details"):].strip()
            if not arg:
                print("Usage: details <tool name|number>")
            else:
                show_tool_details(last_companies, arg)
            continue
        
        # Handle compare command
        if last_companies and command.lower().startswith("compare") and not command.lower().startswith("export-compare"):
            compare_tools(last_companies, command)
            continue
        
        # Handle export-compare command
        if last_companies and command.lower().startswith("export-compare"):
            export_comparison(last_companies, command)
            continue
        
        # Handle search command
        if last_companies and command.lower().startswith("search"):
            search_tools(last_companies, command)
            continue
        
        # Handle filtering and sorting
        if last_companies and (command.lower().startswith("filter") or command.lower().startswith("sort")):
            filtered_companies, filters_applied = parse_filter_command(command, last_companies)
            if filtered_companies != last_companies:
                last_companies = filtered_companies
                display = display_filtered_results(filtered_companies, len(original_companies), filters_applied)
                print(display)
            continue
        
        # Handle new queries
        try:
            print("🔬 Researching... This may take a moment.")
            result = workflow.run(command)
            last_result = result
            last_companies = result.get("companies", [])
            original_companies = last_companies.copy() if last_companies else None
            current_preferences = None  # Reset preferences for new query
            
            print("\n" + "="*50)
            print("📊 RESEARCH RESULTS")
            print("="*50)
            
            if result.get("companies"):
                stats = generate_quick_stats(result["companies"])
                print(stats)
            
            if result.get("analysis"):
                print("\n💡 ANALYSIS:")
                print(result["analysis"])
            
            if result.get("comparison_matrix"):
                comparison_display = display_comparison_matrix(result["comparison_matrix"])
                print(comparison_display)
            
            if result.get("companies"):
                print(f"\n✅ Analyzed {len(result['companies'])} tools successfully!")
                print("💡 Use 'list', 'search <keyword>', 'filter <criteria>', 'sort <field>', 'score', 'details <name|number>', 'compare <tool1> <tool2>', or 'export-compare <tool1> <tool2>' to refine results!")
                
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            last_result = None
            last_companies = None
            original_companies = None
            current_preferences = None

if __name__ == "__main__":
    main()  
  