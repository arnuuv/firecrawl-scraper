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
    save_comparison_as_markdown
)
import json
from datetime import datetime
import os

load_dotenv()

def save_results_to_file(result: dict, query: str):
    """Save research results to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"research_results_{timestamp}.json"
    
    # Convert Pydantic models to dict for JSON serialization
    serializable_result = {}
    for key, value in result.items():
        if hasattr(value, 'model_dump'):
            serializable_result[key] = value.model_dump()
        elif isinstance(value, list) and value and hasattr(value[0], 'model_dump'):
            serializable_result[key] = [item.model_dump() for item in value]
        else:
            serializable_result[key] = value
    
    # Add metadata
    serializable_result['metadata'] = {
        'query': query,
        'timestamp': timestamp,
        'generated_at': datetime.now().isoformat()
    }
    
    with open(filename, 'w') as f:
        json.dump(serializable_result, f, indent=2)
    
    return filename

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

def main():
    workflow = Workflow()
    print("🚀 Developer Tools Research Agent")
    print("Features: Research, Analysis, Report, Comparison Matrix, MD/JSON Export, Filtering, Scoring, Details, Compare, Export Compare")
    print("Commands: 'exit' to quit, 'save' to save last result, 'filter' to filter results, 'score' for recommendations, 'details <name|number>' for tool details, 'compare <tool1> <tool2>' for side-by-side comparison, 'export-compare <tool1> <tool2>' to save comparison as file")
    
    last_result = None
    last_companies = None
    original_companies = None
    current_preferences = None
    
    while True:
        if last_companies:
            print(f"\n📊 Current results: {len(last_companies)} tools")
            command = input("🔍 Enter query, 'filter <criteria>', 'sort <field>', 'score', 'details <name|number>', 'compare <tool1> <tool2>', 'export-compare <tool1> <tool2>', 'save', or 'exit': ")
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
                print("💡 Use 'filter <criteria>', 'sort <field>', 'score', 'details <name|number>', 'compare <tool1> <tool2>', or 'export-compare <tool1> <tool2>' to refine results!")
                
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            last_result = None
            last_companies = None
            original_companies = None
            current_preferences = None

if __name__ == "__main__":
    main()  
  