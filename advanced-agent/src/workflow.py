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
    search_results = self.firecrawl.search_companies(article_query, num_results=3)
    
    all_content = "" 
    for result in search_results:
      url  =  results.get("url","")
      scraped = self.firecrawl.scrape_company_pages(url)
      if scraped:
        all_content += scraped.markdown[:1500] + "\n\n"
        
    if not all_content:
      return {"error": "No articles found"}
    
    messages = [
      Systemmessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
      Humanmessage(content=self.prompts.tool_extraction_user(state.query, all_content))
    ]
    
    try:
      response = self.llm.invoke(messages)
      tool_names = [
        name.strip()
        for name in response.content.strip().split("\n")
        if name.strip()
      ]
      print(f"Extracted tools : {', '.join(tool_names[:5])}")
      return {"extracted_tools": tool_names}
    except Exception as e:
      print(e)
      return {"extracted_tools": []}
    
    def _analyze_company_content(self,company_name:str,content:str) -> CompanyAnalysis:
      structured_llm = self.llm.with_structured_output(CompanyAnalysis)
      
      messages = [
        Systemmessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
        Humanmessage(content=self.prompts.tool_analysis_user(company_name, content))
      ]
      
      try:
        response = structured_llm.invoke(messages)
        return response
      except Exception as e:
        print(e)
        return None 