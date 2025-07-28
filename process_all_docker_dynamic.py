#!/usr/bin/env python3
"""
Dynamic Docker Batch Processing Script for Challenge 1B
Processes any number of input files using Docker
"""

import os
import sys
import subprocess
import glob
import json
from pathlib import Path

def run_docker_command(cmd):
    """Run a Docker command"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def find_input_files():
    """Find all input JSON files in the input directory"""
    input_files = []
    
    # Look for JSON files in input directory and subdirectories
    for json_file in glob.glob("input/**/*.json", recursive=True):
        # Skip output files and other non-input files
        if "output" not in json_file and "desired" not in json_file:
            input_files.append(json_file)
    
    return sorted(input_files)

def validate_input_file(input_file):
    """Validate that an input file has the correct structure"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check required fields
        required_fields = ['challenge_info', 'documents', 'persona', 'job_to_be_done']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        return True, "Valid input file"
    except Exception as e:
        return False, f"Invalid JSON: {e}"

def process_collection_docker(collection_name, input_file, output_file):
    """Process a single collection using Docker"""
    print(f"\n{'='*50}")
    print(f"Processing {collection_name} with Docker")
    print(f"{'='*50}")
    
    # Get absolute paths for Docker volumes
    current_dir = os.getcwd()
    input_path = os.path.join(current_dir, "input")
    output_path = os.path.join(current_dir, "output")
    
    # Convert Windows paths to Docker format
    if os.name == 'nt':  # Windows
        input_path = input_path.replace('\\', '/')
        output_path = output_path.replace('\\', '/')
        # Add drive letter if needed
        if ':' in input_path:
            input_path = '/' + input_path.replace(':', '')
        if ':' in output_path:
            output_path = '/' + output_path.replace(':', '')
    
    # Docker run command with absolute paths
    docker_cmd = f'docker run --rm -v "{input_path}:/app/input" -v "{output_path}:/app/output" --network none challenge1b:latest "{input_file}" "{output_file}"'
    
    print(f"Running: {docker_cmd}")
    
    success, output = run_docker_command(docker_cmd)
    
    if success:
        print(f"✅ {collection_name} completed successfully!")
        print(f"Output: {output_file}")
        return True
    else:
        print(f"❌ Error processing {collection_name}:")
        print(f"Error: {output}")
        return False

def main():
    """Process all input files dynamically using Docker"""
    print("🚀 Starting dynamic Docker batch processing...")
    
    # Check if Docker image exists
    print("Checking Docker image...")
    success, output = run_docker_command("docker images challenge1b:latest")
    
    if not success or "challenge1b" not in output:
        print("Building Docker image...")
        build_cmd = "docker build --platform linux/amd64 -t challenge1b:latest ."
        success, output = run_docker_command(build_cmd)
        
        if not success:
            print(f"❌ Failed to build Docker image: {output}")
            return
        else:
            print("✅ Docker image built successfully!")
    
    # Find all input files
    input_files = find_input_files()
    
    if not input_files:
        print("❌ No input files found!")
        print("Please place your input JSON files in the input/ directory")
        return
    
    print(f"Found {len(input_files)} input file(s):")
    for i, input_file in enumerate(input_files, 1):
        print(f"  {i}. {input_file}")
    
    # Validate and process each input file
    valid_files = []
    for input_file in input_files:
        is_valid, message = validate_input_file(input_file)
        if is_valid:
            valid_files.append(input_file)
        else:
            print(f"⚠️  Skipping {input_file}: {message}")
    
    if not valid_files:
        print("❌ No valid input files found!")
        return
    
    print(f"\nProcessing {len(valid_files)} valid input file(s) with Docker...")
    
    # Process each valid file
    success_count = 0
    total_count = len(valid_files)
    
    for input_file in valid_files:
        # Generate output filename with unique path
        input_path = input_file.replace("input/", "").replace(".json", "")
        input_path_clean = input_path.replace("/", "_").replace("\\", "_")
        output_file = f"{input_path_clean}_docker_output.json"
        
        # Create collection name from file path
        collection_name = input_file.replace("input/", "").replace(".json", "")
        
        if process_collection_docker(collection_name, input_file, output_file):
            success_count += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"DYNAMIC DOCKER BATCH PROCESSING COMPLETE")
    print(f"{'='*50}")
    print(f"✅ Successfully processed: {success_count}/{total_count} files")
    
    if success_count == total_count:
        print("🎉 All files processed successfully with Docker!")
    else:
        print(f"⚠️  {total_count - success_count} files failed")
    
    print(f"\nOutput files generated in: output/")
    print("Files:")
    for input_file in valid_files:
        input_path = input_file.replace("input/", "").replace(".json", "")
        input_path_clean = input_path.replace("/", "_").replace("\\", "_")
        output_path = f"output/{input_path_clean}_docker_output.json"
        if os.path.exists(output_path):
            print(f"  ✅ {output_path}")
        else:
            print(f"  ❌ {output_path} (failed)")

if __name__ == "__main__":
    main() 