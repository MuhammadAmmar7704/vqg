import os
import cv2
import numpy as np
import random
import json
from pathlib import Path
from config import *

class ShapeInfo:
    """Store information about a shape in the combined image"""
    def __init__(self, shape_type, color_name, size_category, position, size_pixels):
        self.shape_type = shape_type
        self.color_name = color_name
        self.size_category = size_category  # 'small', 'medium', 'large'
        self.position = position
        self.size_pixels = size_pixels

def load_shape_image(shape_type):
    """Load a random individual shape image from the pre-generated folder"""
    shape_folder = Path(INDIVIDUAL_SHAPES_PATH) / shape_type
    
    if not shape_folder.exists():
        raise FileNotFoundError(f"Shape folder not found: {shape_folder}")
    
    # Get all PNG files in the shape folder
    shape_files = list(shape_folder.glob(f"{shape_type}*.png"))
    
    if not shape_files:
        raise FileNotFoundError(f"No images found in {shape_folder}")
    
    # Pick a random shape image
    random_shape_file = random.choice(shape_files)
    
    # Load the image
    shape_img = cv2.imread(str(random_shape_file))
    
    if shape_img is None:
        raise ValueError(f"Could not load image: {random_shape_file}")
    
    return shape_img

def extract_shape_from_image(shape_img):
    """Extract the shape from white background and return shape data"""
    # Convert to grayscale to find the shape
    gray = cv2.cvtColor(shape_img, cv2.COLOR_BGR2GRAY)
    
    # Find contours (shape should be non-white pixels)
    mask = gray < 240  # Non-white pixels
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None, None, None, None
    
    # Get the largest contour (should be our shape)
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get bounding rectangle
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Extract the shape region with some padding
    padding = 5
    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(shape_img.shape[1], x + w + padding)
    y2 = min(shape_img.shape[0], y + h + padding)
    
    shape_region = shape_img[y1:y2, x1:x2]
    shape_mask = mask[y1:y2, x1:x2]
    
    # Get the dominant color of the shape
    shape_pixels = shape_region[shape_mask]
    if len(shape_pixels) > 0:
        dominant_color = np.median(shape_pixels, axis=0).astype(int)
    else:
        dominant_color = [128, 128, 128]  # Gray fallback
    
    return shape_region, shape_mask, tuple(dominant_color), max(w, h)

def get_color_name(bgr_color):
    """Map BGR color to a readable name"""
    color_names = {
        (232, 232, 169): "light_blue",
        (210, 204, 131): "teal", 
        (158, 226, 245): "yellow",
        (136, 207, 226): "beige",
        (242, 204, 210): "light_purple",
        (226, 185, 190): "lavender",
        (202, 183, 232): "pink",
        (200, 176, 216): "light_pink",
        (162, 139, 246): "orange",
        (243, 207, 223): "soft_purple",
        (239, 225, 173): "soft_blue",
        (238, 234, 198): "mint",
        (211, 234, 178): "light_green",
        (237, 232, 177): "pale_blue",
        (213, 189, 237): "purple",
        (239, 235, 200): "pale_mint",
        (234, 243, 192): "light_mint",
        (214, 244, 245): "cream"
    }
    
    # Find closest color match
    min_distance = float('inf')
    closest_color_name = "unknown"
    
    for color_bgr, name in color_names.items():
        distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(bgr_color, color_bgr)))
        if distance < min_distance:
            min_distance = distance
            closest_color_name = name
    
    return closest_color_name

def resize_shape(shape_region, shape_mask, target_size, size_category):
    """Resize shape to target size category"""
    current_size = max(shape_region.shape[:2])
    
    if current_size == 0:
        return shape_region, shape_mask
    
    # Calculate scale factor based on size category
    if size_category == 'small':
        scale_factor = target_size / current_size * 0.7
    elif size_category == 'medium':
        scale_factor = target_size / current_size * 1.0
    else:  # large
        scale_factor = target_size / current_size * 1.3
    
    new_width = int(shape_region.shape[1] * scale_factor)
    new_height = int(shape_region.shape[0] * scale_factor)
    
    if new_width > 0 and new_height > 0:
        resized_shape = cv2.resize(shape_region, (new_width, new_height))
        resized_mask = cv2.resize(shape_mask.astype(np.uint8), (new_width, new_height))
        resized_mask = resized_mask > 0  # Convert back to boolean
    else:
        resized_shape = shape_region
        resized_mask = shape_mask
    
    return resized_shape, resized_mask

def check_overlap(center1, size1, center2, size2, margin=20):
    """Check if two shapes would overlap (with margin for no overlap)"""
    distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
    return distance < (size1 + size2 + margin)

def place_shape_on_canvas(canvas, shape_region, shape_mask, center):
    """Place a shape on the canvas at the specified center"""
    shape_h, shape_w = shape_region.shape[:2]
    canvas_h, canvas_w = canvas.shape[:2]
    
    # Calculate placement coordinates
    start_x = center[0] - shape_w // 2
    start_y = center[1] - shape_h // 2
    end_x = start_x + shape_w
    end_y = start_y + shape_h
    
    # Check boundaries and adjust if necessary
    if start_x < 0:
        shape_region = shape_region[:, -start_x:]
        shape_mask = shape_mask[:, -start_x:]
        start_x = 0
    if start_y < 0:
        shape_region = shape_region[-start_y:, :]
        shape_mask = shape_mask[-start_y:, :]
        start_y = 0
    if end_x > canvas_w:
        shape_region = shape_region[:, :canvas_w-start_x]
        shape_mask = shape_mask[:, :canvas_w-start_x]
        end_x = canvas_w
    if end_y > canvas_h:
        shape_region = shape_region[:canvas_h-start_y, :]
        shape_mask = shape_mask[:canvas_h-start_y, :]
        end_y = canvas_h
    
    # Place the shape on canvas where mask is True
    if shape_region.size > 0 and shape_mask.size > 0:
        canvas_region = canvas[start_y:end_y, start_x:end_x]
        canvas_region[shape_mask] = shape_region[shape_mask]

def generate_combined_image(config):
    """Generate a single combined image using pre-generated individual shapes"""
    canvas_width, canvas_height = config['canvas_size']
    canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255
    
    # Determine number of shapes
    num_shapes = random.randint(*config['shapes_count_range'])
    
    shapes_info = []
    placed_shapes = []  # For overlap checking: (center, approximate_radius)
    
    max_attempts = 100  # Prevent infinite loops
    
    for _ in range(num_shapes):
        attempts = 0
        shape_placed = False
        
        while attempts < max_attempts and not shape_placed:
            # Choose random shape and size category
            shape_type = random.choice(config['available_shapes'])
            size_category = random.choice(config['size_variations'])
            
            try:
                # Load individual shape image
                shape_img = load_shape_image(shape_type)
                
                # Extract shape data
                shape_region, shape_mask, dominant_color, original_size = extract_shape_from_image(shape_img)
                
                if shape_region is None:
                    attempts += 1
                    continue
                
                # Calculate target size based on canvas and category
                min_factor, max_factor = SIZE_FACTORS[size_category]
                target_size = int(random.uniform(min_factor, max_factor) * min(canvas_width, canvas_height))
                
                # Resize shape
                resized_shape, resized_mask = resize_shape(shape_region, shape_mask, target_size, size_category)
                
                # Calculate approximate radius for overlap checking
                shape_radius = max(resized_shape.shape[:2]) // 2
                
                # Generate position with margins
                margin = shape_radius + 20
                if canvas_width - 2 * margin > 0 and canvas_height - 2 * margin > 0:
                    center_x = random.randint(margin, canvas_width - margin)
                    center_y = random.randint(margin, canvas_height - margin)
                    center = (center_x, center_y)
                else:
                    # If margins too large, place in center area
                    center = (canvas_width // 2, canvas_height // 2)
                
                # Check for overlap - NO OVERLAPPING ALLOWED
                overlap_detected = False
                for placed_center, placed_radius in placed_shapes:
                    if check_overlap(center, shape_radius, placed_center, placed_radius):
                        overlap_detected = True
                        break
                
                if not overlap_detected:
                    # Place the shape on canvas
                    place_shape_on_canvas(canvas, resized_shape, resized_mask, center)
                    
                    # Store shape information
                    color_name = get_color_name(dominant_color)
                    shape_info = ShapeInfo(shape_type, color_name, size_category, center, shape_radius * 2)
                    shapes_info.append(shape_info)
                    placed_shapes.append((center, shape_radius))
                    
                    shape_placed = True
                
            except (FileNotFoundError, ValueError) as e:
                print(f"Warning: Could not load shape {shape_type}: {e}")
                attempts += 1
                continue
            
            attempts += 1
        
        # If we couldn't place a shape after max_attempts, skip it
        if not shape_placed:
            print(f"Warning: Could not place {shape_type} after {max_attempts} attempts")
    
    return canvas, shapes_info

def save_metadata(shapes_info, output_path, difficulty, image_index):
    """Save metadata about the generated image"""
    metadata = {
        'difficulty': difficulty,
        'image_index': image_index,
        'total_shapes': len(shapes_info),
        'shapes': []
    }
    
    for shape in shapes_info:
        shape_data = {
            'type': shape.shape_type,
            'color': shape.color_name,
            'size_category': shape.size_category,
            'position': shape.position,
            'size_pixels': shape.size_pixels
        }
        metadata['shapes'].append(shape_data)
    
    # Save individual metadata file
    metadata_file = output_path.replace('.png', '_metadata.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return metadata

def generate_dataset(config):
    """Generate complete dataset for a difficulty level"""
    print(f"Generating {config['name']} dataset using pre-generated individual shapes...")
    
    # Create output directory
    os.makedirs(config['output_folder'], exist_ok=True)
    
    all_metadata = []
    
    for i in range(config['num_images']):
        try:
            # Generate combined image
            canvas, shapes_info = generate_combined_image(config)
            
            # Save image
            image_filename = f"{config['name']}_image_{i+1:05d}.png"
            image_path = os.path.join(config['output_folder'], image_filename)
            cv2.imwrite(image_path, canvas)
            
            # Save metadata
            metadata = save_metadata(shapes_info, image_path, config['name'], i+1)
            all_metadata.append(metadata)
            
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1}/{config['num_images']} images for {config['name']} dataset")
                
        except Exception as e:
            print(f"Error generating image {i+1} for {config['name']}: {e}")
            continue
    
    # Save combined metadata file
    combined_metadata_path = os.path.join(config['output_folder'], f"{config['name']}_dataset_metadata.json")
    with open(combined_metadata_path, 'w') as f:
        json.dump(all_metadata, f, indent=2)
    
    print(f"✅ Completed {config['name']} dataset: {len(all_metadata)} images generated")
    print(f"📁 Saved to: {config['output_folder']}")

def generate_all_datasets():
    """Generate all three difficulty level datasets using pre-generated shapes"""
    
    # Check if individual shapes exist
    individual_shapes_path = Path(INDIVIDUAL_SHAPES_PATH)
    if not individual_shapes_path.exists():
        print(f"❌ Error: Individual shapes directory not found at {INDIVIDUAL_SHAPES_PATH}")
        print("Please run generate_individual_shapes.py first!")
        return
    
    # Check if we have shapes for all required categories
    missing_shapes = []
    for shape in SHAPE_CATEGORIES:
        shape_folder = individual_shapes_path / shape
        if not shape_folder.exists() or not list(shape_folder.glob("*.png")):
            missing_shapes.append(shape)
    
    if missing_shapes:
        print(f"❌ Error: Missing individual shapes for: {missing_shapes}")
        print("Please run generate_individual_shapes.py first!")
        return
    
    print("✅ Found all required individual shape categories")
    print("🔄 Starting combined image generation...")
    
    configs = [EASY_CONFIG, MEDIUM_CONFIG, HARD_CONFIG]
    
    for config in configs:
        generate_dataset(config)
    
    print("\n🎉 All datasets generated successfully using pre-generated individual shapes!")
    print("📊 Summary:")
    print(f"🟢 Easy: {EASY_CONFIG['shapes_count_range'][0]}-{EASY_CONFIG['shapes_count_range'][1]} shapes, {len(EASY_CONFIG['available_shapes'])} shape types, NO OVERLAPPING")
    print(f"🟡 Medium: {MEDIUM_CONFIG['shapes_count_range'][0]}-{MEDIUM_CONFIG['shapes_count_range'][1]} shapes, {len(MEDIUM_CONFIG['available_shapes'])} shape types, NO OVERLAPPING")
    print(f"🔴 Hard: {HARD_CONFIG['shapes_count_range'][0]}-{HARD_CONFIG['shapes_count_range'][1]} shapes, {len(HARD_CONFIG['available_shapes'])} shape types, NO OVERLAPPING")

if __name__ == "__main__":
    generate_all_datasets()