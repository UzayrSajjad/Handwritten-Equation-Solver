from PIL import Image, ImageDraw, ImageFont
import os

# Create a simple logo image
img = Image.new('RGB', (100, 100), color='lightblue')
draw = ImageDraw.Draw(img)

# Draw a simple mathematical symbol
draw.text((25, 25), "∑=", fill='black', font_size=30)
draw.text((10, 55), "CNN", fill='darkblue', font_size=20)

# Save the logo
img.save('logo.png')
print("Logo created successfully!")
