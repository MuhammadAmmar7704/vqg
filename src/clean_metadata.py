#!/usr/bin/env python3
"""
Script to remove individual image metadata JSON files while keeping dataset metadata files.
Removes all *_metadata.json files except *dataset_metadata.json files.
"""

import os
import glob
from pathlib import Path

def clean_metadata_files(base_dir):
    """Remove individual image metadata files while preserving dataset metadata."""
    
    difficulties = ["easy", "medium", "hard"]
    total_removed = 0
    
    print("🧹 Cleaning metadata files...")
    print(f"Base directory: {base_dir}")
    print("-" * 60)
    
    for difficulty in difficulties:
        difficulty_dir = os.path.join(base_dir, "generated_images", difficulty)
        
        if not os.path.exists(difficulty_dir):
            print(f"⚠️  Directory not found: {difficulty_dir}")
            continue
        
        print(f"📂 Cleaning {difficulty} directory...")
        
        # Find all metadata files
        all_metadata_files = glob.glob(os.path.join(difficulty_dir, "*_metadata.json"))
        
        # Filter out dataset metadata files
        dataset_metadata_files = glob.glob(os.path.join(difficulty_dir, "*dataset_metadata.json"))
        
        # Files to remove (individual image metadata)
        files_to_remove = [f for f in all_metadata_files if f not in dataset_metadata_files]
        
        print(f"  📊 Found {len(all_metadata_files)} total metadata files")
        print(f"  🔒 Keeping {len(dataset_metadata_files)} dataset metadata files")
        print(f"  🗑️  Removing {len(files_to_remove)} individual image metadata files")
        
        # Remove individual metadata files
        removed_count = 0
        for file_path in files_to_remove:
            try:
                os.remove(file_path)
                removed_count += 1
            except OSError as e:
                print(f"  ❌ Error removing {file_path}: {e}")
        
        print(f"  ✅ Successfully removed {removed_count} files from {difficulty}")
        total_removed += removed_count
        
        # List remaining files for verification
        remaining_files = glob.glob(os.path.join(difficulty_dir, "*_metadata.json"))
        if remaining_files:
            print(f"  📋 Remaining metadata files in {difficulty}:")
            for f in remaining_files:
                print(f"    - {os.path.basename(f)}")
        
        print()
    
    print("-" * 60)
    print(f"🎉 Cleanup completed!")
    print(f"📊 Total files removed: {total_removed}")

def main():
    """Main function to clean metadata files."""
    base_dir = "/home/r64/Desktop/Desktop/CV/VQG-Dataset/VQG_SHAPES_DATA/data"
    
    # Confirm action
    print("This script will remove individual image metadata files (*_metadata.json)")
    print("while keeping dataset metadata files (*dataset_metadata.json)")
    print(f"Target directory: {base_dir}")
    
    response = input("\nDo you want to proceed? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        clean_metadata_files(base_dir)
    else:
        print("❌ Operation cancelled.")

if __name__ == "__main__":
    main()
