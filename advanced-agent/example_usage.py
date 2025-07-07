#!/usr/bin/env python3
"""
Example usage of the Developer Tools Research Agent

This script demonstrates how to use the agent programmatically
for automated research and analysis.
"""

import os
from dotenv import load_dotenv
from src.workflow import Workflow
from src.utils import (
    save_as_json,
    save_as_markdown,
    generate_quick_stats,
    display_comparison_matrix,
    filter_tools,
    sort_tools,
    score_and_rank_tools,
    get_recommendation_preferences,
    compare_two_tools,
    generate_trend_stats
)

# Load environment variables
load_dotenv()

def example_research():
    """Example of basic research workflow"""
    print("🚀 Starting Developer Tools Research Agent Example")
    print("=" * 60)
    
    # Initialize the workflow
    workflow = Workflow()
    
    # Example 1: Research database tools
    print("\n📊 Example 1: Researching Database Tools")
    print("-" * 40)
    
    query = "database tools for startups"
    print(f"Query: {query}")
    
    try:
        result = workflow.run(query)
        
        if result.get("companies"):
            print(f"✅ Found {len(result['companies'])} tools")
            
            # Generate quick stats
            stats = generate_quick_stats(result["companies"])
            print("\n📈 Quick Stats:")
            print(stats)
            
            # Show analysis
            if result.get("analysis"):
                print(f"\n💡 Analysis:")
                print(result["analysis"][:500] + "..." if len(result["analysis"]) > 500 else result["analysis"])
            
            # Show comparison matrix
            if result.get("comparison_matrix"):
                print("\n📊 Comparison Matrix:")
                comparison = display_comparison_matrix(result["comparison_matrix"])
                print(comparison)
            
            # Example filtering
            print("\n🔍 Example Filtering:")
            free_tools = filter_tools(result["companies"], pricing="free")
            print(f"Free tools: {len(free_tools)}")
            
            # Example sorting
            sorted_tools = sort_tools(result["companies"], sort_by="integrations", reverse=True)
            print(f"Top tool by integrations: {sorted_tools[0].name if sorted_tools else 'None'}")
            
            # Save results
            json_file = save_as_json(result, query)
            md_file = save_as_markdown(result, query)
            print(f"\n💾 Results saved to:")
            print(f"   JSON: {json_file}")
            print(f"   Markdown: {md_file}")
            
        else:
            print("❌ No tools found")
            
    except Exception as e:
        print(f"❌ Error during research: {e}")

def example_comparison():
    """Example of tool comparison"""
    print("\n\n🔍 Example 2: Tool Comparison")
    print("-" * 40)
    
    workflow = Workflow()
    
    try:
        # Research web frameworks
        result = workflow.run("python web frameworks")
        
        if result.get("companies") and len(result["companies"]) >= 2:
            tool1 = result["companies"][0]
            tool2 = result["companies"][1]
            
            print(f"Comparing: {tool1.name} vs {tool2.name}")
            
            # Generate comparison
            comparison = compare_two_tools(tool1, tool2)
            print("\n📊 Comparison:")
            print(comparison)
            
        else:
            print("❌ Need at least 2 tools for comparison")
            
    except Exception as e:
        print(f"❌ Error during comparison: {e}")

def example_trend_analysis():
    """Example of trend analysis"""
    print("\n\n📈 Example 3: Trend Analysis")
    print("-" * 40)
    
    workflow = Workflow()
    
    try:
        # Research real-time tools
        result = workflow.run("real-time collaboration tools")
        
        if result.get("companies"):
            # Generate trend stats
            trend_analysis = generate_trend_stats(result["companies"])
            print("📊 Trend Analysis:")
            print(trend_analysis)
            
            # Show trending tools
            trending_tools = [c for c in result["companies"] if c.trend_status in ["Rising", "Hot", "Emerging"]]
            if trending_tools:
                print(f"\n🔥 Trending Tools ({len(trending_tools)}):")
                for i, tool in enumerate(trending_tools, 1):
                    print(f"{i}. {tool.name} - {tool.trend_status}")
                    print(f"   Popularity: {tool.popularity_score}/10 | Community: {tool.community_activity}")
            
        else:
            print("❌ No tools found for trend analysis")
            
    except Exception as e:
        print(f"❌ Error during trend analysis: {e}")

def example_personalized_scoring():
    """Example of personalized scoring"""
    print("\n\n🎯 Example 4: Personalized Scoring")
    print("-" * 40)
    
    workflow = Workflow()
    
    try:
        # Research API tools
        result = workflow.run("API development tools")
        
        if result.get("companies"):
            print("Getting personalized recommendations...")
            
            # Simulate user preferences
            preferences = {
                "budget": "free",
                "team_size": "startup",
                "tech_stack": ["python", "javascript"],
                "use_case": "web_development"
            }
            
            # Score and rank tools
            scored_tools = score_and_rank_tools(result["companies"], preferences)
            
            print(f"\n🎯 Top 3 Recommendations:")
            for i, (tool, score) in enumerate(scored_tools[:3], 1):
                print(f"{i}. {tool.name} (Score: {score:.2f})")
                print(f"   {tool.description[:100]}...")
            
        else:
            print("❌ No tools found for scoring")
            
    except Exception as e:
        print(f"❌ Error during scoring: {e}")

def main():
    """Run all examples"""
    print("🎯 Developer Tools Research Agent - Example Usage")
    print("=" * 60)
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in the .env file")
        return
    
    try:
        # Run examples
        example_research()
        example_comparison()
        example_trend_analysis()
        example_personalized_scoring()
        
        print("\n\n✅ All examples completed successfully!")
        print("Check the generated files for detailed results.")
        
    except KeyboardInterrupt:
        print("\n⚠️ Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 