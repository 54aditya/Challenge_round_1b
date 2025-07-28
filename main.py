#!/usr/bin/env python3
"""
Challenge 1B: Persona-Driven Document Intelligence
Main entry point for processing document collections based on persona and job requirements.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from hybrid_document_analyzer import HybridDocumentAnalyzer
from output_generator import OutputGenerator


def load_input_data(input_path: str) -> Dict[str, Any]:
    """Load and validate input JSON data."""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate required fields
        required_fields = ['challenge_info', 'documents', 'persona', 'job_to_be_done']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        return data
    except Exception as e:
        print(f"Error loading input data: {e}")
        sys.exit(1)


def get_pdf_paths(documents: List[Dict], pdf_dir: str) -> List[str]:
    """Get full paths to PDF files."""
    pdf_paths = []
    for doc in documents:
        filename = doc['filename']
        pdf_path = os.path.join(pdf_dir, filename)
        if os.path.exists(pdf_path):
            pdf_paths.append(pdf_path)
        else:
            print(f"Warning: PDF file not found: {pdf_path}")
    
    return pdf_paths


def main():
    """Main execution function."""
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_json_path> <output_json_path>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Load input data
    input_data = load_input_data(input_path)
    
    # Extract key information
    documents = input_data['documents']
    persona = input_data['persona']['role']
    job_to_be_done = input_data['job_to_be_done']['task']
    
    # Get PDF directory (assuming PDFs are in a 'PDFs' subdirectory)
    input_dir = os.path.dirname(input_path)
    pdf_dir = os.path.join(input_dir, 'PDFs')
    
    # Get PDF file paths
    pdf_paths = get_pdf_paths(documents, pdf_dir)
    
    if not pdf_paths:
        print("Error: No PDF files found")
        sys.exit(1)
    
    print(f"Processing {len(pdf_paths)} PDF documents...")
    print(f"Persona: {persona}")
    print(f"Job: {job_to_be_done}")
    
    try:
        # Initialize components
        analyzer = HybridDocumentAnalyzer()
        output_generator = OutputGenerator()
        
        # Analyze documents using hybrid approach
        print("Analyzing documents with hybrid approach...")
        analysis_result = analyzer.analyze_documents(pdf_paths, persona, job_to_be_done)
        
        # Generate output
        print("Generating output...")
        output_data = output_generator.generate_output(
            documents=documents,
            persona=persona,
            job_to_be_done=job_to_be_done,
            extracted_sections=analysis_result['extracted_sections'],
            subsection_analysis=analysis_result['subsection_analysis']
        )
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        
        print(f"Output written to: {output_path}")
        print("Processing completed successfully!")
        
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if _name_ == "_main_":
    main() 
