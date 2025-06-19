#!/usr/bin/env python3
"""
Enhanced Example Usage of VC Form Filling AI Agent

This script demonstrates the advanced capabilities including:
- Navigation to main pages and finding apply links
- File uploads (documents, pitch decks, etc.)
- Enhanced form filling with AI
- Batch processing with file uploads
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any

from vc_form_agent import FormFillingAgent
from vc_form_agent.utils.data_manager import DataManager
from vc_form_agent.templates.ycombinator import YCombinatorTemplate


class EnhancedVCFormAgent:
    """Enhanced VC Form Agent with advanced capabilities."""
    
    def __init__(self):
        """Initialize the enhanced agent."""
        self.agent = FormFillingAgent(
            headless=False,  # Set to True for production
            browser_type="chrome"
        )
        
        # Sample file paths (you would replace these with your actual files)
        self.sample_files = {
            "pitch_deck": "documents/pitch_deck.pdf",
            "financial_model": "documents/financial_model.xlsx",
            "team_bios": "documents/team_bios.pdf",
            "market_research": "documents/market_research.pdf",
            "product_demo": "documents/product_demo.mp4"
        }
        
        # Create sample documents directory
        self._create_sample_documents()
    
    def _create_sample_documents(self):
        """Create sample document files for demonstration."""
        docs_dir = Path("documents")
        docs_dir.mkdir(exist_ok=True)
        
        # Create sample files (empty files for demo)
        for file_name in self.sample_files.values():
            file_path = Path(file_name)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not file_path.exists():
                # Create empty file with appropriate extension
                if file_path.suffix == '.pdf':
                    file_path.write_text("Sample PDF content")
                elif file_path.suffix == '.xlsx':
                    file_path.write_text("Sample Excel content")
                elif file_path.suffix == '.mp4':
                    file_path.write_text("Sample video content")
                else:
                    file_path.write_text("Sample document content")
        
        print("✅ Sample documents created")
    
    async def example_navigate_and_fill_with_files(self):
        """Example: Navigate to main page, find apply link, and fill form with file uploads."""
        print("\n=== Example: Navigate and Fill with File Uploads ===")
        
        # File uploads configuration
        file_uploads = {
            "pitch_deck": self.sample_files["pitch_deck"],
            "financial_model": self.sample_files["financial_model"],
            "team_bios": self.sample_files["team_bios"],
            "additional_documents": [
                self.sample_files["market_research"],
                self.sample_files["product_demo"]
            ]
        }
        
        # Custom field mappings
        custom_fields = {
            "company_name": "TechStartup Inc.",
            "company_description": "AI-powered SaaS platform that automates business processes",
            "traction_metrics": "300% YoY growth, 500 customers, $50K MRR",
            "competitive_advantage": "Proprietary AI algorithms, 80% time savings, enterprise-grade security"
        }
        
        # Navigate to main page and fill form
        result = await self.agent.navigate_and_fill_form(
            main_url="https://example-vc.com",  # Replace with actual VC URL
            template_name="ycombinator",
            custom_fields=custom_fields,
            file_uploads=file_uploads,
            apply_link_texts=["Apply Now", "Submit Application", "Start Application"]
        )
        
        print(f"Success: {result.success}")
        print(f"Fields filled: {result.fields_filled}/{result.total_fields}")
        print(f"Files uploaded: {len(result.files_uploaded)}")
        print(f"Errors: {result.errors}")
        
        return result
    
    async def example_batch_processing_with_files(self):
        """Example: Process multiple VC applications with file uploads."""
        print("\n=== Example: Batch Processing with File Uploads ===")
        
        # List of VC URLs (replace with actual URLs)
        vc_urls = [
            "https://vc1.com",
            "https://vc2.com", 
            "https://vc3.com"
        ]
        
        # File uploads for all forms
        file_uploads = {
            "pitch_deck": self.sample_files["pitch_deck"],
            "financial_model": self.sample_files["financial_model"],
            "team_bios": self.sample_files["team_bios"]
        }
        
        # Process all VCs
        results = await self.agent.batch_process(
            urls=vc_urls,
            template_name="generic",
            file_uploads=file_uploads,
            delay_between_forms=30,
            auto_navigate=True
        )
        
        # Print results
        successful = sum(1 for r in results if r.success)
        total_files = sum(len(r.files_uploaded or []) for r in results)
        
        print(f"Successfully filled {successful}/{len(vc_urls)} forms")
        print(f"Total files uploaded: {total_files}")
        
        return results
    
    async def example_smart_form_detection(self):
        """Example: Smart form detection and filling without templates."""
        print("\n=== Example: Smart Form Detection ===")
        
        # Let AI detect and fill form fields automatically
        result = await self.agent.fill_form(
            url="https://example-vc-form.com/apply",
            auto_navigate_to_apply=True,
            file_uploads={
                "pitch_deck": self.sample_files["pitch_deck"],
                "financial_documents": [
                    self.sample_files["financial_model"],
                    self.sample_files["market_research"]
                ]
            }
        )
        
        print(f"Smart form detection result: {result.success}")
        print(f"Fields detected and filled: {result.fields_filled}")
        
        return result
    
    async def example_custom_file_upload_scenarios(self):
        """Example: Different file upload scenarios."""
        print("\n=== Example: Custom File Upload Scenarios ===")
        
        scenarios = [
            {
                "name": "Single File Upload",
                "file_uploads": {
                    "pitch_deck": self.sample_files["pitch_deck"]
                }
            },
            {
                "name": "Multiple Files to Single Field",
                "file_uploads": {
                    "additional_documents": [
                        self.sample_files["pitch_deck"],
                        self.sample_files["financial_model"],
                        self.sample_files["team_bios"]
                    ]
                }
            },
            {
                "name": "Multiple Fields with Multiple Files",
                "file_uploads": {
                    "pitch_deck": self.sample_files["pitch_deck"],
                    "financial_documents": [
                        self.sample_files["financial_model"],
                        self.sample_files["market_research"]
                    ],
                    "team_information": self.sample_files["team_bios"],
                    "product_demo": self.sample_files["product_demo"]
                }
            }
        ]
        
        for scenario in scenarios:
            print(f"\nTesting: {scenario['name']}")
            
            result = await self.agent.fill_form(
                url="https://example-vc-form.com/apply",
                file_uploads=scenario["file_uploads"],
                auto_navigate_to_apply=False
            )
            
            print(f"  Success: {result.success}")
            print(f"  Files uploaded: {len(result.files_uploaded)}")
    
    async def example_navigation_testing(self):
        """Example: Test navigation and apply link detection."""
        print("\n=== Example: Navigation Testing ===")
        
        test_urls = [
            "https://example-vc1.com",
            "https://example-vc2.com",
            "https://example-vc3.com"
        ]
        
        for url in test_urls:
            print(f"\nTesting navigation to: {url}")
            
            try:
                # Test navigation
                result = await self.agent.navigate_and_fill_form(
                    main_url=url,
                    apply_link_texts=["Apply", "Apply Now", "Submit Application"]
                )
                
                if result.success:
                    print(f"  ✅ Successfully navigated and filled form")
                    print(f"  📄 Fields filled: {result.fields_filled}")
                    print(f"  📎 Files uploaded: {len(result.files_uploaded)}")
                else:
                    print(f"  ❌ Failed: {result.errors}")
                    
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
    
    def example_file_preparation(self):
        """Example: Prepare files for upload."""
        print("\n=== Example: File Preparation ===")
        
        # Common file types for VC applications
        file_types = {
            "pitch_deck": {
                "description": "Company pitch deck (PDF)",
                "recommended_size": "5-15 MB",
                "format": "PDF"
            },
            "financial_model": {
                "description": "Financial projections and model",
                "recommended_size": "2-10 MB", 
                "format": "Excel"
            },
            "team_bios": {
                "description": "Founder and team biographies",
                "recommended_size": "1-5 MB",
                "format": "PDF"
            },
            "market_research": {
                "description": "Market analysis and research",
                "recommended_size": "3-10 MB",
                "format": "PDF"
            },
            "product_demo": {
                "description": "Product demonstration video",
                "recommended_size": "10-50 MB",
                "format": "MP4"
            }
        }
        
        print("Recommended file preparation:")
        for file_type, details in file_types.items():
            print(f"  📄 {file_type}:")
            print(f"    Description: {details['description']}")
            print(f"    Format: {details['format']}")
            print(f"    Size: {details['recommended_size']}")
    
    async def run_all_examples(self):
        """Run all enhanced examples."""
        print("🚀 Enhanced VC Form Filling AI Agent - Examples")
        print("=" * 60)
        
        try:
            # File preparation guide
            self.example_file_preparation()
            
            # Navigation testing
            await self.example_navigation_testing()
            
            # Smart form detection
            await self.example_smart_form_detection()
            
            # Custom file upload scenarios
            await self.example_custom_file_upload_scenarios()
            
            # Navigate and fill with files
            await self.example_navigate_and_fill_with_files()
            
            # Batch processing with files
            await self.example_batch_processing_with_files()
            
            print("\n✅ All enhanced examples completed!")
            print("\n📋 Key Features Demonstrated:")
            print("  • Automatic navigation to apply pages")
            print("  • File uploads (single and multiple files)")
            print("  • Smart form field detection")
            print("  • Batch processing with file uploads")
            print("  • AI-powered field mapping")
            print("  • Form validation and error handling")
            
        except Exception as e:
            print(f"❌ Error running examples: {str(e)}")


def main():
    """Run the enhanced examples."""
    enhanced_agent = EnhancedVCFormAgent()
    asyncio.run(enhanced_agent.run_all_examples())


if __name__ == "__main__":
    main() 