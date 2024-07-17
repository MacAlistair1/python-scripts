import json
import svgwrite
from svgwrite import cm, mm

# Load JSON data
file_path = "/Users/nepalivlog/Documents/scripts/stat.json"
with open(file_path, 'r') as f:
    data = json.load(f)

# Initialize SVG drawing
dwg = svgwrite.Drawing('contribution_chart.svg', profile='tiny')

# Define the size of each cell
cell_size = 20
cell_padding = 5

# Define colors for different levels
colors = {
    0: "#ebedf0",  # no contributions
    1: "#c6e48b",  # low contributions
    2: "#7bc96f",  # medium contributions
    3: "#239a3b",  # high contributions
    4: "#196127"   # very high contributions
}

# Add rectangles for each data point
for item in data:
    x = item['x'] * (cell_size + cell_padding)
    y = item['y'] * (cell_size + cell_padding)
    level = item['level']
    color = colors.get(level, "#ebedf0")
    
    dwg.add(dwg.rect(insert=(x, y), size=(cell_size, cell_size), fill=color))

# Save the SVG file
dwg.save()
