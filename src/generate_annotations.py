#!/usr/bin/env python3
"""
Script to generate annotation JSON files for VQG dataset.
Creates question-answer pairs for each image based on difficulty level.
"""

import os
import json
import glob
from pathlib import Path

# Question templates for each difficulty level
QUESTIONS_CONFIG = {
    "easy": [
        {
            "type": "counting_total",
            "template": "What are the number of shapes present in the image?"
        },
        {
            "type": "existence_list", 
            "template": "What shapes are present in the image?"
        }
    ],
    "medium": [
        {
            "type": "classification_shape",
            "template": "What are the types of shapes present?"
        },
        {
            "type": "counting_specific",
            "template": "Number of shapes of a particular type?"
        },
        {
            "type": "comparison_size_smallest",
            "template": "What is the smallest shape present?"
        },
        {
            "type": "comparison_size_largest", 
            "template": "What is the largest shape present?"
        },
        {
            "type": "comparison_frequency",
            "template": "Which shape appears the most in the image?"
        },
        {
            "type": "duplicates_detection",
            "template": "Are there any duplicates in the image?"
        }
    ],
    "hard": [
        {
            "type": "comparison_size_second",
            "template": "What is the second largest shape?"
        },
        {
            "type": "ordering_size",
            "template": "What are the order-wise smallest shapes?"
        },
        {
            "type": "attribute_color",
            "template": "What are the colors of the shapes present?"
        },
        {
            "type": "counting_colors",
            "template": "Total number of colors in the image?"
        }
    ]
}

def get_image_files(directory):
    """Get all PNG image files from a directory."""
    pattern = os.path.join(directory, "*.png")
    image_files = glob.glob(pattern)
    # Sort to ensure consistent ordering
    image_files.sort()
    return image_files

def generate_annotation_for_image(image_path, difficulty):
    """Generate annotation JSON for a single image."""
    image_filename = os.path.basename(image_path)
    image_id = os.path.splitext(image_filename)[0]
    
    # Extract image number for question IDs
    if difficulty in image_filename:
        # Extract number from filename like "easy_image_00001.png"
        image_num = image_filename.split('_')[-1].split('.')[0]
    else:
        image_num = "00001"  # fallback
    
    annotation = {
        "image_id": image_filename,
        # "image_path": image_path,
        "difficulty": difficulty,
        "questions": []
    }
    
    # Get questions for this difficulty level
    questions = QUESTIONS_CONFIG.get(difficulty, [])
    
    for idx, question_config in enumerate(questions, 1):
        question_id = f"{image_id}_q{idx}"
        
        question = {
            "id": question_id,
            "type": question_config["type"],
            "text": question_config["template"],
            # "answer": "",  # To be filled during annotation
            # "answer_type": question_config["type"]
        }
        
        annotation["questions"].append(question)
    
    return annotation

def generate_annotations_for_difficulty(difficulty, base_path, output_dir):
    """Generate annotations for all images in a difficulty level."""
    print(f"Generating annotations for {difficulty} difficulty...")
    
    # Input directory for images
    images_dir = os.path.join(base_path, "generated_images", difficulty)
    
    # Create output directory for annotations
    annotations_dir = os.path.join(output_dir, f"{difficulty}_annotations")
    os.makedirs(annotations_dir, exist_ok=True)
    
    # Get all image files
    image_files = get_image_files(images_dir)
    
    if not image_files:
        print(f"No images found in {images_dir}")
        return
    
    print(f"Found {len(image_files)} images in {difficulty}")
    
    # Generate annotations for each image
    for idx, image_path in enumerate(image_files, 1):
        annotation = generate_annotation_for_image(image_path, difficulty)
        
        # Create output filename
        image_filename = os.path.basename(image_path)
        annotation_filename = os.path.splitext(image_filename)[0] + "_annotation.json"
        annotation_path = os.path.join(annotations_dir, annotation_filename)
        
        # Save annotation
        with open(annotation_path, 'w', encoding='utf-8') as f:
            json.dump(annotation, f, indent=2, ensure_ascii=False)
        
        # Progress update
        if idx % 1000 == 0 or idx == len(image_files):
            print(f"  Generated {idx}/{len(image_files)} annotations for {difficulty}")
    
    print(f"✅ Completed {difficulty}: {len(image_files)} annotation files saved to {annotations_dir}")

def generate_summary_file(base_path, output_dir):
    """Generate a summary file with question statistics."""
    summary = {
        "dataset_info": {
            "name": "VQG Shapes Dataset",
            "total_difficulties": 3,
            "difficulties": ["easy", "medium", "hard"]
        },
        "question_types": {},
        "statistics": {}
    }
    
    # Collect question type information
    for difficulty, questions in QUESTIONS_CONFIG.items():
        summary["question_types"][difficulty] = []
        for q in questions:
            summary["question_types"][difficulty].append({
                "type": q["type"],
                "template": q["template"]
            })
    
    # Collect statistics
    for difficulty in ["easy", "medium", "hard"]:
        images_dir = os.path.join(base_path, "generated_images", difficulty)
        image_files = get_image_files(images_dir)
        
        summary["statistics"][difficulty] = {
            "total_images": len(image_files),
            "questions_per_image": len(QUESTIONS_CONFIG.get(difficulty, [])),
            "total_questions": len(image_files) * len(QUESTIONS_CONFIG.get(difficulty, []))
        }
    
    # Save summary
    summary_path = os.path.join(output_dir, "annotation_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Summary saved to {summary_path}")

def main():
    """Main function to generate all annotations."""
    # Base paths
    base_path = "/home/r64/Desktop/Desktop/CV/VQG-Dataset/VQG_SHAPES_DATA/data"
    output_dir = "/home/r64/Desktop/Desktop/CV/VQG-Dataset/VQG_SHAPES_DATA/annotations"
    
    # Create main annotations directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("🚀 Starting VQG Dataset Annotation Generation")
    print(f"Input directory: {base_path}")
    print(f"Output directory: {output_dir}")
    print("-" * 60)
    
    # Generate annotations for each difficulty
    difficulties = ["easy", "medium", "hard"]
    
    for difficulty in difficulties:
        generate_annotations_for_difficulty(difficulty, base_path, output_dir)
        print()
    
    # Generate summary file
    generate_summary_file(base_path, output_dir)
    
    print("-" * 60)
    print("🎉 Annotation generation completed!")
    print(f"📁 Check the '{output_dir}' directory for all annotation files")
    print("\nNext steps:")
    print("1. Review the generated annotation JSON files")
    print("2. Fill in the 'answer' fields with actual answers")
    print("3. Validate the annotations")

if __name__ == "__main__":
    main()
