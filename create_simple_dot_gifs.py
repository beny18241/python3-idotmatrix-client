#!/usr/bin/env python3
"""
Create simple dot GIFs for iDotMatrix
Red dot with white X for BUSY, green dot with white tick for FREE
"""

import os
import math
from PIL import Image, ImageDraw

def create_free_dot_gif():
    """Create animated green dot with white tick for FREE status"""
    
    frames = []
    size = 32  # 32x32 pixels
    
    for frame in range(20):
        img = Image.new('RGB', (size, size), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        progress = frame / 19.0
        
        # Large green dot in center
        center_x, center_y = 16, 16
        radius = 12  # Large dot
        
        # Pulsing effect
        pulse_radius = radius + int(3 * math.sin(progress * 4 * math.pi))
        
        if progress > 0.1:
            # Draw large green circle
            for r in range(pulse_radius - 2, pulse_radius + 2):
                for angle in range(0, 360, 3):
                    x = center_x + int(r * math.cos(math.radians(angle)))
                    y = center_y + int(r * math.sin(math.radians(angle)))
                    if 0 <= x < size and 0 <= y < size:
                        draw.point((x, y), fill=(0, 255, 0))
            
            # Draw white tick inside
            if progress > 0.3:
                tick_progress = min(1.0, (progress - 0.3) / 0.7)
                
                # Draw tick with thick white lines
                for i in range(int(8 * tick_progress)):
                    for thickness in range(3):
                        # Left line of tick
                        x = center_x - 4 + i
                        y = center_y + 1 + i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(255, 255, 255))
                
                # Right line of tick
                if tick_progress > 0.6:
                    for i in range(int(10 * (tick_progress - 0.6) / 0.4)):
                        for thickness in range(3):
                            x = center_x + 1 + i
                            y = center_y - 3 - i + thickness
                            if 0 <= x < size and 0 <= y < size:
                                draw.point((x, y), fill=(255, 255, 255))
        
        frames.append(img)
    
    gif_path = "images/demo.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=200, loop=0)
    print(f"✅ Created FREE dot GIF: {gif_path}")
    return gif_path

def create_busy_dot_gif():
    """Create animated red dot with white X for BUSY status"""
    
    frames = []
    size = 32  # 32x32 pixels
    
    for frame in range(20):
        img = Image.new('RGB', (size, size), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        progress = frame / 19.0
        
        # Large red dot in center
        center_x, center_y = 16, 16
        radius = 12  # Large dot
        
        # Pulsing effect
        pulse_radius = radius + int(3 * math.sin(progress * 4 * math.pi))
        
        if progress > 0.1:
            # Draw large red circle
            for r in range(pulse_radius - 2, pulse_radius + 2):
                for angle in range(0, 360, 3):
                    x = center_x + int(r * math.cos(math.radians(angle)))
                    y = center_y + int(r * math.sin(math.radians(angle)))
                    if 0 <= x < size and 0 <= y < size:
                        draw.point((x, y), fill=(255, 0, 0))
            
            # Draw white X inside
            if progress > 0.3:
                x_progress = min(1.0, (progress - 0.3) / 0.7)
                
                # Draw X with thick white lines
                for i in range(int(10 * x_progress)):
                    for thickness in range(3):
                        # Diagonal line 1 (top-left to bottom-right)
                        x1 = center_x - 5 + i
                        y1 = center_y - 5 + i + thickness
                        if 0 <= x1 < size and 0 <= y1 < size:
                            draw.point((x1, y1), fill=(255, 255, 255))
                        
                        # Diagonal line 2 (top-right to bottom-left)
                        x2 = center_x + 5 - i
                        y2 = center_y - 5 + i + thickness
                        if 0 <= x2 < size and 0 <= y2 < size:
                            draw.point((x2, y2), fill=(255, 255, 255))
        
        frames.append(img)
    
    gif_path = "images/demo_64.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=200, loop=0)
    print(f"✅ Created BUSY dot GIF: {gif_path}")
    return gif_path

if __name__ == "__main__":
    print("🎬 Creating simple dot GIFs for iDotMatrix...")
    
    # Create both GIFs
    free_gif = create_free_dot_gif()
    busy_gif = create_busy_dot_gif()
    
    print(f"\n🎉 Simple dot GIFs created successfully!")
    print(f"📁 FREE dot: {free_gif}")
    print(f"📁 BUSY dot: {busy_gif}")
    print("\n💡 These GIFs have colored dots with white symbols")
