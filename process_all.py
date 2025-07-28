#!/usr/bin/env python3
"""
Batch Processing Script for Challenge 1B
Processes all collections at once and generates outputs for each
"""

import os
import sys
import subprocess
from pathlib import Path

def process_collection(collection_name, input_file, output_file):
    """Process a single collection"""
    print(f"\n{'='*50}")
    print(f"Processing {collection_name}")
    print(f"{'='*50}")
    
    # Run the main script
    cmd = [
        sys.executable, "main.py",
        input_file,
        output_file
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ {collection_name} completed successfully!")
        print(f"Output: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error processing {collection_name}:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Process all collections"""
    print("🚀 Starting batch processing for all collections...")
    
    # Define collections to process
    collections = [
        {
            "name": "Collection 1 - Travel Planning",
            "input": "input/Collection 1/challenge1b_input.json",
            "output": "output/collection1_batch_output.json"
        },
        {
            "name": "Collection 2 - HR Forms",
            "input": "input/Collection 2/challenge1b_input.json", 
            "output": "output/collection2_batch_output.json"
        },
        {
            "name": "Collection 3 - Food Contractor",
            "input": "input/Collection 3/challenge1b_input.json",
            "output": "output/collection3_batch_output.json"
        }
    ]
    
    # Process each collection
    success_count = 0
    total_count = len(collections)
    
    for collection in collections:
        if process_collection(collection["name"], collection["input"], collection["output"]):
            success_count += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"BATCH PROCESSING COMPLETE")
    print(f"{'='*50}")
    print(f"✅ Successfully processed: {success_count}/{total_count} collections")
    
    if success_count == total_count:
        print("🎉 All collections processed successfully!")
    else:
        print(f"⚠️  {total_count - success_count} collections failed")
    
    print(f"\nOutput files generated in: output/")
    print("Files:")
    for collection in collections:
        if os.path.exists(collection["output"]):
            print(f"  ✅ {collection['output']}")
        else:
            print(f"  ❌ {collection['output']} (failed)")

if __name__ == "__main__":
    main() 