#!/usr/bin/env python3
"""
Script to generate annotation JSON files for MEDIUM difficulty images only.
"""

import os
import json
import glob
from pathlib import Path

def get_image_files(directory):
    """Get all PNG image files from a directory."""
    pattern = os.path.join(directory, "*.png")
    image_files = glob.glob(pattern)
    image_files.sort()
    return image_files

def generate_medium_annotation(image_path):
    """Generate annotation JSON for a single medium image."""
    image_filename = os.path.basename(image_path)
    image_id = os.path.splitext(image_filename)[0]
    
    # Extract image number for question IDs
    image_num = image_filename.split('_')[-1].split('.')[0]
    
    annotation = {
        "image_id": image_filename,
        # "image_path": image_path,
        "difficulty": "medium",
        "questions": [
            {
                "id": f"{image_id}_q1",
                "type": "classification_shape",
                "text": "What are the types of shapes present?",
                # "answer": "",  # To be filled during annotation
                # "answer_type": "list"
            },
            {
                "id": f"{image_id}_q2",
                "type": "counting_specific",
                "text": "Number of shapes of a particular type?",
                # "answer": "",  # To be filled during annotation
                # "answer_type": "object_count"
            },
            {
                "id": f"{image_id}_q3",
                "type": "comparison_size_smallest", 
                "text": "What is the smallest shape present?",
                # "answer": "",  # To be filled during annotation
                # "answer_type": "shape_type"
            },
            {
                "id": f"{image_id}_q4",
                "type": "comparison_size_largest",
                "text": "What is the largest shape present?",
                # "answer": "",  # To be filled during annotation
                # "answer_type": "shape_type"
            },
            {
                "id": f"{image_id}_q5",
                "type": "comparison_frequency",
                "text": "Which shape appears the most in the image?",
                # "answer": "",  # To be filled during annotation
                # "answer_type": "shape_type"
            },
            {
                "id": f"{image_id}_q6",
                "type": "duplicates_detection",
                "text": "Are there any duplicates in the image?",
                # "answer": "",  # To be filled during annotation
                # "answer_type": "boolean"
            }
        ]
    }
    
    return annotation

def main():
    """Generate annotations for medium difficulty images."""
    # Paths
    base_path = "/home/r64/Desktop/Desktop/CV/VQG-Dataset/VQG_SHAPES_DATA/data"
    images_dir = os.path.join(base_path, "generated_images", "medium")
    output_dir = "/home/r64/Desktop/Desktop/CV/VQG-Dataset/VQG_SHAPES_DATA/annotations/medium_annotations"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("🚀 Generating annotations for MEDIUM difficulty images...")
    print(f"Input directory: {images_dir}")
    print(f"Output directory: {output_dir}")
    
    # Get all image files
    image_files = get_image_files(images_dir)
    
    if not image_files:
        print(f"❌ No images found in {images_dir}")
        return
    
    print(f"📊 Found {len(image_files)} images")
    
    # Generate annotations
    for idx, image_path in enumerate(image_files, 1):
        annotation = generate_medium_annotation(image_path)
        
        # Create output filename
        image_filename = os.path.basename(image_path)
        annotation_filename = os.path.splitext(image_filename)[0] + "_annotation.json"
        annotation_path = os.path.join(output_dir, annotation_filename)
        
        # Save annotation
        with open(annotation_path, 'w', encoding='utf-8') as f:
            json.dump(annotation, f, indent=2, ensure_ascii=False)
        
        # Progress update
        if idx % 1000 == 0 or idx == len(image_files):
            print(f"  ✅ Generated {idx}/{len(image_files)} annotations")
    
    print(f"🎉 Completed! {len(image_files)} annotation files saved to {output_dir}")

if __name__ == "__main__":
    main()
