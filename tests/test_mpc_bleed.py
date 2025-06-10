"""
Tests for MPC Bleed Border Tool
"""

import pytest
from pathlib import Path
from PIL import Image
import tempfile
import sys
import os

# Add the parent directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_mpc_bleed import calculate_bleed_pixels, add_bleed_border


class TestBleedCalculations:
    """Test bleed pixel calculations"""
    
    def test_calculate_bleed_pixels_standard_card(self):
        """Test bleed calculation for a standard card size"""
        # Standard playing card: 2.5" x 3.5" at 300 DPI = 750x1050 pixels
        width, height = 750, 1050
        top, bottom, left, right = calculate_bleed_pixels(width, height)
        
        # Expected: 4.84% of 750 = 36.3 -> 36 pixels horizontal per side
        # Expected: 3.47% of 1050 = 36.4 -> 36 pixels vertical per side
        assert left == right == 36  # 4.84% of 750
        assert top == bottom == 36   # 3.47% of 1050
    
    def test_calculate_bleed_pixels_small_image(self):
        """Test bleed calculation for a small image"""
        width, height = 100, 140
        top, bottom, left, right = calculate_bleed_pixels(width, height)
        
        # Expected: 4.84% of 100 = 4.84 -> 4 pixels horizontal per side
        # Expected: 3.47% of 140 = 4.86 -> 4 pixels vertical per side
        assert left == right == 4
        assert top == bottom == 4


class TestImageProcessing:
    """Test image processing functions"""
    
    def test_add_bleed_border_basic(self):
        """Test adding bleed border by extending edge pixels"""
        # Create a temporary test image
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            # Create a simple test image with distinct colors for edge detection
            test_image = Image.new('RGB', (100, 140), color=(255, 0, 0))  # Red background
            # Add colored edges to test edge extension
            for x in range(100):
                test_image.putpixel((x, 0), (0, 0, 255))  # Blue top edge
                test_image.putpixel((x, 139), (0, 255, 0))  # Green bottom edge
            for y in range(140):
                test_image.putpixel((0, y), (255, 255, 0))  # Yellow left edge
                test_image.putpixel((99, y), (255, 0, 255))  # Magenta right edge
            
            # Save as PNG to avoid JPEG compression
            input_path = temp_dir / "test_input.png"
            test_image.save(input_path)
            
            # Create output directory
            output_dir = temp_dir / "output"
            output_dir.mkdir()
            
            # Process the image
            result = add_bleed_border(input_path, output_dir)
            
            # Check if processing was successful
            assert result is True
            
            # Check if output file exists
            output_path = output_dir / "test_input.png"
            assert output_path.exists()
              # Check if the output image has the correct dimensions
            with Image.open(output_path) as output_img:
                original_width, original_height = 100, 140
                expected_width = original_width + 2 * 4  # 4 pixels on each side
                expected_height = original_height + 2 * 4  # 4 pixels on each side
                
                assert output_img.size == (expected_width, expected_height)
                
                # Verify that edge pixels were extended by checking bleed areas
                # Left bleed area should have yellow color (from left edge)
                left_bleed_color = output_img.getpixel((2, 50))  # Middle of left bleed
                assert left_bleed_color == (255, 255, 0)  # Yellow
                
                # Right bleed area should have magenta color (from right edge)
                right_bleed_color = output_img.getpixel((105, 50))  # Middle of right bleed
                assert right_bleed_color == (255, 0, 255)  # Magenta
                
                # Top bleed area should have blue color (from top edge)
                top_bleed_color = output_img.getpixel((50, 2))  # Middle of top bleed
                assert top_bleed_color == (0, 0, 255)  # Blue


if __name__ == "__main__":
    pytest.main([__file__])
