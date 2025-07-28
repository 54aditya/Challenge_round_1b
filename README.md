# Challenge 1B: Persona-Driven Document Intelligence

## Overview

This solution implements an intelligent document analyst system that extracts and prioritizes the most relevant sections from a collection of documents based on a specific persona and their job-to-be-done. The system uses advanced NLP techniques and semantic analysis to understand document content and match it with user requirements.

## Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd Adobe-India-Hackathon25/Challenge_1b

# Option 1: Use setup script (Linux/Mac)
bash setup.sh

# Option 2: Use setup script (Windows)
setup.bat

# Option 3: Manual setup
mkdir -p input/PDFs
mkdir -p output
mkdir -p desired
```

### 2. Prepare Your Input
```bash
# Place your input JSON file in the input directory
# Example: input/challenge1b_input.json

# Place your PDF documents in the input/PDFs directory
# Example: input/PDFs/document1.pdf, input/PDFs/document2.pdf, etc.
```

### 3. Run Locally

#### Single Collection:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the solution for a single collection
python main.py "input/challenge1b_input.json" "output/challenge1b_output.json"
```

#### All Collections at Once:
```bash
# Process all test collections in batch
python process_all.py
```

### 4. Run with Docker

#### Single Collection:
```bash
# Build the Docker image
docker build --platform linux/amd64 -t challenge1b:latest .

# Run the solution for a single collection
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none challenge1b:latest "challenge1b_input.json" "challenge1b_output.json"
```

#### All Collections at Once:
```bash
# Process all test collections using Docker (Linux/Mac)
python process_all_docker.py

# Process all test collections using Docker (Windows PowerShell)
.\process_all_docker_windows.ps1
```

## Input Format

### Directory Structure
```
Challenge_1b/
├── input/
│   ├── challenge1b_input.json    # Input configuration
│   └── PDFs/                     # PDF documents
│       ├── document1.pdf
│       ├── document2.pdf
│       └── ...
├── output/                       # Generated outputs
└── desired/                      # Expected outputs (for reference)
```

### Input JSON Format
```json
{
  "challenge_info": {
    "name": "Challenge 1B",
    "version": "1.0"
  },
  "documents": [
    {
      "filename": "document1.pdf"
    },
    {
      "filename": "document2.pdf"
    }
  ],
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  }
}
```

## Output Format

The solution generates a structured JSON output with:

```json
{
  "metadata": {
    "input_documents": ["document1.pdf", "document2.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "2024-01-15T10:30:00"
  },
  "extracted_sections": [
    {
      "document": "document1.pdf",
      "section_title": "Section Title",
      "importance_rank": 1,
      "page_number": 5
    }
  ],
  "subsection_analysis": [
    {
      "document": "document1.pdf",
      "refined_text": "Detailed, actionable content...",
      "page_number": 5
    }
  ]
}
```

## Approach & Methodology

### 1. Document Processing Pipeline
- **PDF Text Extraction**: Uses PyMuPDF for robust text extraction
- **Structure Analysis**: Identifies headings, sections, and document hierarchy
- **Content Classification**: Categorizes content into different types

### 2. Persona Analysis Engine
- **Persona Recognition**: Identifies and understands different persona types
- **Job Requirement Analysis**: Extracts action verbs, constraints, and specific requirements
- **Context Combination**: Merges persona and job information for relevance criteria

### 3. Section Extraction & Ranking
- **Multi-level Section Detection**: Identifies sections from headings and content structure
- **Relevance Scoring**: Uses weighted scoring based on keyword matching, semantic relevance, content quality, and section importance
- **Ranking Algorithm**: Prioritizes sections based on persona-specific needs

### 4. Content Refinement and Analysis
- **Content Refinement**: Extracts and refines content based on persona type
- **Actionable Information**: Focuses on practical, implementable content
- **Quality Filtering**: Ensures content meets relevance and quality thresholds

## Key Features

### Persona-Specific Processing
- **Travel Planner**: Focuses on locations, activities, accommodations, dining, and practical travel information
- **HR Professional**: Emphasizes processes, forms, compliance, workflows, and documentation
- **Food Contractor**: Prioritizes recipes, ingredients, preparation methods, and dietary considerations
- **Researcher**: Concentrates on methodologies, findings, data analysis, and conclusions
- **Student**: Highlights key concepts, definitions, examples, and practice problems
- **Investment Analyst**: Focuses on financial metrics, trends, strategies, and market analysis

### Advanced NLP Techniques
- **Semantic Similarity**: Uses advanced text analysis for understanding content meaning
- **Keyword Weighting**: Implements dynamic keyword importance based on persona and job context
- **Content Quality Assessment**: Evaluates information density, structure, and specificity
- **Multi-modal Analysis**: Combines text analysis with document structure understanding

### Robust Document Handling
- **Multiple PDF Libraries**: Robust text extraction across different PDF formats
- **Error Recovery**: Graceful handling of corrupted or complex documents
- **Performance Optimization**: Efficient processing for large document collections

## Technical Architecture

### Core Components
1. **HybridDocumentAnalyzer**: Main analysis engine with exact matching and semantic analysis
2. **OutputGenerator**: Formats results in required JSON structure
3. **Main Entry Point**: Orchestrates the entire processing pipeline

### Dependencies
- **PyMuPDF**: Advanced PDF text extraction and analysis
- **numpy**: Numerical computing utilities
- **scikit-learn**: Machine learning utilities for text processing

## Performance Characteristics

### Constraints Compliance
- **Model Size**: < 1GB (uses lightweight models)
- **Processing Time**: < 60 seconds for 3-5 documents
- **CPU Only**: No GPU dependencies
- **Offline Operation**: No internet access required

### Scalability
- **Document Count**: Handles 3-10 documents efficiently
- **Document Size**: Supports PDFs up to 50 pages
- **Memory Usage**: Optimized for systems with 8 CPUs and 16 GB RAM

## Testing

### Test Collections
The solution includes three test collections:

```bash
# Test Collection 1 (Travel Planning)
python main.py "input/Collection 1/challenge1b_input.json" "output/collection1_output.json"

# Test Collection 2 (HR Forms)
python main.py "input/Collection 2/challenge1b_input.json" "output/collection2_output.json"

# Test Collection 3 (Food Contractor)
python main.py "input/Collection 3/challenge1b_input.json" "output/collection3_output.json"
```

### Validation
Compare outputs with expected results in the `desired/` directory:
```bash
# Compare outputs (example)
diff output/collection1_output.json desired/collection1.json
```

## Troubleshooting

### Common Issues

1. **PDF files not found**
   - Ensure PDFs are placed in `input/PDFs/` directory
   - Check filenames match exactly with input JSON

2. **Docker build fails**
   - Ensure Docker Desktop is running
   - Check platform compatibility: `docker build --platform linux/amd64`

3. **Permission errors**
   - Ensure proper file permissions on input/output directories
   - Use `chmod` if needed: `chmod 755 input output`

4. **Memory issues**
   - Solution is optimized for 8 CPUs and 16 GB RAM
   - Reduce document count if experiencing issues

### Error Messages
- **"Missing required field"**: Check input JSON format
- **"No PDF files found"**: Verify PDF directory structure
- **"Usage: python main.py"**: Check command line arguments

## GitHub Setup

### Initial Repository Setup
```bash
# Create necessary directories (GitHub doesn't upload empty folders)
mkdir -p input/PDFs
mkdir -p output
mkdir -p desired

# Create .gitkeep files to ensure folders are tracked
touch input/.gitkeep
touch input/PDFs/.gitkeep
touch output/.gitkeep
touch desired/.gitkeep

# Add to git
git add .
git commit -m "Initial setup with directory structure"
```

### .gitignore (Optional)
Create a `.gitignore` file to exclude temporary files:
```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so

# Output files (optional - remove if you want to track outputs)
output/*.json

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## License

This project is part of the Adobe India Hackathon 2025 Challenge 1B submission. 