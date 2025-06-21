from dotenv import load_dotenv
from src.workflow import Workflow

load_dotenv()

def main():
  workflow = Workflow()
  print("Developer Tools Research Agent")
  
  while True:
    query = input("\n Developer Tools Research Agent\n Enter a query (or 'exit' to quit): ")
    if query.lower() == "exit":
      print("Exiting...")
      break
    
    try:
      result = workflow.run(query)
      print("\nResearch Results:")
      print(result["report"])
    except Exception as e:
      print(f"Error: {e}")