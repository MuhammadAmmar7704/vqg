import os

def create_folder_structure():
    # Define base directories
    base_dirs = [
        "data/individual_shapes",  # Note: Fixed typo from your original ('shapes' vs 'shapes')
        "data/generated_images"
    ]
    
    # Define shape types
    shapes = [
        "circle", "square", "triangle", "rectangle", "star",
        "oval", "pentagon", "hexagon", "heart", "diamond"
    ]
    
    # Define difficulty levels
    difficulties = ["easy", "medium", "hard"]
    
    # Create base directories
    for dir_path in base_dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # Create individual shape folders
    for shape in shapes:
        os.makedirs(f"data/individual_shapes/{shape}", exist_ok=True)
    
    # Create generated images folders by difficulty
    for difficulty in difficulties:
        os.makedirs(f"data/generated_images/{difficulty}", exist_ok=True)
    
    print("Folder structure created successfully!")

if __name__ == "__main__":
    create_folder_structure()