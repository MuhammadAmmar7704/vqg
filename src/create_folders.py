import os
from pathlib import Path
from config import BASE_PATH, INDIVIDUAL_SHAPES_PATH, GENERATED_IMAGES_PATH, SHAPE_CATEGORIES

def create_folder_structure():
    # Create base directories
    BASE_PATH.mkdir(parents=True, exist_ok=True)
    INDIVIDUAL_SHAPES_PATH.mkdir(parents=True, exist_ok=True)
    GENERATED_IMAGES_PATH.mkdir(parents=True, exist_ok=True)
    
    # Create individual shape folders
    for shape in SHAPE_CATEGORIES:
        shape_dir = INDIVIDUAL_SHAPES_PATH / shape
        shape_dir.mkdir(parents=True, exist_ok=True)
    
    # Create generated images folders by difficulty
    difficulties = ["easy", "medium", "hard"]
    for difficulty in difficulties:
        difficulty_dir = GENERATED_IMAGES_PATH / difficulty
        difficulty_dir.mkdir(parents=True, exist_ok=True)
    
    print("Folder structure created successfully!")
    print(f"Base path: {BASE_PATH}")
    print(f"Individual shapes: {INDIVIDUAL_SHAPES_PATH}")
    print(f"Generated images: {GENERATED_IMAGES_PATH}")

if __name__ == "__main__":
    create_folder_structure()