# MPC Print Bleed Border Tool

A Python script that adds appropriate bleed borders to images for MPC (Make Playing Cards) printing.

## Features

- 🎨 Adds proper bleed borders by extending edge pixels (no black borders!)
- 🔄 Processes multiple images automatically
- 📊 Shows progress with loading spinners and progress bars
- ✨ Beautiful terminal interface with colors
- 🖼️ Supports multiple image formats (JPG, PNG, BMP, TIFF, WebP)
- 🌈 Extends the actual image content outward for natural-looking bleeds
- 📜 **Input history** - use ↑/↓ arrows to recall previous folder paths

## How It Works

The script automatically calculates bleed areas based on MPC's requirements and **extends the edge pixels** of your images outward to create natural-looking bleed areas instead of adding solid black borders.

**Corrected MPC Bleed Specifications:**
- **Width**: 4.84% bleed (0.12" on each side for 2.48" safe area)
- **Height**: 3.47% bleed (0.12" on each side for 3.46" safe area)

The edge extension method:
1. Takes the outermost pixels from each edge of your image
2. Extends them outward to fill the bleed area (0.12" on each side)
3. Creates a seamless transition that looks natural when trimmed

## Installation

### Option 1: Using pipenv (Recommended for Development)

1. Make sure you have Python 3.8+ installed
2. Install pipenv: `pip install pipenv`
3. Set up the development environment:

```powershell
pipenv install
```

4. Activate the environment:

```powershell
pipenv shell
```

### Option 2: Using pip

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### With pipenv:
```powershell
pipenv run python add_mpc_bleed.py
```

### With regular Python:
```bash
python add_mpc_bleed.py
```

### Steps:

1. Follow the prompts:
   - Enter the path to your input folder (containing the images)
   - Enter the path to your output folder (where bordered images will be saved)
   - **💡 Tip**: Use ↑/↓ arrow keys to navigate through previously entered paths

2. The script will:
   - Scan for images in the input folder
   - Show you a summary of what it found
   - Ask for confirmation before processing
   - Process all images with a progress bar
   - Save the bordered images to the output folder

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WebP (.webp)

## Example

```
$ python add_mpc_bleed.py

============================================================
    MPC Print Bleed Border Tool    
============================================================

Adds bleed borders to images for MPC printing:
• Width bleed:  9.7% (0.24" over 2.48" safe area)
• Height bleed: 6.9% (0.24" over 3.46" safe area)

Enter the input folder path (containing images):
Path: C:\Users\username\mtg_cards

Enter the output folder path (where bordered images will be saved):
Path: C:\Users\username\mtg_cards_with_bleed

⠋ Scanning for images...
✓ Found 15 image(s)

Summary:
Input folder:  C:\Users\username\mtg_cards
Output folder: C:\Users\username\mtg_cards_with_bleed
Images found:  15

Press Enter to continue or Ctrl+C to cancel...

Processing 15 image(s)...

[██████████████████████████████] 100.0% - Processing: card_015.jpg...

Processing Complete!
✓ Successfully processed: 15 images

All done! 🎉
Check your output folder: C:\Users\username\mtg_cards_with_bleed
```

## Notes

- The script preserves the original image quality
- **Edge pixels are extended** outward to create natural bleed areas (no black borders!)
- The output folder will be created automatically if it doesn't exist
- Original images are not modified - only copies with extended borders are created
- Works great with card images, artwork, and any graphics that need print bleeds
