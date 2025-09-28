#!/usr/bin/env python3
"""
Create animated emoji GIFs with LARGE, visible text overlays for iDotMatrix calendar status
Creates FREE, CALL, and ERROR animated emojis with prominent text
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_free_emoji_gif_with_large_text():
    """Create animated green checkmark/check emoji with large 'FREE' text for FREE status"""
    
    # Create frames for the animation
    frames = []
    size = 32  # 32x32 pixels
    
    for i in range(8):  # 8 frames for smooth animation
        # Create new image
        img = Image.new('RGB', (size, size), color=(0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        # Calculate animation progress (0 to 1)
        progress = i / 7.0
        
        # Draw animated checkmark
        center_x, center_y = size // 2, size // 2
        radius = 10  # Smaller circle to make room for text
        
        # Draw circle (grows from 0 to full size)
        circle_radius = int(radius * progress)
        if circle_radius > 0:
            draw.ellipse([center_x - circle_radius, center_y - circle_radius, 
                         center_x + circle_radius, center_y + circle_radius], 
                        fill=(0, 255, 0))  # Green
        
        # Draw checkmark (appears after circle)
        if progress > 0.3:
            check_progress = min(1.0, (progress - 0.3) / 0.7)
            
            # Checkmark points
            check_x1 = center_x - 4
            check_y1 = center_y
            check_x2 = center_x - 1
            check_y2 = center_y + 3
            check_x3 = center_x + 4
            check_y3 = center_y - 3
            
            # Draw checkmark with animation
            if check_progress > 0:
                # First part of checkmark
                if check_progress > 0.5:
                    draw.line([check_x1, check_y1, check_x2, check_y2], 
                             fill=(255, 255, 255), width=2)
                # Second part of checkmark
                if check_progress > 0.5:
                    second_progress = (check_progress - 0.5) * 2
                    end_x = int(check_x2 + (check_x3 - check_x2) * second_progress)
                    end_y = int(check_y2 + (check_y3 - check_y2) * second_progress)
                    draw.line([check_x2, check_y2, end_x, end_y], 
                             fill=(255, 255, 255), width=2)
        
        # Add extra large "FREE" text overlay - very prominent
        if progress > 0.3:  # Text appears earlier
            text_progress = min(1.0, (progress - 0.3) / 0.7)
            
            # Draw extra large pixelated "FREE" text (3x3 pixels per letter)
            if text_progress > 0.2:
                # Draw "FREE" in extra large pixels (3x3 blocks)
                # F - 3x3 block
                for y in range(1, 7):
                    for x in range(1, 4):
                        if x == 1 or (y == 1) or (y == 4):
                            # Draw 3x3 block for each pixel
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(0, 255, 0))
                
                # R - 3x3 block
                for y in range(1, 7):
                    for x in range(5, 8):
                        if x == 5 or (y == 1) or (y == 4) or (x == 7 and y > 4):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(0, 255, 0))
                
                # E - 3x3 block
                for y in range(1, 7):
                    for x in range(9, 12):
                        if x == 9 or (y == 1) or (y == 4) or (y == 6):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(0, 255, 0))
                
                # E - 3x3 block
                for y in range(1, 7):
                    for x in range(13, 16):
                        if x == 13 or (y == 1) or (y == 4) or (y == 6):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(0, 255, 0))
        
        frames.append(img)
    
    # Save as GIF
    gif_path = "images/free_emoji_with_large_text.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created FREE emoji with large text GIF: {gif_path}")
    return gif_path

def create_busy_emoji_gif_with_large_text():
    """Create animated red X or stop emoji with large 'CALL' text for BUSY status"""
    
    # Create frames for the animation
    frames = []
    size = 32  # 32x32 pixels
    
    for i in range(8):  # 8 frames for smooth animation
        # Create new image
        img = Image.new('RGB', (size, size), color=(0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        # Calculate animation progress (0 to 1)
        progress = i / 7.0
        
        # Draw animated X
        center_x, center_y = size // 2, size // 2
        radius = 10  # Smaller circle to make room for text
        
        # Draw circle (grows from 0 to full size)
        circle_radius = int(radius * progress)
        if circle_radius > 0:
            draw.ellipse([center_x - circle_radius, center_y - circle_radius, 
                         center_x + circle_radius, center_y + circle_radius], 
                        fill=(255, 0, 0))  # Red
        
        # Draw X (appears after circle)
        if progress > 0.3:
            x_progress = min(1.0, (progress - 0.3) / 0.7)
            
            # X lines
            x_size = 6
            if x_progress > 0:
                # First diagonal
                if x_progress > 0.5:
                    draw.line([center_x - x_size, center_y - x_size, 
                             center_x + x_size, center_y + x_size], 
                             fill=(255, 255, 255), width=2)
                # Second diagonal
                if x_progress > 0.5:
                    draw.line([center_x - x_size, center_y + x_size, 
                             center_x + x_size, center_y - x_size], 
                             fill=(255, 255, 255), width=2)
        
        # Add extra large "CALL" text overlay - very prominent
        if progress > 0.3:  # Text appears earlier
            text_progress = min(1.0, (progress - 0.3) / 0.7)
            
            # Draw extra large pixelated "CALL" text (3x3 pixels per letter)
            if text_progress > 0.2:
                # Draw "CALL" in extra large pixels (3x3 blocks)
                # C - 3x3 block
                for y in range(1, 7):
                    for x in range(1, 4):
                        if x == 1 or (y == 1) or (y == 6):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 0, 0))
                
                # A - 3x3 block
                for y in range(1, 7):
                    for x in range(5, 8):
                        if x == 5 or (y == 1) or (y == 4) or (x == 7 and y < 4):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 0, 0))
                
                # L - 3x3 block
                for y in range(1, 7):
                    for x in range(9, 12):
                        if x == 9 or (y == 6):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 0, 0))
                
                # L - 3x3 block
                for y in range(1, 7):
                    for x in range(13, 16):
                        if x == 13 or (y == 6):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 0, 0))
        
        frames.append(img)
    
    # Save as GIF
    gif_path = "images/busy_emoji_with_large_text.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created BUSY emoji with large text GIF: {gif_path}")
    return gif_path

def create_error_emoji_gif_with_large_text():
    """Create animated orange warning emoji with large 'ERROR' text for ERROR status"""
    
    # Create frames for the animation
    frames = []
    size = 32  # 32x32 pixels
    
    for i in range(8):  # 8 frames for smooth animation
        # Create new image
        img = Image.new('RGB', (size, size), color=(0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        # Calculate animation progress (0 to 1)
        progress = i / 7.0
        
        # Draw animated warning triangle
        center_x, center_y = size // 2, size // 2
        triangle_size = 10  # Smaller triangle to make room for text
        
        # Draw triangle (grows from 0 to full size)
        if progress > 0:
            current_size = int(triangle_size * progress)
            
            # Triangle points
            top_x = center_x
            top_y = center_y - current_size
            left_x = center_x - current_size
            left_y = center_y + current_size
            right_x = center_x + current_size
            right_y = center_y + current_size
            
            # Draw triangle
            draw.polygon([(top_x, top_y), (left_x, left_y), (right_x, right_y)], 
                        fill=(255, 165, 0))  # Orange
        
        # Draw exclamation mark (appears after triangle)
        if progress > 0.5:
            exclamation_progress = min(1.0, (progress - 0.5) / 0.5)
            
            # Exclamation mark
            exclamation_x = center_x
            exclamation_y = center_y - 2
            exclamation_height = 4
            
            if exclamation_progress > 0:
                current_height = int(exclamation_height * exclamation_progress)
                draw.line([exclamation_x, exclamation_y - current_height, 
                         exclamation_x, exclamation_y + 1], 
                         fill=(255, 255, 255), width=2)
                # Dot at bottom
                if exclamation_progress > 0.8:
                    draw.ellipse([exclamation_x - 1, exclamation_y + 1, 
                                exclamation_x + 1, exclamation_y + 3], 
                               fill=(255, 255, 255))
        
        # Add extra large "ERROR" text overlay - very prominent
        if progress > 0.3:  # Text appears earlier
            text_progress = min(1.0, (progress - 0.3) / 0.7)
            
            # Draw extra large pixelated "ERROR" text (3x3 pixels per letter)
            if text_progress > 0.2:
                # Draw "ERROR" in extra large pixels (3x3 blocks)
                # E - 3x3 block
                for y in range(1, 7):
                    for x in range(1, 4):
                        if x == 1 or (y == 1) or (y == 4) or (y == 6):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 165, 0))
                
                # R - 3x3 block
                for y in range(1, 7):
                    for x in range(5, 8):
                        if x == 5 or (y == 1) or (y == 4) or (x == 7 and y > 4):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 165, 0))
                
                # R - 3x3 block
                for y in range(1, 7):
                    for x in range(9, 12):
                        if x == 9 or (y == 1) or (y == 4) or (x == 11 and y > 4):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 165, 0))
                
                # O - 3x3 block
                for y in range(1, 7):
                    for x in range(13, 16):
                        if (x == 13 and y > 1 and y < 6) or (x == 15 and y > 1 and y < 6) or (y == 1 and x > 13 and x < 16) or (y == 6 and x > 13 and x < 16):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 165, 0))
                
                # R - 3x3 block
                for y in range(1, 7):
                    for x in range(17, 20):
                        if x == 17 or (y == 1) or (y == 4) or (x == 19 and y > 4):
                            for dy in range(3):
                                for dx in range(3):
                                    if 0 <= x*3+dx < size and 0 <= y*3+dy < size:
                                        draw.point((x*3+dx, y*3+dy), fill=(255, 165, 0))
        
        frames.append(img)
    
    # Save as GIF
    gif_path = "images/error_emoji_with_large_text.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created ERROR emoji with large text GIF: {gif_path}")
    return gif_path

def main():
    """Create all emoji GIFs with large, visible text overlays"""
    print("🎬 Creating animated emoji GIFs with LARGE text overlays for iDotMatrix...")
    
    # Create all GIFs with large text
    free_gif = create_free_emoji_gif_with_large_text()
    busy_gif = create_busy_emoji_gif_with_large_text()
    error_gif = create_error_emoji_gif_with_large_text()
    
    print("\n🎉 All emoji GIFs with large text created successfully!")
    print(f"📁 FREE emoji with large text: {free_gif}")
    print(f"📁 CALL emoji with large text: {busy_gif}")
    print(f"📁 ERROR emoji with large text: {error_gif}")
    print("\n💡 These GIFs have larger, more visible text for the iDotMatrix display")

if __name__ == "__main__":
    main()
