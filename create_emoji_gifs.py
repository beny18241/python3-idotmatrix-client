#!/usr/bin/env python3
"""
Create animated emoji GIFs for iDotMatrix calendar status
Creates FREE and BUSY animated emojis
"""

import os
from PIL import Image, ImageDraw
import numpy as np

def create_free_emoji_gif():
    """Create animated green checkmark/check emoji for FREE status"""
    
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
        radius = 12
        
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
            check_x1 = center_x - 6
            check_y1 = center_y
            check_x2 = center_x - 2
            check_y2 = center_y + 4
            check_x3 = center_x + 6
            check_y3 = center_y - 4
            
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
        
        frames.append(img)
    
    # Save as GIF
    gif_path = "images/free_emoji.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created FREE emoji GIF: {gif_path}")
    return gif_path

def create_busy_emoji_gif():
    """Create animated red X or stop emoji for BUSY status"""
    
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
        radius = 12
        
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
            x_size = 8
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
        
        frames.append(img)
    
    # Save as GIF
    gif_path = "images/busy_emoji.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created BUSY emoji GIF: {gif_path}")
    return gif_path

def create_error_emoji_gif():
    """Create animated orange warning emoji for ERROR status"""
    
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
        triangle_size = 12
        
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
            exclamation_height = 6
            
            if exclamation_progress > 0:
                current_height = int(exclamation_height * exclamation_progress)
                draw.line([exclamation_x, exclamation_y - current_height, 
                         exclamation_x, exclamation_y + 2], 
                         fill=(255, 255, 255), width=2)
                # Dot at bottom
                if exclamation_progress > 0.8:
                    draw.ellipse([exclamation_x - 1, exclamation_y + 2, 
                                exclamation_x + 1, exclamation_y + 4], 
                               fill=(255, 255, 255))
        
        frames.append(img)
    
    # Save as GIF
    gif_path = "images/error_emoji.gif"
    os.makedirs("images", exist_ok=True)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                   duration=150, loop=0)
    print(f"✅ Created ERROR emoji GIF: {gif_path}")
    return gif_path

def main():
    """Create all emoji GIFs"""
    print("🎬 Creating animated emoji GIFs for iDotMatrix...")
    
    # Create all GIFs
    free_gif = create_free_emoji_gif()
    busy_gif = create_busy_emoji_gif()
    error_gif = create_error_emoji_gif()
    
    print("\n🎉 All emoji GIFs created successfully!")
    print(f"📁 FREE emoji: {free_gif}")
    print(f"📁 BUSY emoji: {busy_gif}")
    print(f"📁 ERROR emoji: {error_gif}")
    print("\n💡 These GIFs can now be used with the iDotMatrix --set-gif command")

if __name__ == "__main__":
    main()
