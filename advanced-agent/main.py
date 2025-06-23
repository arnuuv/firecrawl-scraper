from dotenv import load_dotenv
from src.workflow import Workflow
from src.utils import (
    display_comparison_matrix, 
    generate_quick_stats, 
    save_as_json, 
    save_as_markdown,
    filter_tools,
    sort_tools,
    display_filtered_results
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

def main():
    workflow = Workflow()
    print("🚀 Developer Tools Research Agent")
    print("Features: Research, Analysis, Report, Comparison Matrix, MD/JSON Export, Filtering")
    print("Commands: 'exit' to quit, 'save' to save last result, 'filter' to filter results")
    
    last_result = None
    last_companies = None
    original_companies = None
    
    while True:
        if last_companies:
            print(f"\n📊 Current results: {len(last_companies)} tools")
            command = input("🔍 Enter query, 'filter <criteria>', 'sort <field>', 'save', or 'exit': ")
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
                print("💡 Use 'filter <criteria>' or 'sort <field>' to refine results!")
                
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            last_result = None
            last_companies = None
            original_companies = None

if __name__ == "__main__":
    main()  
  