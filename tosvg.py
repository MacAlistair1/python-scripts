from PIL import Image
import matplotlib.pyplot as plt
import cairosvg
import numpy as np
import cv2
import io

# Load the image
image_path = "/Users/nepalivlog/Downloads/Project NG/raddish/raw.png"
image = Image.open(image_path)

# Display the image
# plt.imshow(image)
# plt.axis('off')  # Turn off axis numbers and ticks
# plt.show()


# Convert the PIL image to a NumPy array
image_np = np.array(image)

# Convert to grayscale
gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

# Apply thresholding to convert the image to binary
_, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create an SVG file with the contours
svg_output = io.StringIO()
svg_output.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
svg_output.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n')

for contour in contours:
    svg_output.write('<path d="M ')
    for point in contour:
        x, y = point[0]
        svg_output.write(f'{x},{y} ')
    svg_output.write('z" fill="none" stroke="black" stroke-width="1"/>\n')

svg_output.write('</svg>\n')

# Get the SVG string
svg_data = svg_output.getvalue()
svg_output.close()

# Save the SVG file
svg_path = "/Users/nepalivlog/Downloads/Project NG/raddish/radish1.svg"
with open(svg_path, "w") as file:
    file.write(svg_data)