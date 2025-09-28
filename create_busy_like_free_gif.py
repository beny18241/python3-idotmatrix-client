#!/usr/bin/env python3
"""
Create BUSY GIF similar to FREE but with red color and CALL text
Red checkmark with 'CALL' text for BUSY status
"""

import os
import math
from PIL import Image, ImageDraw

def create_busy_like_free_gif():
    """Create animated red checkmark with 'CALL' text for BUSY status"""
    
    frames = []
    size = 32  # 32x32 pixels
    
    for frame in range(20):
        img = Image.new('RGB', (size, size), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        progress = frame / 19.0
        
        # Large centered checkmark (like FREE but red)
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
                        draw.point((x, y), fill=(255, 0, 0))  # Red instead of green
            
            # Draw large checkmark
            if progress > 0.3:
                check_progress = min(1.0, (progress - 0.3) / 0.7)
                
                # Left line of checkmark
                for i in range(int(8 * check_progress)):
                    for thickness in range(3):
                        x = center_x - 6 + i
                        y = center_y + 2 + i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(0, 255, 0))  # White checkmark
                
                # Right line of checkmark
                if check_progress > 0.6:
                    for i in range(int(10 * (check_progress - 0.6) / 0.4)):
                        for thickness in range(3):
                            x = center_x + 2 + i
                            y = center_y - 4 - i + thickness
                            if 0 <= x < size and 0 <= y < size:
                                draw.point((x, y), fill=(0, 255, 0))  # White checkmark
        
        # Add "CALL" text at bottom (like FREE but with CALL)
        if progress > 0.5:
            text_progress = min(1.0, (progress - 0.5) / 0.5)
            if text_progress > 0.3:
                # Draw "CALL" in small pixels at bottom
                text_y = 28
                # C
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + y), fill=(255, 0, 0))  # Red text
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + 4 + y), fill=(255, 0, 0))
                
                # A
                for y in range(2):
                    for x in range(2):
                        draw.point((6 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((6 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((8 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((8 + x, text_y + 4 + y), fill=(255, 0, 0))
                
                # L
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + 4 + y), fill=(255, 0, 0))
                
                # L
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + 4 + y), fill=(255, 0, 0))
        
        frames.append(img)
    
    gif_path = "images/busy_emoji_with_text.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=200, loop=0)
    print(f"✅ Created BUSY like FREE GIF: {gif_path}")
    return gif_path

if __name__ == "__main__":
    print("🎬 Creating BUSY GIF like FREE but with red color and CALL text...")
    
    # Create the GIF
    busy_gif = create_busy_like_free_gif()
    
    print(f"\n🎉 BUSY like FREE GIF created successfully!")
    print(f"📁 BUSY GIF: {busy_gif}")
    print("\n💡 This GIF has red circle with white checkmark and 'CALL' text")
