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
        return CompanyAnalysis(
          pricing_model="Unknown",
          is_open_source=None,
          tech_stack=[],
          description="Failed",
          api_available=None,
          language_support=[],
          integration_capabilities=[]
        )
  def _research_step(self, state: ResearchState) -> Dict[str, Any]:
    extracted_tools = getattr(state,"extracted_tools",[])
    
    if not extracted_tools:
      print("No extracted tools found")
      search_results = self.firecrawl.search_companies(state.query, num_results=4)
      tool_names= [
        result.get("metadata",{}).get("title","Unknown")
        for result in search_results.data
      ]
    else:
      tool_names=extracted_tools[:4]
    print(f"Researching tools: {', '.join(tool_names)}")
    
    companies = [] 
    for tool_name in tool_names:
      tool_search_results = self.firecrawl.search_companies(tool_name + "official site", num_results=1)
      if tool_search_results:
        result = tool_search_results.data[0]
        url = result.get("url","")
        company = CompanyInfo(
          name = tool_name,
          description = result.get("markdown", ""),
          wesbite = url,
          tech_Stack = [],
          competitors = []
        )
        scraped = self.firecrawl.scrape_company_pages(url)
        if scraped:
          content = scraped.markdown
          analysis = self._analyze_company_content(company.name, content)
          
          company.pricing_model = analysis.pricing_model
          company.is_open_source = analysis.is_open_source
          company.tech_stack = analysis.tech_stack
          company.description = analysis.description
          company.api_available = analysis.api_available
          company.language_support = analysis.language_support
          company.integration_capabilities = analysis.integration_capabilities
          
        companies.append(company)
        
    return {"companies": companies}
  
  def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
    print("Generating recommendations")
    company_data = ", ".join([
      company.json() for company in state.companies
        ])
        
    messages = [
      Systemmessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
      Humanmessage(content=self.prompts.recommendations_user(company_data))
    ]
    response = self.llm.invoke(messages)
    return {"analysis": response.content}
    
  def _generate_report_step(self, state: ResearchState) -> Dict[str, Any]:
    print("Generating report")
    company_data = ", ".join([
      company.json() for company in state.companies
    ])
    
    messages = [
      Systemmessage(content=self.prompts.REPORT_SYSTEM),