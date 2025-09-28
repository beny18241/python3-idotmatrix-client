#!/usr/bin/env python3
"""
Create enhanced busy GIF with additional text for iDotMatrix
Red X with multiple text overlays for BUSY status
"""

import os
import math
from PIL import Image, ImageDraw

def create_enhanced_busy_gif():
    """Create animated red X with multiple text overlays for BUSY status"""
    
    frames = []
    size = 32  # 32x32 pixels
    
    for frame in range(20):
        img = Image.new('RGB', (size, size), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        progress = frame / 19.0
        
        # Large red X in center
        center_x, center_y = 16, 16
        radius = 10  # Good size for visibility
        
        # Pulsing effect
        pulse_radius = radius + int(2 * math.sin(progress * 4 * math.pi))
        
        if progress > 0.1:
            # Draw large red circle
            for r in range(pulse_radius - 1, pulse_radius + 1):
                for angle in range(0, 360, 3):
                    x = center_x + int(r * math.cos(math.radians(angle)))
                    y = center_y + int(r * math.sin(math.radians(angle)))
                    if 0 <= x < size and 0 <= y < size:
                        draw.point((x, y), fill=(255, 0, 0))
            
            # Draw white X inside
            if progress > 0.3:
                x_progress = min(1.0, (progress - 0.3) / 0.7)
                
                # Draw X with thick white lines
                for i in range(int(8 * x_progress)):
                    for thickness in range(3):
                        # Diagonal line 1 (top-left to bottom-right)
                        x1 = center_x - 4 + i
                        y1 = center_y - 4 + i + thickness
                        if 0 <= x1 < size and 0 <= y1 < size:
                            draw.point((x1, y1), fill=(255, 255, 255))
                        
                        # Diagonal line 2 (top-right to bottom-left)
                        x2 = center_x + 4 - i
                        y2 = center_y - 4 + i + thickness
                        if 0 <= x2 < size and 0 <= y2 < size:
                            draw.point((x2, y2), fill=(255, 255, 255))
        
        # Add "BUSY" text at bottom
        if progress > 0.4:
            text_progress = min(1.0, (progress - 0.4) / 0.6)
            if text_progress > 0.2:
                # Draw "BUSY" in small pixels at bottom
                text_y = 28
                # B
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + 4 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((4 + x, text_y + 2 + y), fill=(255, 0, 0))
                
                # U
                for y in range(2):
                    for x in range(2):
                        draw.point((6 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((8 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((6 + x, text_y + 4 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((8 + x, text_y + 4 + y), fill=(255, 0, 0))
                
                # S
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + 4 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((12 + x, text_y + 2 + y), fill=(255, 0, 0))
                
                # Y
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((16 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((15 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((15 + x, text_y + 4 + y), fill=(255, 0, 0))
        
        # Add "MEETING" text at top
        if progress > 0.6:
            meeting_progress = min(1.0, (progress - 0.6) / 0.4)
            if meeting_progress > 0.3:
                # Draw "MEETING" in small pixels at top
                text_y = 2
                # M
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((4 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((6 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((8 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((8 + x, text_y + 2 + y), fill=(255, 0, 0))
                
                # E
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + 4 + y), fill=(255, 0, 0))
                
                # E
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + 4 + y), fill=(255, 0, 0))
                
                # T
                for y in range(2):
                    for x in range(2):
                        draw.point((18 + x, text_y + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((18 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((18 + x, text_y + 4 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((20 + x, text_y + 2 + y), fill=(255, 0, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((22 + x, text_y + 2 + y), fill=(255, 0, 0))
        
        frames.append(img)
    
    gif_path = "images/busy_emoji_with_text.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=200, loop=0)
    print(f"✅ Created enhanced BUSY GIF: {gif_path}")
    return gif_path

if __name__ == "__main__":
    print("🎬 Creating enhanced busy GIF with additional text...")
    
    # Create the enhanced GIF
    busy_gif = create_enhanced_busy_gif()
    
    print(f"\n🎉 Enhanced BUSY GIF created successfully!")
    print(f"📁 BUSY GIF: {busy_gif}")
    print("\n💡 This GIF has 'BUSY' at bottom and 'MEETING' at top")
