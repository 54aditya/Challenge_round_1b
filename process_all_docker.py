#!/usr/bin/env python3
"""
Docker Batch Processing Script for Challenge 1B
Processes all collections using Docker
"""

import os
import sys
import subprocess
from pathlib import Path

def run_docker_command(cmd):
    """Run a Docker command"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

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
    """Process all collections using Docker"""
    print("🚀 Starting Docker batch processing for all collections...")
    
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
    
    # Define collections to process
    collections = [
        {
            "name": "Collection 1 - Travel Planning",
            "input": "Collection 1/challenge1b_input.json",
            "output": "collection1_docker_batch.json"
        },
        {
            "name": "Collection 2 - HR Forms",
            "input": "Collection 2/challenge1b_input.json", 
            "output": "collection2_docker_batch.json"
        },
        {
            "name": "Collection 3 - Food Contractor",
            "input": "Collection 3/challenge1b_input.json",
            "output": "collection3_docker_batch.json"
        }
    ]
    
    # Process each collection
    success_count = 0
    total_count = len(collections)
    
    for collection in collections:
        if process_collection_docker(collection["name"], collection["input"], collection["output"]):
            success_count += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"DOCKER BATCH PROCESSING COMPLETE")
    print(f"{'='*50}")
    print(f"✅ Successfully processed: {success_count}/{total_count} collections")
    
    if success_count == total_count:
        print("🎉 All collections processed successfully with Docker!")
    else:
        print(f"⚠️  {total_count - success_count} collections failed")
    
    print(f"\nOutput files generated in: output/")
    print("Files:")
    for collection in collections:
        output_path = f"output/{collection['output']}"
        if os.path.exists(output_path):
            print(f"  ✅ {output_path}")
        else:
            print(f"  ❌ {output_path} (failed)")

if __name__ == "__main__":
    main() 