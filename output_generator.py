"""
Output Generator for Challenge 1B
Generates the final output JSON in the required format.
"""

import json
from datetime import datetime
from typing import Dict, List, Any


class OutputGenerator:
    """Generates the final output in the required JSON format."""
    
    def __init__(self):
        pass
    
    def generate_output(self, documents: List[Dict], persona: str, job_to_be_done: str,
                       extracted_sections: List[Dict], subsection_analysis: List[Dict]) -> Dict[str, Any]:
        """Generate the complete output JSON."""
        
        # Generate metadata
        metadata = self.generate_metadata(documents, persona, job_to_be_done)
        
        # Format extracted sections
        formatted_sections = self.format_extracted_sections(extracted_sections)
        
        # Format subsection analysis
        formatted_subsections = self.format_subsection_analysis(subsection_analysis)
        
        # Combine into final output
        output = {
            "metadata": metadata,
            "extracted_sections": formatted_sections,
            "subsection_analysis": formatted_subsections
        }
        
        return output
    
    def generate_metadata(self, documents: List[Dict], persona: str, job_to_be_done: str) -> Dict[str, Any]:
        """Generate metadata section."""
        # Extract document filenames
        input_documents = [doc['filename'] for doc in documents]
        
        # Get current timestamp
        processing_timestamp = datetime.now().isoformat()
        
        return {
            "input_documents": input_documents,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": processing_timestamp
        }
    
    def format_extracted_sections(self, extracted_sections: List[Dict]) -> List[Dict]:
        """Format extracted sections for output."""
        formatted_sections = []
        
        for section in extracted_sections:
            formatted_section = {
                "document": section['document'],
                "section_title": section['section_title'],
                "importance_rank": section.get('importance_rank', 1),
                "page_number": section['page_number']
            }
            formatted_sections.append(formatted_section)
        
        return formatted_sections
    
    def format_subsection_analysis(self, subsection_analysis: List[Dict]) -> List[Dict]:
        """Format subsection analysis for output."""
        formatted_subsections = []
        
        for subsection in subsection_analysis:
            formatted_subsection = {
                "document": subsection['document'],
                "refined_text": subsection['refined_text'],
                "page_number": subsection['page_number']
            }
            formatted_subsections.append(formatted_subsection)
        
        return formatted_subsections
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the output structure."""
        required_fields = ['metadata', 'extracted_sections', 'subsection_analysis']
        
        # Check required top-level fields
        for field in required_fields:
            if field not in output:
                print(f"Missing required field: {field}")
                return False
        
        # Validate metadata
        metadata = output['metadata']
        metadata_fields = ['input_documents', 'persona', 'job_to_be_done', 'processing_timestamp']
        for field in metadata_fields:
            if field not in metadata:
                print(f"Missing metadata field: {field}")
                return False
        
        # Validate extracted sections
        extracted_sections = output['extracted_sections']
        if not isinstance(extracted_sections, list):
            print("extracted_sections must be a list")
            return False
        
        for section in extracted_sections:
            section_fields = ['document', 'section_title', 'importance_rank', 'page_number']
            for field in section_fields:
                if field not in section:
                    print(f"Missing section field: {field}")
                    return False
        
        # Validate subsection analysis
        subsection_analysis = output['subsection_analysis']
        if not isinstance(subsection_analysis, list):
            print("subsection_analysis must be a list")
            return False
        
        for subsection in subsection_analysis:
            subsection_fields = ['document', 'refined_text', 'page_number']
            for field in subsection_fields:
                if field not in subsection:
                    print(f"Missing subsection field: {field}")
                    return False
        
        return True
    
    def save_output(self, output: Dict[str, Any], output_path: str) -> bool:
        """Save output to JSON file."""
        try:
            # Validate output before saving
            if not self.validate_output(output):
                print("Output validation failed")
                return False
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
            
            print(f"Output saved successfully to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving output: {e}")
            return False 