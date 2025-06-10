#!/usr/bin/env python3
"""
MPC Print Bleed Border Tool
Adds appropriate bleed borders to images for MPC (Make Playing Cards) printing
by extending edge pixels outward instead of adding solid borders.

Bleed calculations (corrected):
- Width: 4.84% (0.12" on each side for 2.48" safe area)
- Height: 3.47% (0.12" on each side for 3.46" safe area)
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageOps
import threading
import time
from typing import List, Tuple, Optional

class TerminalColors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'

class LoadingSpinner:
    """A simple loading spinner for terminal"""
    
    def __init__(self, message: str = "Processing"):
        self.message = message
        self.is_running = False
        self.thread = None
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        
    def _spin(self):
        """Run the spinner animation"""
        idx = 0
        while self.is_running:
            sys.stdout.write(f'\r{TerminalColors.CYAN}{self.spinner_chars[idx]} {self.message}...{TerminalColors.RESET}')
            sys.stdout.flush()
            idx = (idx + 1) % len(self.spinner_chars)
            time.sleep(0.1)
    
    def start(self):
        """Start the spinner"""
        self.is_running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self, success_message: Optional[str] = None):
        """Stop the spinner"""
        self.is_running = False
        if self.thread:
            self.thread.join()
        
        # Clear the spinner line
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        
        if success_message:
            print(f'{TerminalColors.GREEN}✓ {success_message}{TerminalColors.RESET}')

def print_banner():
    """Print a nice banner for the application"""
    banner = f"""
{TerminalColors.MAGENTA}{'='*60}
{TerminalColors.BOLD}    MPC Print Bleed Border Tool    
{'='*60}{TerminalColors.RESET}

{TerminalColors.CYAN}Adds bleed borders by extending edge pixels for MPC printing:{TerminalColors.RESET}
• Width bleed:  4.84% (0.12" on each side for 2.48" safe area)
• Height bleed: 3.47% (0.12" on each side for 3.46" safe area)
"""
    print(banner)

def get_folder_path(prompt: str, must_exist: bool = True) -> Path:
    """Get and validate a folder path from user input"""
    while True:
        print(f"\n{TerminalColors.YELLOW}{prompt}{TerminalColors.RESET}")
        path_str = input("Path: ").strip().strip('"\'')
        
        if not path_str:
            print(f"{TerminalColors.RED}Please enter a valid path.{TerminalColors.RESET}")
            continue
            
        path = Path(path_str)
        
        if must_exist and not path.exists():
            print(f"{TerminalColors.RED}Path does not exist: {path}{TerminalColors.RESET}")
            continue
            
        if must_exist and not path.is_dir():
            print(f"{TerminalColors.RED}Path is not a directory: {path}{TerminalColors.RESET}")
            continue
            
        return path

def find_image_files(input_folder: Path) -> List[Path]:
    """Find all image files in the input folder"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
    image_files = []
    
    spinner = LoadingSpinner("Scanning for images")
    spinner.start()
    
    try:
        for file_path in input_folder.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                image_files.append(file_path)
    finally:
        spinner.stop(f"Found {len(image_files)} image(s)")
    
    return image_files

def calculate_bleed_pixels(width: int, height: int) -> Tuple[int, int, int, int]:
    """
    Calculate bleed pixels for each side based on MPC requirements.
    
    MPC Requirements:
    - Safe area: 2.48" × 3.46"
    - Total with bleed: 2.72" × 3.70"
    - Bleed area: 0.12" on each side
    
    Returns: (top, bottom, left, right) pixels to add
    """
    # Calculate bleed as percentage of safe area dimensions
    # Horizontal bleed: 0.12" on each side = 0.12/2.48 = 4.84% of width
    # Vertical bleed: 0.12" on each side = 0.12/3.46 = 3.47% of height
    WIDTH_BLEED_PERCENT = 4.84   # 0.12" / 2.48" = 4.84%
    HEIGHT_BLEED_PERCENT = 3.47  # 0.12" / 3.46" = 3.47%
    
    # Calculate bleed pixels for each side
    horizontal_bleed_per_side = int((width * WIDTH_BLEED_PERCENT) / 100)
    vertical_bleed_per_side = int((height * HEIGHT_BLEED_PERCENT) / 100)
    
    # Return as (top, bottom, left, right)
    return vertical_bleed_per_side, vertical_bleed_per_side, horizontal_bleed_per_side, horizontal_bleed_per_side

def add_bleed_border(image_path: Path, output_folder: Path) -> bool:
    """
    Add bleed border to a single image by extending edge pixels outward.
    
    Returns: True if successful, False otherwise
    """
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (for PNG with transparency, etc.)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            width, height = img.size
            
            # Calculate bleed pixels
            top, bottom, left, right = calculate_bleed_pixels(width, height)
            
            # Create new image with extended dimensions
            new_width = width + left + right
            new_height = height + top + bottom
            extended_img = Image.new('RGB', (new_width, new_height))
            
            # Paste the original image in the center
            extended_img.paste(img, (left, top))
            
            # Extend edge pixels outward
            # Top edge
            if top > 0:
                top_edge = img.crop((0, 0, width, 1))
                for y in range(top):
                    extended_img.paste(top_edge, (left, y))
            
            # Bottom edge
            if bottom > 0:
                bottom_edge = img.crop((0, height - 1, width, height))
                for y in range(top + height, new_height):
                    extended_img.paste(bottom_edge, (left, y))
            
            # Left edge (including corners)
            if left > 0:
                left_edge = extended_img.crop((left, 0, left + 1, new_height))
                for x in range(left):
                    extended_img.paste(left_edge, (x, 0))
            
            # Right edge (including corners)
            if right > 0:
                right_edge = extended_img.crop((left + width - 1, 0, left + width, new_height))
                for x in range(left + width, new_width):
                    extended_img.paste(right_edge, (x, 0))
            
            # Create output path
            output_path = output_folder / image_path.name
            
            # Save the image
            extended_img.save(output_path, quality=95, optimize=True)
            
            return True
            
    except Exception as e:
        print(f"\n{TerminalColors.RED}Error processing {image_path.name}: {e}{TerminalColors.RESET}")
        return False

def process_images(image_files: List[Path], output_folder: Path):
    """Process all image files with progress tracking"""
    total_files = len(image_files)
    processed = 0
    failed = 0
    
    print(f"\n{TerminalColors.BOLD}Processing {total_files} image(s)...{TerminalColors.RESET}\n")
    
    for i, image_path in enumerate(image_files, 1):
        # Show progress
        progress = (i / total_files) * 100
        bar_length = 30
        filled_length = int(bar_length * i // total_files)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        print(f'\r{TerminalColors.BLUE}[{bar}] {progress:.1f}% - Processing: {image_path.name[:30]}...{TerminalColors.RESET}', end='', flush=True)
        
        # Process the image
        if add_bleed_border(image_path, output_folder):
            processed += 1
        else:
            failed += 1
    
    # Clear progress line and show summary
    print('\r' + ' ' * 80 + '\r', end='')
    
    print(f"\n{TerminalColors.BOLD}Processing Complete!{TerminalColors.RESET}")
    print(f"{TerminalColors.GREEN}✓ Successfully processed: {processed} images{TerminalColors.RESET}")
    
    if failed > 0:
        print(f"{TerminalColors.RED}✗ Failed to process: {failed} images{TerminalColors.RESET}")

def main():
    """Main application function"""
    try:
        # Print banner
        print_banner()
        
        # Get input folder
        input_folder = get_folder_path("Enter the input folder path (containing images):", must_exist=True)
        
        # Get output folder
        output_folder = get_folder_path("Enter the output folder path (where bordered images will be saved):", must_exist=False)
        
        # Create output folder if it doesn't exist
        if not output_folder.exists():
            spinner = LoadingSpinner("Creating output folder")
            spinner.start()
            try:
                output_folder.mkdir(parents=True, exist_ok=True)
                spinner.stop("Output folder created")
            except Exception as e:
                spinner.stop()
                print(f"{TerminalColors.RED}Error creating output folder: {e}{TerminalColors.RESET}")
                return
        
        # Find image files
        image_files = find_image_files(input_folder)
        
        if not image_files:
            print(f"\n{TerminalColors.YELLOW}No image files found in the input folder.{TerminalColors.RESET}")
            return
        
        # Show summary
        print(f"\n{TerminalColors.BOLD}Summary:{TerminalColors.RESET}")
        print(f"Input folder:  {TerminalColors.CYAN}{input_folder}{TerminalColors.RESET}")
        print(f"Output folder: {TerminalColors.CYAN}{output_folder}{TerminalColors.RESET}")
        print(f"Images found:  {TerminalColors.GREEN}{len(image_files)}{TerminalColors.RESET}")
        
        # Confirm before processing
        print(f"\n{TerminalColors.YELLOW}Press Enter to continue or Ctrl+C to cancel...{TerminalColors.RESET}")
        input()
        
        # Process images
        process_images(image_files, output_folder)
        
        print(f"\n{TerminalColors.GREEN}{TerminalColors.BOLD}All done! 🎉{TerminalColors.RESET}")
        print(f"Check your output folder: {TerminalColors.CYAN}{output_folder}{TerminalColors.RESET}")
        
    except KeyboardInterrupt:
        print(f"\n\n{TerminalColors.YELLOW}Operation cancelled by user.{TerminalColors.RESET}")
    except Exception as e:
        print(f"\n{TerminalColors.RED}An unexpected error occurred: {e}{TerminalColors.RESET}")

if __name__ == "__main__":
    main()
