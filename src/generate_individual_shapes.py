import os
import cv2
import numpy as np
from pathlib import Path
import random
from config import *

def draw_shape(shape_type, img_size=256, colors=None):
    """
    Draw individual shape - updated version of your existing function
    """
    if colors is None:
        colors = ASD_COLORS
    
    # White background (3 channels for color)
    img = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255

    # Random ASD-friendly color for the shape
    color = random.choice(colors)

    # Size scales with image size
    min_size = int(img_size * IMG_GENERATION_SETTINGS['individual_shapes']['min_size_factor'])
    max_size = int(img_size * IMG_GENERATION_SETTINGS['individual_shapes']['max_size_factor'])
    size = random.randint(min_size, max_size)

    # Center placement so shape doesn't get cut off
    center_margin = max_size + 5
    center = (
        random.randint(center_margin, img_size - center_margin),
        random.randint(center_margin, img_size - center_margin)
    )

    angle = random.uniform(-180, 180)

    if shape_type == "circle":
        cv2.circle(img, center, size, color, -1)
    elif shape_type == "square":
        pts = np.array([
            [center[0] - size, center[1] - size],
            [center[0] + size, center[1] - size],
            [center[0] + size, center[1] + size],
            [center[0] - size, center[1] + size]
        ])
        rot_pts = rotate_pts(pts, center, angle)
        cv2.fillPoly(img, [rot_pts], color)
    elif shape_type == "rectangle":
        pts = np.array([
            [center[0] - size, center[1] - size//2],
            [center[0] + size, center[1] - size//2],
            [center[0] + size, center[1] + size//2],
            [center[0] - size, center[1] + size//2]
        ])
        rot_pts = rotate_pts(pts, center, angle)
        cv2.fillPoly(img, [rot_pts], color)
    elif shape_type == "triangle":
        pts = np.array([
            [center[0], center[1] - size],
            [center[0] - size, center[1] + size],
            [center[0] + size, center[1] + size]
        ])
        rot_pts = rotate_pts(pts, center, angle)
        cv2.fillPoly(img, [rot_pts], color)
    elif shape_type == "star":
        pts = []
        for i in range(10):
            r = size if i % 2 == 0 else size // 2
            theta = np.pi / 5 * i
            x = int(center[0] + r * np.cos(theta))
            y = int(center[1] + r * np.sin(theta))
            pts.append((x, y))
        rot_pts = rotate_pts(np.array(pts), center, angle)
        cv2.fillPoly(img, [rot_pts], color)
    elif shape_type == "oval":
        axes = (size, size // 2)
        cv2.ellipse(img, center, axes, angle, 0, 360, color, -1)
    elif shape_type == "pentagon":
        pts = []
        for i in range(5):
            theta = 2 * np.pi * i / 5 - np.pi / 2
            x = int(center[0] + size * np.cos(theta))
            y = int(center[1] + size * np.sin(theta))
            pts.append((x, y))
        rot_pts = rotate_pts(np.array(pts), center, angle)
        cv2.fillPoly(img, [rot_pts], color)
    elif shape_type == "hexagon":
        pts = []
        for i in range(6):
            theta = 2 * np.pi * i / 6
            x = int(center[0] + size * np.cos(theta))
            y = int(center[1] + size * np.sin(theta))
            pts.append((x, y))
        rot_pts = rotate_pts(np.array(pts), center, angle)
        cv2.fillPoly(img, [rot_pts], color)
    elif shape_type == "diamond":
        pts = np.array([
            [center[0], center[1] - size],
            [center[0] + size, center[1]],
            [center[0], center[1] + size],
            [center[0] - size, center[1]]
        ])
        rot_pts = rotate_pts(pts, center, angle)
        cv2.fillPoly(img, [rot_pts], color)
    elif shape_type == "heart":
        t = np.linspace(0, 2 * np.pi, 100)
        x = (16 * np.sin(t) ** 3) * size / 32 + center[0]
        y = -(13 * np.cos(t) - 5 * np.cos(2 * t)
              - 2 * np.cos(3 * t) - np.cos(4 * t)) * size / 32 + center[1]
        pts = np.array(np.vstack((x, y)).T, np.int32)
        cv2.fillPoly(img, [pts], color)

    return img

def rotate_pts(pts, center, angle):
    """Rotate points around center"""
    rot_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    ones = np.ones(shape=(len(pts), 1))
    pts_ones = np.hstack([pts, ones])
    rotated = rot_matrix @ pts_ones.T
    return rotated.T.astype(np.int32)

def generate_individual_shapes():
    """Generate individual shapes for all categories"""
    print("Generating individual shapes...")
    
    for shape in SHAPE_CATEGORIES:
        shape_dir = Path(INDIVIDUAL_SHAPES_PATH) / shape
        shape_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Generating {IMG_GENERATION_SETTINGS['individual_shapes']['num_per_shape']} images for {shape}...")
        
        for i in range(1, IMG_GENERATION_SETTINGS['individual_shapes']['num_per_shape'] + 1):
            img = draw_shape(
                shape, 
                IMG_GENERATION_SETTINGS['individual_shapes']['img_size'],
                ASD_COLORS
            )
            cv2.imwrite(str(shape_dir / f"{shape}{i}.png"), img)
        
        print(f"✅ Completed {shape}")
    
    print("🎉 All individual shapes generated!")

if __name__ == "__main__":
    generate_individual_shapes()