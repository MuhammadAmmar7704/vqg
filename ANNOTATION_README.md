# VQG Dataset Annotation Scripts

This directory contains scripts to generate annotation JSON files for the VQG (Visual Question Generation) Shapes Dataset.

## Overview

The dataset contains images with geometric shapes in three difficulty levels:
- **Easy**: 20,000 images (1-3 shapes, basic shapes, 2 questions per image)
- **Medium**: 20,000 images (4-5 shapes, more shape types, 6 questions per image)  
- **Hard**: 20,000 images (5-7 shapes, all shape types, 4 questions per image)

## Scripts Available

### 1. Main Annotation Generator
- **File**: `generate_annotations.py`
- **Purpose**: Generate annotations for all difficulty levels
- **Usage**: 
  ```bash
  conda activate myenv
  python src/generate_annotations.py
  ```

### 2. Individual Difficulty Scripts
- **Files**: 
  - `generate_annotations_easy.py` (2 questions per image)
  - `generate_annotations_medium.py` (6 questions per image)
  - `generate_annotations_hard.py` (4 questions per image)
- **Usage**:
  ```bash
  conda activate myenv
  python src/generate_annotations_easy.py
  python src/generate_annotations_medium.py
  python src/generate_annotations_hard.py
  ```

### 3. Test Script
- **File**: `test_annotations.py`
- **Purpose**: Generate sample annotations to verify format
- **Usage**:
  ```bash
  conda activate myenv
  python src/test_annotations.py
  ```

### 4. Metadata Cleanup
- **File**: `clean_metadata.py`
- **Purpose**: Remove individual image metadata files, keep dataset metadata
- **Usage**:
  ```bash
  conda activate myenv
  python src/clean_metadata.py
  ```

## Question Types by Difficulty

### Easy (2 questions)
1. **Counting**: "What are the number of shapes present in the image?"
2. **Shape Identification**: "What shapes are present in the image?"

### Medium (6 questions)
1. **Shape Identification**: "What are the types of shapes present?"
2. **Counting**: "Number of shapes of a particular type?"
3. **Size Comparison**: "What is the smallest shape present?"
4. **Size Comparison**: "What is the largest shape present?"
5. **Frequency**: "Which shape appears the most in the image?"
6. **Duplicate Detection**: "Are there any duplicates in the image?"

### Hard (4 questions)
1. **Size Comparison**: "What is the second largest shape?"
2. **Ordering**: "What are the order-wise smallest shapes?"
3. **Color Identification**: "What are the colors of the shapes present?"
4. **Counting**: "Total number of colors in the image?"

## Output Structure

Each image generates a JSON file with this structure:

```json
{
  "image_id": "hard_image_00001.png",
  "image_path": "/path/to/image.png",
  "difficulty": "hard",
  "questions": [
    {
      "id": "hard_image_00001_q1",
      "type": "size_comparison",
      "text": "What is the second largest shape?",
      "answer": "",
      "answer_type": "shape_type"
    }
  ]
}
```

## Directory Structure After Running

```
VQG_SHAPES_DATA/
├── annotations/
│   ├── easy_annotations/
│   │   ├── easy_image_00001_annotation.json
│   │   ├── easy_image_00002_annotation.json
│   │   └── ... (20,000 files)
│   ├── medium_annotations/
│   │   ├── medium_image_00001_annotation.json
│   │   └── ... (20,000 files)
│   ├── hard_annotations/
│   │   ├── hard_image_00001_annotation.json
│   │   └── ... (20,000 files)
│   └── annotation_summary.json
├── data/
│   └── generated_images/
│       ├── easy/ (20,000 PNG files)
│       ├── medium/ (20,000 PNG files)
│       └── hard/ (20,000 PNG files)
└── src/
    └── (annotation scripts)
```

## Next Steps After Generation

1. **Review Sample Files**: Check a few generated annotation files to verify format
2. **Fill in Answers**: The annotation files have empty "answer" fields that need to be populated
3. **Validation**: Create scripts to validate annotations
4. **Analysis**: Generate statistics about the dataset

## Answer Types Reference

- `number`: Integer values (e.g., "3", "5")
- `list`: Array of items (e.g., ["circle", "square"])
- `shape_type`: Single shape name (e.g., "triangle")
- `boolean`: True/False (e.g., "true", "false")
- `object_count`: Object with counts (e.g., {"circle": 2, "square": 1})
- `ordered_list`: Ordered array (e.g., ["triangle", "circle", "square"])

## Notes

- Each script includes progress tracking for large datasets
- All scripts use UTF-8 encoding for JSON files
- Error handling included for missing images or directories
- Scripts are designed to handle 20,000+ images efficiently
