from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .firecrawl import FirecrawlService
from .prompts import DeveloperToolsPrompts
from .models import ResearchState, CompanyInfo, CompanyAnalysis, ComparisonMatrix
from datetime import datetime

class Workflow:
  def __init__(self):
    self.firecrawl = FirecrawlService()
    self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    self.prompts = DeveloperToolsPrompts()
    self.workflow = self._build_workflow()
 
  def _build_workflow(self):
    graph = StateGraph(ResearchState)
    graph.add_node("extract_tools", self._extract_tools_step)
    graph.add_node("research", self._research_step)
    graph.add_node("analyze", self._analyze_step)
    graph.add_node("generate_report", self._generate_report_step)
    graph.add_node("generate_comparison", self._generate_comparison_step)
    graph.set_entry_point("extract_tools")
    graph.add_edge("extract_tools", "research")
    graph.add_edge("research", "analyze")
    graph.add_edge("analyze", "generate_report")
    graph.add_edge("generate_report", "generate_comparison")
    graph.add_edge("generate_comparison", END)
    return graph.compile()
  
  def _extract_tools_step(self, state: ResearchState) -> Dict[str, Any]:
    print(f"Finding articles about: {state.query}")
    
    article_query = f"{state.query} tools comparison best all alternatives"
    search_results = self.firecrawl.search_companies(article_query, num_results=3)
    
    all_content = "" 
    for result in search_results:
      url  =  result.get("url","")
      scraped = self.firecrawl.scrape_company_pages(url)
      if scraped:
        all_content += scraped.markdown[:1500] + "\n\n"
        
    if not all_content:
      return {"error": "No articles found"}
    
    messages = [
      SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
      HumanMessage(content=self.prompts.tool_extraction_user(state.query, all_content))
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
      SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
      HumanMessage(content=self.prompts.tool_analysis_user(company_name, content))
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
        integration_capabilities=[],
        trend_status="Unknown",
        popularity_score=5,
        community_activity="Medium",
        recent_updates="Unknown",
        market_position="Unknown"
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
      tool_search_results = self.firecrawl.search_companies(tool_name + " official site", num_results=1)
      if tool_search_results:
        result = tool_search_results.data[0]
        url = result.get("url","")
        company = CompanyInfo(
          name = tool_name,
          description = result.get("markdown", ""),
          website = url,
          tech_stack = [],
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
          # Trend analysis fields
          company.trend_status = analysis.trend_status
          company.popularity_score = analysis.popularity_score
          company.community_activity = analysis.community_activity
          company.recent_updates = analysis.recent_updates
          company.market_position = analysis.market_position
          
        companies.append(company)
        
    return {"companies": companies}
  
  def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
    print("Generating recommendations")
    company_data = ", ".join([
      company.model_dump_json() for company in state.companies
        ])
        
    messages = [
      SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
      HumanMessage(content=self.prompts.recommendations_user(state.query, company_data))
    ]
    response = self.llm.invoke(messages)
    return {"analysis": response.content}
    
  def _generate_report_step(self, state: ResearchState) -> Dict[str, Any]:
    print("Generating report")
    company_data = ", ".join([
      company.model_dump_json() for company in state.companies
    ])
    
    messages = [
      SystemMessage(content=self.prompts.REPORT_SYSTEM),
      HumanMessage(content=self.prompts.report_user(state.query, company_data))
    ]
    
    response = self.llm.invoke(messages)
    return {"report": response.content}

  def _generate_comparison_step(self, state: ResearchState) -> Dict[str, Any]:
    print("Generating comparison matrix")
    company_data = ", ".join([
      company.model_dump_json() for company in state.companies
    ])
    
    structured_llm = self.llm.with_structured_output(ComparisonMatrix)
    
    messages = [
      SystemMessage(content=self.prompts.COMPARISON_MATRIX_SYSTEM),
      HumanMessage(content=self.prompts.comparison_matrix_user(state.query, company_data))
    ]
    
    try:
      response = structured_llm.invoke(messages)
      return {"comparison_matrix": response}
    except Exception as e:
      print(f"Error generating comparison matrix: {e}")
      # Fallback to simple comparison
      tools = [company.name for company in state.companies]
      categories = ["Pricing", "Open Source", "API", "Languages", "Learning Curve"]
      matrix = {}
      for company in state.companies:
        matrix[company.name] = {
          "Pricing": company.pricing_model or "Unknown",
          "Open Source": "Yes" if company.is_open_source else "No",
          "API": "Yes" if company.api_available else "No",
          "Languages": ", ".join(company.language_support[:3]),
          "Learning Curve": "Medium"
        }
      fallback_matrix = ComparisonMatrix(tools=tools, categories=categories, matrix=matrix)
      return {"comparison_matrix": fallback_matrix}
  
  def run(self, query: str, template_info: dict = None) -> dict:
        """Run the complete workflow"""
        try:
            # Add template info to metadata if provided
            metadata = {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "template_info": template_info
            }
            
            # Research phase
            companies = self.research_phase(query)
            
            if not companies:
                return {
                    "error": "No companies found for the given query",
                    "metadata": metadata
                }
            
            # Analysis phase
            analysis = self.analysis_phase(companies, query)
            
            # Comparison matrix
            comparison_matrix = self.comparison_phase(companies)
            
            # Generate report
            report = self.report_phase(companies, analysis, query)
            
            return {
                "companies": companies,
                "analysis": analysis,
                "comparison_matrix": comparison_matrix,
                "report": report,
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "metadata": metadata if 'metadata' in locals() else {"query": query}
            }