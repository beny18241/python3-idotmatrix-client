#!/usr/bin/env python3
"""
Create a fullscreen BUSY GIF for iDotMatrix
Large, clear "BUSY" text that fills the entire screen
"""

import os
import math
from PIL import Image, ImageDraw

def create_busy_gif_fullscreen():
    """Create animated BUSY text that fills the entire screen"""
    
    frames = []
    size = 32  # 32x32 pixels
    
    for frame in range(20):
        img = Image.new('RGB', (size, size), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        progress = frame / 19.0
        
        # Large pulsing "BUSY" text that fills the screen
        if progress > 0.1:
            text_progress = min(1.0, (progress - 0.1) / 0.9)
            
            # Pulsing effect
            pulse = 1 + 0.3 * math.sin(progress * 6 * math.pi)
            
            # Draw "BUSY" in large 3x3 pixel blocks
            if text_progress > 0.2:
                # B - 3x3 blocks
                for y in range(0, 7):
                    for x in range(0, 4):
                        if x == 0 or (y == 0) or (y == 3) or (y == 6) or (x == 3 and y < 4):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 0, 0))
                
                # U - 3x3 blocks
                for y in range(0, 7):
                    for x in range(5, 9):
                        if x == 5 or x == 8 or (y == 6):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 0, 0))
                
                # S - 3x3 blocks
                for y in range(0, 7):
                    for x in range(10, 14):
                        if (y == 0) or (y == 3) or (y == 6) or (x == 10 and y < 4) or (x == 13 and y > 3):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 0, 0))
                
                # Y - 3x3 blocks
                for y in range(0, 7):
                    for x in range(15, 19):
                        if (x == 16 and y < 4) or (x == 17 and y < 4) or (y == 3 and x > 15) or (y > 3 and (x == 15 or x == 18)):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 0, 0))
        
        # Add pulsing red border
        if progress > 0.3:
            border_progress = min(1.0, (progress - 0.3) / 0.7)
            border_intensity = int(255 * border_progress * pulse)
            
            # Draw border around the entire screen
            for i in range(2):
                # Top and bottom borders
                for x in range(size):
                    if 0 <= x < size:
                        draw.point((x, i), fill=(border_intensity, 0, 0))
                        draw.point((x, size-1-i), fill=(border_intensity, 0, 0))
                
                # Left and right borders
                for y in range(size):
                    if 0 <= y < size:
                        draw.point((i, y), fill=(border_intensity, 0, 0))
                        draw.point((size-1-i, y), fill=(border_intensity, 0, 0))
        
        frames.append(img)
    
    gif_path = "images/demo_64.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=200, loop=0)
    print(f"✅ Created fullscreen BUSY GIF: {gif_path}")
    return gif_path

if __name__ == "__main__":
    print("🎬 Creating fullscreen BUSY GIF for iDotMatrix...")
    
    # Create the GIF
    busy_gif = create_busy_gif_fullscreen()
    
    print(f"\n🎉 Fullscreen BUSY GIF created successfully!")
    print(f"📁 BUSY GIF: {busy_gif}")
    print("\n💡 This GIF has large 'BUSY' text that fills the entire screen")
