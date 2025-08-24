#!/usr/bin/env python3
"""
Test script to generate a few sample annotations to verify the format.
"""

import os
import json
from generate_annotations import generate_annotation_for_image

def test_annotation_generation():
    """Test annotation generation with sample data."""
    print("🧪 Testing annotation generation...")
    
    # Test data
    test_cases = [
        {
            "image_path": "/home/r64/Desktop/Desktop/CV/VQG-Dataset/VQG_SHAPES_DATA/data/generated_images/easy/easy_image_00001.png",
            "difficulty": "easy"
        },
        {
            "image_path": "/home/r64/Desktop/Desktop/CV/VQG-Dataset/VQG_SHAPES_DATA/data/generated_images/medium/medium_image_00001.png", 
            "difficulty": "medium"
        },
        {
            "image_path": "/home/r64/Desktop/Desktop/CV/VQG-Dataset/VQG_SHAPES_DATA/data/generated_images/hard/hard_image_00001.png",
            "difficulty": "hard"
        }
    ]
    
    # Create test output directory
    test_output_dir = "/home/r64/Desktop/Desktop/CV/VQG-Dataset/VQG_SHAPES_DATA/test_annotations"
    os.makedirs(test_output_dir, exist_ok=True)
    
    for test_case in test_cases:
        image_path = test_case["image_path"]
        difficulty = test_case["difficulty"]
        
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"⚠️  Image not found: {image_path}")
            continue
        
        print(f"📝 Generating test annotation for {difficulty} difficulty...")
        
        # Generate annotation
        annotation = generate_annotation_for_image(image_path, difficulty)
        
        # Save test annotation
        output_filename = f"test_{difficulty}_annotation.json"
        output_path = os.path.join(test_output_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(annotation, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved test annotation: {output_path}")
        
        # Print sample output
        print(f"Sample {difficulty} annotation:")
        print(json.dumps(annotation, indent=2)[:500] + "...")
        print("-" * 50)
    
    print(f"🎉 Test completed! Check {test_output_dir} for sample files.")

if __name__ == "__main__":
    test_annotation_generation()
