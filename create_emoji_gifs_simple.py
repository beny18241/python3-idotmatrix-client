#!/usr/bin/env python3
"""
Create simple animated emoji GIFs for iDotMatrix calendar status
Large, centered visuals without text complications
"""

import os
import math
from PIL import Image, ImageDraw

def create_free_emoji_gif():
    """Create animated green checkmark for FREE status - large and centered"""
    
    frames = []
    size = 32  # 32x32 pixels
    
    for frame in range(20):
        img = Image.new('RGB', (size, size), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        progress = frame / 19.0
        
        # Large centered checkmark
        center_x, center_y = 16, 16
        radius = 12  # Large radius for maximum visibility
        
        # Pulsing effect
        pulse_radius = radius + int(3 * math.sin(progress * 4 * math.pi))
        
        if progress > 0.1:
            # Draw large circle
            for r in range(pulse_radius - 2, pulse_radius + 2):
                for angle in range(0, 360, 3):
                    x = center_x + int(r * math.cos(math.radians(angle)))
                    y = center_y + int(r * math.sin(math.radians(angle)))
                    if 0 <= x < size and 0 <= y < size:
                        draw.point((x, y), fill=(0, 255, 0))
            
            # Draw large checkmark
            if progress > 0.3:
                check_progress = min(1.0, (progress - 0.3) / 0.7)
                
                # Left line of checkmark
                for i in range(int(8 * check_progress)):
                    for thickness in range(3):
                        x = center_x - 6 + i
                        y = center_y + 2 + i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(0, 255, 0))
                
                # Right line of checkmark
                if check_progress > 0.6:
                    for i in range(int(10 * (check_progress - 0.6) / 0.4)):
                        for thickness in range(3):
                            x = center_x + 2 + i
                            y = center_y - 4 - i + thickness
                            if 0 <= x < size and 0 <= y < size:
                                draw.point((x, y), fill=(0, 255, 0))
        
        frames.append(img)
    
    gif_path = "images/free_emoji_simple.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created FREE emoji GIF: {gif_path}")
    return gif_path

def create_busy_emoji_gif():
    """Create animated red X for BUSY status - large and centered"""
    
    frames = []
    size = 32  # 32x32 pixels
    
    for frame in range(20):
        img = Image.new('RGB', (size, size), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        progress = frame / 19.0
        
        # Large centered X
        center_x, center_y = 16, 16
        radius = 12  # Large radius for maximum visibility
        
        # Pulsing effect
        pulse_radius = radius + int(3 * math.sin(progress * 4 * math.pi))
        
        if progress > 0.1:
            # Draw large circle
            for r in range(pulse_radius - 2, pulse_radius + 2):
                for angle in range(0, 360, 3):
                    x = center_x + int(r * math.cos(math.radians(angle)))
                    y = center_y + int(r * math.sin(math.radians(angle)))
                    if 0 <= x < size and 0 <= y < size:
                        draw.point((x, y), fill=(255, 0, 0))
            
            # Draw large X
            if progress > 0.3:
                x_progress = min(1.0, (progress - 0.3) / 0.7)
                
                # Draw X lines (thick)
                for i in range(int(12 * x_progress)):
                    for thickness in range(3):
                        # Diagonal line 1 (top-left to bottom-right)
                        x1 = center_x - 6 + i
                        y1 = center_y - 6 + i + thickness
                        if 0 <= x1 < size and 0 <= y1 < size:
                            draw.point((x1, y1), fill=(255, 0, 0))
                        
                        # Diagonal line 2 (top-right to bottom-left)
                        x2 = center_x + 6 - i
                        y2 = center_y - 6 + i + thickness
                        if 0 <= x2 < size and 0 <= y2 < size:
                            draw.point((x2, y2), fill=(255, 0, 0))
        
        frames.append(img)
    
    gif_path = "images/busy_emoji_simple.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created BUSY emoji GIF: {gif_path}")
    return gif_path

def create_error_emoji_gif():
    """Create animated orange warning for ERROR status - large and centered"""
    
    frames = []
    size = 32  # 32x32 pixels
    
    for frame in range(20):
        img = Image.new('RGB', (size, size), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        progress = frame / 19.0
        
        # Large centered warning triangle
        center_x, center_y = 16, 16
        radius = 12  # Large radius for maximum visibility
        
        # Pulsing effect
        pulse_radius = radius + int(3 * math.sin(progress * 4 * math.pi))
        
        if progress > 0.1:
            # Draw large circle
            for r in range(pulse_radius - 2, pulse_radius + 2):
                for angle in range(0, 360, 3):
                    x = center_x + int(r * math.cos(math.radians(angle)))
                    y = center_y + int(r * math.sin(math.radians(angle)))
                    if 0 <= x < size and 0 <= y < size:
                        draw.point((x, y), fill=(255, 165, 0))
            
            # Draw large warning triangle
            if progress > 0.3:
                triangle_progress = min(1.0, (progress - 0.3) / 0.7)
                
                # Draw triangle outline
                for i in range(int(8 * triangle_progress)):
                    for thickness in range(3):
                        # Top point
                        x = center_x
                        y = center_y - 6 + i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(255, 165, 0))
                        
                        # Left side
                        x = center_x - 6 + i
                        y = center_y + 6 - i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(255, 165, 0))
                        
                        # Right side
                        x = center_x + 6 - i
                        y = center_y + 6 - i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(255, 165, 0))
            
            # Draw exclamation mark inside triangle
            if progress > 0.6:
                exclamation_progress = min(1.0, (progress - 0.6) / 0.4)
                
                # Exclamation mark
                for i in range(int(4 * exclamation_progress)):
                    for thickness in range(2):
                        x = center_x
                        y = center_y - 2 + i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(255, 165, 0))
                
                # Dot at bottom
                if exclamation_progress > 0.5:
                    draw.point((center_x, center_y + 3), fill=(255, 165, 0))
        
        frames.append(img)
    
    gif_path = "images/error_emoji_simple.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created ERROR emoji GIF: {gif_path}")
    return gif_path

if __name__ == "__main__":
    print("🎬 Creating simple animated emoji GIFs for iDotMatrix...")
    
    # Create all GIFs
    free_gif = create_free_emoji_gif()
    busy_gif = create_busy_emoji_gif()
    error_gif = create_error_emoji_gif()
    
    print("\n🎉 All simple emoji GIFs created successfully!")
    print(f"📁 FREE emoji: {free_gif}")
    print(f"📁 BUSY emoji: {busy_gif}")
    print(f"📁 ERROR emoji: {error_gif}")
    print("\n💡 These GIFs have large, centered visuals without text complications")
