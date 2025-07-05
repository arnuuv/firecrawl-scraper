class DeveloperToolsPrompts:
    """Collection of prompts for analyzing developer tools and technologies"""

    # Tool extraction prompts
    TOOL_EXTRACTION_SYSTEM = """You are a tech researcher. Extract specific tool, library, platform, or service names from articles.
                            Focus on actual products/tools that developers can use, not general concepts or features."""

    @staticmethod
    def tool_extraction_user(query: str, content: str) -> str:
        return f"""Query: {query}
                Article Content: {content}

                Extract a list of specific tool/service names mentioned in this content that are relevant to "{query}".

                Rules:
                - Only include actual product names, not generic terms
                - Focus on tools developers can directly use/implement
                - Include both open source and commercial options
                - Limit to the 5 most relevant tools
                - Return just the tool names, one per line, no descriptions

                Example format:
                Supabase
                PlanetScale
                Railway
                Appwrite
                Nhost"""

    # Company/Tool analysis prompts
    TOOL_ANALYSIS_SYSTEM = """You are analyzing developer tools and programming technologies. 
                            Focus on extracting information relevant to programmers and software developers. 
                            Pay special attention to programming languages, frameworks, APIs, SDKs, and development workflows."""

    @staticmethod
    def tool_analysis_user(company_name: str, content: str) -> str:
        return f"""Company/Tool: {company_name}
                Website Content: {content[:2500]}

                Analyze this content from a developer's perspective and provide:
                - pricing_model: One of "Free", "Freemium", "Paid", "Enterprise", or "Unknown"
                - is_open_source: true if open source, false if proprietary, null if unclear
                - tech_stack: List of programming languages, frameworks, databases, APIs, or technologies supported/used
                - description: Brief 1-sentence description focusing on what this tool does for developers
                - api_available: true if REST API, GraphQL, SDK, or programmatic access is mentioned
                - language_support: List of programming languages explicitly supported (e.g., Python, JavaScript, Go, etc.)
                - integration_capabilities: List of tools/platforms it integrates with (e.g., GitHub, VS Code, Docker, AWS, etc.)
                - trend_status: One of "Rising", "Stable", "Declining", "Hot", "Emerging" based on mentions, updates, and market buzz
                - popularity_score: Integer 1-10 based on community mentions, GitHub stars, Stack Overflow presence, etc.
                - community_activity: "High", "Medium", or "Low" based on community engagement indicators
                - recent_updates: "Recent" (last 3 months), "Moderate" (3-12 months), or "Stale" (over 1 year) based on update frequency
                - market_position: "Leader", "Challenger", "Niche", or "New" based on market presence and adoption

                Focus on developer-relevant features like APIs, SDKs, language support, integrations, and development workflows."""

    # Recommendation prompts
    RECOMMENDATIONS_SYSTEM = """You are a senior software engineer providing quick, concise tech recommendations. 
                            Keep responses brief and actionable - maximum 3-4 sentences total."""

    @staticmethod
    def recommendations_user(query: str, company_data: str) -> str:
        return f"""Developer Query: {query}
                Tools/Technologies Analyzed: {company_data}

                Provide a brief recommendation (3-4 sentences max) covering:
                - Which tool is best and why
                - Key cost/pricing consideration
                - Main technical advantage

                Be concise and direct - no long explanations needed."""

    # Report generation prompts
    REPORT_SYSTEM = """You are a technical writer creating comprehensive reports for developers. 
                    Provide detailed, well-structured analysis with clear sections and actionable insights."""

    @staticmethod
    def report_user(query: str, company_data: str) -> str:
        return f"""Developer Query: {query}
                Tools/Technologies Analyzed: {company_data}

                Create a comprehensive report with the following sections:

                1. **Executive Summary** (2-3 sentences)
                2. **Tool Comparison Table** (pricing, open source status, key features)
                3. **Detailed Analysis** (pros/cons for each tool)
                4. **Recommendations** (ranked by different use cases)
                5. **Implementation Considerations** (getting started tips)

                Focus on practical developer needs and real-world usage scenarios."""

    # Comparison matrix prompts
    COMPARISON_MATRIX_SYSTEM = """You are creating a structured comparison matrix for developer tools. 
                                Focus on key decision-making criteria that developers care about."""

    @staticmethod
    def comparison_matrix_user(query: str, company_data: str) -> str:
        return f"""Developer Query: {query}
                Tools/Technologies Analyzed: {company_data}

                Create a comparison matrix with the following categories:
                - Pricing Model (Free/Freemium/Paid/Enterprise)
                - Open Source (Yes/No/Partial)
                - API Available (Yes/No)
                - Language Support (List top 3 languages)
                - Learning Curve (Easy/Medium/Hard)
                - Community Size (Small/Medium/Large)
                - Documentation Quality (Poor/Good/Excellent)
                - Integration Capabilities (Limited/Moderate/Extensive)

                Return a structured matrix that can be easily compared side-by-side."""