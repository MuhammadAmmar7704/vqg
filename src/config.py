import os

# Base paths
BASE_PATH = r"C:\Users\800 G2\Desktop\vqg_shapes_project\data"
INDIVIDUAL_SHAPES_PATH = os.path.join(BASE_PATH, "individual_shapes")
GENERATED_IMAGES_PATH = os.path.join(BASE_PATH, "generated_images")

# Shape categories
SHAPE_CATEGORIES = [
    "circle", "square", "triangle", "rectangle", "star",
    "oval", "pentagon", "hexagon", "heart", "diamond"
]

# ASD-friendly colors (BGR for OpenCV)
ASD_COLORS = [
    (232, 232, 169),  # #A9E8E8
    (210, 204, 131),  # #83CCD2
    (158, 226, 245),  # #F5E29E
    (136, 207, 226),  # #E2CF88
    (242, 204, 210),  # #D2CCF2
    (226, 185, 190),  # #BEB9E2
    (202, 183, 232),  # #E8B7CA
    (200, 176, 216),  # #D8B0C8
    (162, 139, 246),  # #F68BA2
    (243, 207, 223),  # #DFCFF3
    (239, 225, 173),  # #ADE1EF
    (238, 234, 198),  # #C6EAEE
    (211, 234, 178),  # #B2EAD3
    (237, 232, 177),  # #B1E8ED
    (213, 189, 237),  # #EDBDD5
    (239, 235, 200),  # #C8EBEF
    (234, 243, 192),  # #C0F3EA
    (214, 244, 245)   # #F5F4D6
]

# Difficulty Level Configurations
EASY_CONFIG = {
    'name': 'easy',
    'shapes_count_range': (1, 3),      # 1-3 shapes per image
    'canvas_size': (400, 400),
    'available_shapes': ["circle", "square", "triangle", "rectangle"],  # Basic shapes only
    'available_colors': ASD_COLORS[:6],  # First 6 colors only
    'size_variations': ['medium'],       # Only medium size
    'allow_overlap': False,              # No overlapping for easy
    'num_images': 1000,
    'output_folder': os.path.join(GENERATED_IMAGES_PATH, 'easy')
}

MEDIUM_CONFIG = {
    'name': 'medium',
    'shapes_count_range': (4, 5),       # 4-5 shapes per image
    'canvas_size': (500, 500),
    'available_shapes': ["circle", "square", "triangle", "rectangle", "star", "oval"],
    'available_colors': ASD_COLORS[:12], # First 12 colors
    'size_variations': ['small', 'large'],  # Size variations introduced
    'allow_overlap': False,              # Still no overlap
    'num_images': 1000,
    'output_folder': os.path.join(GENERATED_IMAGES_PATH, 'medium')
}

HARD_CONFIG = {
    'name': 'hard',
    'shapes_count_range': (5, 7),       # 5-7 shapes per image
    'canvas_size': (600, 600),
    'available_shapes': SHAPE_CATEGORIES,  # All shapes available
    'available_colors': ASD_COLORS,      # All colors available
    'size_variations': ['small', 'medium', 'large'],  # All size variations
    'allow_overlap': True,               # Overlapping allowed for complexity
    'num_images': 1000,
    'output_folder': os.path.join(GENERATED_IMAGES_PATH, 'hard')
}

# Size factors for different variations
SIZE_FACTORS = {
    'small': (0.08, 0.15),    # 8-15% of canvas
    'medium': (0.15, 0.25),   # 15-25% of canvas
    'large': (0.25, 0.35)     # 25-35% of canvas
}

# Image generation settings
IMG_GENERATION_SETTINGS = {
    'individual_shapes': {
        'num_per_shape': 1000,
        'img_size': 256,
        'min_size_factor': 0.15,
        'max_size_factor': 0.30
    }
}