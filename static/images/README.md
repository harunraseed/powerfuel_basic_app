# PowerFuel Logo Files

Please save your logo images here:

1. **logo_white_bg.png** - Logo with white background (for login page)
2. **logo_transparent.png** - Logo with transparent background (for PDF and other pages)
3. **logo_black_bg.png** - Logo with black background (optional, for dark themes)

## How to Save:
1. Download the logo images from the attachments
2. Save them in this folder: `d:\Harun\Projects\powerfuel_final\static\images\`
3. Ensure filenames match exactly as listed above

## Usage:
- **Web pages**: Uses Flask's `url_for('static', filename='images/logo_white_bg.png')`
- **PDF reports**: Uses `logo_transparent.png` at the top of each report
- All logos are automatically sized and centered
