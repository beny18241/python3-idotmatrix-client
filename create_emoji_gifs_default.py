#!/usr/bin/env python3
"""
Create default animated emoji GIFs for iDotMatrix calendar status
Uses existing GIFs with small text overlays
"""

import os
import math
from PIL import Image, ImageDraw

def create_free_emoji_gif():
    """Create animated green checkmark for FREE status"""
    
    frames = []
    size = 32  # 32x32 pixels
    
    for frame in range(20):
        img = Image.new('RGB', (size, size), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        progress = frame / 19.0
        
        # Large centered checkmark
        center_x, center_y = 16, 16
        radius = 10  # Good size for visibility
        
        # Pulsing effect
        pulse_radius = radius + int(2 * math.sin(progress * 4 * math.pi))
        
        if progress > 0.1:
            # Draw circle
            for r in range(pulse_radius - 1, pulse_radius + 1):
                for angle in range(0, 360, 5):
                    x = center_x + int(r * math.cos(math.radians(angle)))
                    y = center_y + int(r * math.sin(math.radians(angle)))
                    if 0 <= x < size and 0 <= y < size:
                        draw.point((x, y), fill=(0, 255, 0))
            
            # Draw checkmark
            if progress > 0.3:
                check_progress = min(1.0, (progress - 0.3) / 0.7)
                
                # Left line of checkmark
                for i in range(int(6 * check_progress)):
                    for thickness in range(2):
                        x = center_x - 4 + i
                        y = center_y + 1 + i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(0, 255, 0))
                
                # Right line of checkmark
                if check_progress > 0.6:
                    for i in range(int(8 * (check_progress - 0.6) / 0.4)):
                        for thickness in range(2):
                            x = center_x + 1 + i
                            y = center_y - 3 - i + thickness
                            if 0 <= x < size and 0 <= y < size:
                                draw.point((x, y), fill=(0, 255, 0))
        
        # Add small "FREE" text at bottom
        if progress > 0.5:
            text_progress = min(1.0, (progress - 0.5) / 0.5)
            if text_progress > 0.3:
                # Draw "FREE" in small pixels
                text_y = 28
                # F
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + y), fill=(0, 255, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + 2 + y), fill=(0, 255, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + 4 + y), fill=(0, 255, 0))
                
                # R
                for y in range(2):
                    for x in range(2):
                        draw.point((6 + x, text_y + y), fill=(0, 255, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((6 + x, text_y + 2 + y), fill=(0, 255, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((8 + x, text_y + 2 + y), fill=(0, 255, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((8 + x, text_y + 4 + y), fill=(0, 255, 0))
                
                # E
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + y), fill=(0, 255, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + 2 + y), fill=(0, 255, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + 4 + y), fill=(0, 255, 0))
                
                # E
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + y), fill=(0, 255, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + 2 + y), fill=(0, 255, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + 4 + y), fill=(0, 255, 0))
        
        frames.append(img)
    
    gif_path = "images/free_emoji.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created FREE emoji GIF: {gif_path}")
    return gif_path

def create_busy_emoji_gif():
    """Create animated red X for BUSY status"""
    
    frames = []
    size = 32  # 32x32 pixels
    
    for frame in range(20):
        img = Image.new('RGB', (size, size), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        progress = frame / 19.0
        
        # Large centered X
        center_x, center_y = 16, 16
        radius = 10  # Good size for visibility
        
        # Pulsing effect
        pulse_radius = radius + int(2 * math.sin(progress * 4 * math.pi))
        
        if progress > 0.1:
            # Draw circle
            for r in range(pulse_radius - 1, pulse_radius + 1):
                for angle in range(0, 360, 5):
                    x = center_x + int(r * math.cos(math.radians(angle)))
                    y = center_y + int(r * math.sin(math.radians(angle)))
                    if 0 <= x < size and 0 <= y < size:
                        draw.point((x, y), fill=(255, 0, 0))
            
            # Draw X
            if progress > 0.3:
                x_progress = min(1.0, (progress - 0.3) / 0.7)
                
                # Draw X lines
                for i in range(int(8 * x_progress)):
                    for thickness in range(2):
                        # Diagonal line 1 (top-left to bottom-right)
                        x1 = center_x - 4 + i
                        y1 = center_y - 4 + i + thickness
                        if 0 <= x1 < size and 0 <= y1 < size:
                            draw.point((x1, y1), fill=(255, 0, 0))
                        
                        # Diagonal line 2 (top-right to bottom-left)
                        x2 = center_x + 4 - i
                        y2 = center_y - 4 + i + thickness
                        if 0 <= x2 < size and 0 <= y2 < size:
                            draw.point((x2, y2), fill=(255, 0, 0))
        
        # Add small "BUSY" text at bottom
        if progress > 0.5:
            text_progress = min(1.0, (progress - 0.5) / 0.5)
            if text_progress > 0.3:
                # Draw "BUSY" in small pixels
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
        
        frames.append(img)
    
    gif_path = "images/busy_emoji.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created BUSY emoji GIF: {gif_path}")
    return gif_path

def create_error_emoji_gif():
    """Create animated orange warning for ERROR status"""
    
    frames = []
    size = 32  # 32x32 pixels
    
    for frame in range(20):
        img = Image.new('RGB', (size, size), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        progress = frame / 19.0
        
        # Large centered warning triangle
        center_x, center_y = 16, 16
        radius = 10  # Good size for visibility
        
        # Pulsing effect
        pulse_radius = radius + int(2 * math.sin(progress * 4 * math.pi))
        
        if progress > 0.1:
            # Draw circle
            for r in range(pulse_radius - 1, pulse_radius + 1):
                for angle in range(0, 360, 5):
                    x = center_x + int(r * math.cos(math.radians(angle)))
                    y = center_y + int(r * math.sin(math.radians(angle)))
                    if 0 <= x < size and 0 <= y < size:
                        draw.point((x, y), fill=(255, 165, 0))
            
            # Draw warning triangle
            if progress > 0.3:
                triangle_progress = min(1.0, (progress - 0.3) / 0.7)
                
                # Draw triangle outline
                for i in range(int(6 * triangle_progress)):
                    for thickness in range(2):
                        # Top point
                        x = center_x
                        y = center_y - 4 + i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(255, 165, 0))
                        
                        # Left side
                        x = center_x - 4 + i
                        y = center_y + 4 - i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(255, 165, 0))
                        
                        # Right side
                        x = center_x + 4 - i
                        y = center_y + 4 - i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(255, 165, 0))
            
            # Draw exclamation mark inside triangle
            if progress > 0.6:
                exclamation_progress = min(1.0, (progress - 0.6) / 0.4)
                
                # Exclamation mark
                for i in range(int(3 * exclamation_progress)):
                    for thickness in range(2):
                        x = center_x
                        y = center_y - 1 + i + thickness
                        if 0 <= x < size and 0 <= y < size:
                            draw.point((x, y), fill=(255, 165, 0))
                
                # Dot at bottom
                if exclamation_progress > 0.5:
                    draw.point((center_x, center_y + 2), fill=(255, 165, 0))
        
        # Add small "ERROR" text at bottom
        if progress > 0.5:
            text_progress = min(1.0, (progress - 0.5) / 0.5)
            if text_progress > 0.3:
                # Draw "ERROR" in small pixels
                text_y = 28
                # E
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + 2 + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((2 + x, text_y + 4 + y), fill=(255, 165, 0))
                
                # R
                for y in range(2):
                    for x in range(2):
                        draw.point((6 + x, text_y + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((6 + x, text_y + 2 + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((8 + x, text_y + 2 + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((8 + x, text_y + 4 + y), fill=(255, 165, 0))
                
                # R
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((10 + x, text_y + 2 + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((12 + x, text_y + 2 + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((12 + x, text_y + 4 + y), fill=(255, 165, 0))
                
                # O
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((16 + x, text_y + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((14 + x, text_y + 4 + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((16 + x, text_y + 4 + y), fill=(255, 165, 0))
                
                # R
                for y in range(2):
                    for x in range(2):
                        draw.point((18 + x, text_y + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((18 + x, text_y + 2 + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((20 + x, text_y + 2 + y), fill=(255, 165, 0))
                for y in range(2):
                    for x in range(2):
                        draw.point((20 + x, text_y + 4 + y), fill=(255, 165, 0))
        
        frames.append(img)
    
    gif_path = "images/error_emoji.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created ERROR emoji GIF: {gif_path}")
    return gif_path

if __name__ == "__main__":
    print("🎬 Creating default animated emoji GIFs for iDotMatrix...")
    
    # Create all GIFs
    free_gif = create_free_emoji_gif()
    busy_gif = create_busy_emoji_gif()
    error_gif = create_error_emoji_gif()
    
    print("\n🎉 All default emoji GIFs created successfully!")
    print(f"📁 FREE emoji: {free_gif}")
    print(f"📁 BUSY emoji: {busy_gif}")
    print(f"📁 ERROR emoji: {error_gif}")
    print("\n💡 These GIFs have large visuals with small text overlays")
