from dotenv import load_dotenv
from src.workflow import Workflow
from src.utils import display_comparison_matrix, generate_quick_stats, save_as_json, save_as_markdown
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

def main():
    workflow = Workflow()
    print("🚀 Developer Tools Research Agent")
    print("Features: Research, Analysis, Report, Comparison Matrix, MD/JSON Export")
    print("Commands: 'exit' to quit")
    
    last_result = None
    
    while True:
        query = input("\n🔍 Enter a query (or 'exit' to quit, 'save' to save last result): ")
        
        if query.lower() == "exit":
            print("👋 Exiting...")
            break
            
        if query.lower() == "save":
            if last_result:
                format_choice = input("Choose format (json/md): ").lower()
                if format_choice == 'json':
                    filename = save_as_json(last_result, last_result['metadata']['query'])
                    print(f"💾 Results saved to: {filename}")
                elif format_choice == 'md':
                    filename = save_as_markdown(last_result, last_result['metadata']['query'])
                    print(f"💾 Results saved to: {filename}")
                else:
                    print("⚠️ Invalid format. Skipping save.")
            else:
                print("⚠️ No results to save. Please run a query first.")
            continue
        
        try:
            print("🔬 Researching... This may take a moment.")
            result = workflow.run(query)
            last_result = result
            
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
                
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            last_result = None

if __name__ == "__main__":
    main()  
  