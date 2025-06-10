#!/usr/bin/env python3
"""
Demo script to show the difference between black border and edge extension methods
"""

from PIL import Image, ImageDraw, ImageFont
import tempfile
from pathlib import Path
import sys
import os

# Add the parent directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from add_mpc_bleed import calculate_bleed_pixels

def create_demo_image(size=(300, 400)):
    """Create a demo card image with visible edges"""
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a colorful border around the edge
    border_width = 10
    
    # Top border (blue)
    draw.rectangle([0, 0, size[0], border_width], fill='blue')
    # Bottom border (green)  
    draw.rectangle([0, size[1]-border_width, size[0], size[1]], fill='green')
    # Left border (red)
    draw.rectangle([0, 0, border_width, size[1]], fill='red')
    # Right border (yellow)
    draw.rectangle([size[0]-border_width, 0, size[0], size[1]], fill='yellow')
    
    # Add some content in the center
    draw.rectangle([50, 50, size[0]-50, size[1]-50], fill='lightgray')
    
    # Add text
    try:
        font = ImageFont.load_default()
        text = "DEMO CARD"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        draw.text((x, y), text, fill='black', font=font)
    except:
        # Fallback if font loading fails
        draw.text((size[0]//2 - 40, size[1]//2), "DEMO CARD", fill='black')
    
    return img

def demo_edge_extension():
    """Demonstrate the edge extension method"""
    print("🎨 Edge Extension Demo")
    print("=" * 50)
    
    # Create demo image
    demo_img = create_demo_image()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        
        # Save demo image
        demo_path = temp_dir / "demo_original.png"
        demo_img.save(demo_path)
        print(f"📄 Created demo image: {demo_path}")
        
        # Apply edge extension
        from add_mpc_bleed import add_bleed_border
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        
        success = add_bleed_border(demo_path, output_dir)
        
        if success:
            output_path = output_dir / "demo_original.png"
            print(f"✅ Edge extension applied: {output_path}")
            
            # Show size comparison
            with Image.open(output_path) as extended_img:
                original_size = demo_img.size
                extended_size = extended_img.size
                
                print(f"\n📏 Size Comparison:")
                print(f"   Original: {original_size[0]} x {original_size[1]} pixels")
                print(f"   Extended: {extended_size[0]} x {extended_size[1]} pixels")
                
                width_diff = extended_size[0] - original_size[0]
                height_diff = extended_size[1] - original_size[1]
                print(f"   Added: {width_diff} pixels width, {height_diff} pixels height")
                
                # Calculate bleed percentages
                top, bottom, left, right = calculate_bleed_pixels(original_size[0], original_size[1])
                print(f"\n🎯 Bleed Areas:")
                print(f"   Left/Right: {left}/{right} pixels each (9.7%)")
                print(f"   Top/Bottom: {top}/{bottom} pixels each (6.9%)")
                
                print(f"\n🌈 The colored edges of the original image have been")
                print(f"    extended outward to create natural bleed areas!")
                
        else:
            print("❌ Failed to apply edge extension")

if __name__ == "__main__":
    demo_edge_extension()
