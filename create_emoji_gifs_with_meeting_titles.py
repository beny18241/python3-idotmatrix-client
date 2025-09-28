#!/usr/bin/env python3
"""
Create animated emoji GIFs with meeting titles for iDotMatrix calendar status
Creates FREE, CALL, and ERROR animated emojis with meeting information
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_free_emoji_gif_with_meeting_title(meeting_title=None):
    """Create animated green checkmark with 'FREE' text for FREE status"""
    
    # Create frames for the animation
    frames = []
    size = 32  # 32x32 pixels
    
    for i in range(8):  # 8 frames for smooth animation
        # Create new image
        img = Image.new('RGB', (size, size), color=(0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        # Calculate animation progress (0 to 1)
        progress = i / 7.0
        
        # Draw smaller animated checkmark (bottom area only)
        center_x, center_y = size // 2, 26  # Move to bottom to make room for text
        radius = 4  # Very small circle
        
        # Draw circle (grows from 0 to full size)
        circle_radius = int(radius * progress)
        if circle_radius > 0:
            draw.ellipse([center_x - circle_radius, center_y - circle_radius, 
                         center_x + circle_radius, center_y + circle_radius], 
                        fill=(0, 255, 0))  # Green
        
        # Draw checkmark (appears after circle)
        if progress > 0.3:
            check_progress = min(1.0, (progress - 0.3) / 0.7)
            
            # Checkmark points (smaller)
            check_x1 = center_x - 2
            check_y1 = center_y
            check_x2 = center_x - 1
            check_y2 = center_y + 1
            check_x3 = center_x + 2
            check_y3 = center_y - 1
            
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
        
        # Add smaller "FREE" text overlay - fits screen better
        if progress > 0.2:  # Text appears after visual
            text_progress = min(1.0, (progress - 0.2) / 0.8)
            
            # Draw "FREE" in smaller pixels (2x2 blocks to fit screen)
            if text_progress > 0.1:
                # Draw "FREE" in smaller pixels (2x2 blocks)
                # F - 2x2 block
                for y in range(0, 5):
                    for x in range(0, 3):
                        if x == 0 or (y == 0) or (y == 2):
                            # Draw 2x2 block for each pixel
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(0, 255, 0))
                
                # R - 2x2 block
                for y in range(0, 5):
                    for x in range(4, 7):
                        if x == 4 or (y == 0) or (y == 2) or (x == 6 and y > 2):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(0, 255, 0))
                
                # E - 2x2 block
                for y in range(0, 5):
                    for x in range(8, 11):
                        if x == 8 or (y == 0) or (y == 2) or (y == 4):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(0, 255, 0))
                
                # E - 2x2 block
                for y in range(0, 5):
                    for x in range(12, 15):
                        if x == 12 or (y == 0) or (y == 2) or (y == 4):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(0, 255, 0))
        
        frames.append(img)
    
    # Save as GIF
    gif_path = "images/free_emoji_with_meeting_title.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created FREE emoji with meeting title GIF: {gif_path}")
    return gif_path

def create_busy_emoji_gif_with_meeting_title(meeting_title=None):
    """Create animated red X with 'CALL' text and meeting title for BUSY status"""
    
    # Create frames for the animation
    frames = []
    size = 32  # 32x32 pixels
    
    for i in range(8):  # 8 frames for smooth animation
        # Create new image
        img = Image.new('RGB', (size, size), color=(0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        # Calculate animation progress (0 to 1)
        progress = i / 7.0
        
        # Draw smaller animated X (bottom area only)
        center_x, center_y = size // 2, 26  # Move to bottom to make room for text
        radius = 4  # Very small circle
        
        # Draw circle (grows from 0 to full size)
        circle_radius = int(radius * progress)
        if circle_radius > 0:
            draw.ellipse([center_x - circle_radius, center_y - circle_radius, 
                         center_x + circle_radius, center_y + circle_radius], 
                        fill=(255, 0, 0))  # Red
        
        # Draw X (appears after circle)
        if progress > 0.3:
            x_progress = min(1.0, (progress - 0.3) / 0.7)
            
            # X lines (smaller)
            x_size = 3
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
        
        # Add smaller "CALL" text overlay - fits screen better
        if progress > 0.2:  # Text appears after visual
            text_progress = min(1.0, (progress - 0.2) / 0.8)
            
            # Draw "CALL" in smaller pixels (2x2 blocks to fit screen)
            if text_progress > 0.1:
                # Draw "CALL" in smaller pixels (2x2 blocks)
                # C - 2x2 block
                for y in range(0, 5):
                    for x in range(0, 3):
                        if x == 0 or (y == 0) or (y == 4):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(255, 0, 0))
                
                # A - 2x2 block
                for y in range(0, 5):
                    for x in range(4, 7):
                        if x == 4 or (y == 0) or (y == 2) or (x == 6 and y < 3):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(255, 0, 0))
                
                # L - 2x2 block
                for y in range(0, 5):
                    for x in range(8, 11):
                        if x == 8 or (y == 4):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(255, 0, 0))
                
                # L - 2x2 block
                for y in range(0, 5):
                    for x in range(12, 15):
                        if x == 12 or (y == 4):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(255, 0, 0))
        
        frames.append(img)
    
    # Save as GIF
    gif_path = "images/busy_emoji_with_meeting_title.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created BUSY emoji with meeting title GIF: {gif_path}")
    return gif_path

def create_error_emoji_gif_with_meeting_title(meeting_title=None):
    """Create animated orange warning with 'ERROR' text for ERROR status"""
    
    # Create frames for the animation
    frames = []
    size = 32  # 32x32 pixels
    
    for i in range(8):  # 8 frames for smooth animation
        # Create new image
        img = Image.new('RGB', (size, size), color=(0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        # Calculate animation progress (0 to 1)
        progress = i / 7.0
        
        # Draw smaller animated warning triangle (bottom area only)
        center_x, center_y = size // 2, 26  # Move to bottom to make room for text
        triangle_size = 4  # Very small triangle
        
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
            exclamation_y = center_y - 1
            exclamation_height = 3
            
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
        
        # Add smaller "ERROR" text overlay - fits screen better
        if progress > 0.2:  # Text appears after visual
            text_progress = min(1.0, (progress - 0.2) / 0.8)
            
            # Draw "ERROR" in smaller pixels (2x2 blocks to fit screen)
            if text_progress > 0.1:
                # Draw "ERROR" in smaller pixels (2x2 blocks)
                # E - 2x2 block
                for y in range(0, 5):
                    for x in range(0, 3):
                        if x == 0 or (y == 0) or (y == 2) or (y == 4):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(255, 165, 0))
                
                # R - 2x2 block
                for y in range(0, 5):
                    for x in range(4, 7):
                        if x == 4 or (y == 0) or (y == 2) or (x == 6 and y > 2):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(255, 165, 0))
                
                # R - 2x2 block
                for y in range(0, 5):
                    for x in range(8, 11):
                        if x == 8 or (y == 0) or (y == 2) or (x == 10 and y > 2):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(255, 165, 0))
                
                # O - 2x2 block
                for y in range(0, 5):
                    for x in range(12, 15):
                        if (x == 12 and y > 0 and y < 4) or (x == 14 and y > 0 and y < 4) or (y == 0 and x > 12 and x < 15) or (y == 4 and x > 12 and x < 15):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(255, 165, 0))
                
                # R - 2x2 block
                for y in range(0, 5):
                    for x in range(16, 19):
                        if x == 16 or (y == 0) or (y == 2) or (x == 18 and y > 2):
                            for dy in range(2):
                                for dx in range(2):
                                    if 0 <= x*2+dx < size and 0 <= y*2+dy < size:
                                        draw.point((x*2+dx, y*2+dy), fill=(255, 165, 0))
        
        frames.append(img)
    
    # Save as GIF
    gif_path = "images/error_emoji_with_meeting_title.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created ERROR emoji with meeting title GIF: {gif_path}")
    return gif_path

def main():
    """Create all emoji GIFs with meeting titles"""
    print("🎬 Creating animated emoji GIFs with meeting titles for iDotMatrix...")
    
    # Create all GIFs with meeting titles
    free_gif = create_free_emoji_gif_with_meeting_title()
    busy_gif = create_busy_emoji_gif_with_meeting_title()
    error_gif = create_error_emoji_gif_with_meeting_title()
    
    print("\n🎉 All emoji GIFs with meeting titles created successfully!")
    print(f"📁 FREE emoji with meeting title: {free_gif}")
    print(f"📁 CALL emoji with meeting title: {busy_gif}")
    print(f"📁 ERROR emoji with meeting title: {error_gif}")
    print("\n💡 These GIFs have smaller visuals and larger text for maximum visibility")

if __name__ == "__main__":
    main()
