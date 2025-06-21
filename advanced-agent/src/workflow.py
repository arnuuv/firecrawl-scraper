from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.message import Humanmessage, Systemmessage
from .firecrawl import FirecrawlService
from .prompts import DeveloperToolsPrompts

class Workflow:
  def __init__(self):
    self.firecrawl = FirecrawlService()
    self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    self.prompts = DeveloperToolsPrompts()
    self.workflow = StateGraph(ResearchState)
 
  def _build_workflow(self):
    pass
  
  def _extract_tools_step(self, state: ResearchState) -> Dict[str, Any]:
    print(f"Finding articles about: {state.query}")
    
    article_query = f"{state.query} tools comparison best all alternatives"
    