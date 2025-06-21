from dotenv import load_dotenv
from src.workflow import Workflow
from src.utils import display_comparison_matrix, generate_quick_stats
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
  print("Features: Research, Analysis, Report, Comparison Matrix")
  print("Commands: 'exit' to quit, 'save' to save results")
  
  while True:
    query = input("\n🔍 Enter a query (or 'exit' to quit): ")
    if query.lower() == "exit":
      print("👋 Exiting...")
      break
    
    try:
      print("🔬 Researching... This may take a moment.")
      result = workflow.run(query)
      
      # Display options
      print("\n" + "="*50)
      print("📊 RESEARCH RESULTS")
      print("="*50)
      
      # Show quick stats first
      if result.get("companies"):
        print("\n📈 QUICK STATS:")
        print("-" * 30)
        stats = generate_quick_stats(result["companies"])
        print(stats)
      
      if result.get("report"):
        print("\n📋 REPORT:")
        print("-" * 30)
        print(result["report"])
      
      if result.get("analysis"):
        print("\n💡 ANALYSIS:")
        print("-" * 30)
        print(result["analysis"])
      
      if result.get("comparison_matrix"):
        print("\n📊 COMPARISON MATRIX:")
        print("-" * 30)
        comparison_display = display_comparison_matrix(result["comparison_matrix"])
        print(comparison_display)
      
      # Show summary
      if result.get("companies"):
        print(f"\n✅ Analyzed {len(result['companies'])} tools successfully!")
        
      # Ask if user wants to save results
      save_choice = input("\n💾 Save results to file? (y/n): ").lower()
      if save_choice in ['y', 'yes']:
        filename = save_results_to_file(result, query)
        print(f"💾 Results saved to: {filename}")
        
    except Exception as e:
      print(f"❌ Error: {e}")

if __name__ == "__main__":
  main()  
  