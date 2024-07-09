'''How it works:
a - processing options
b - open image
c - resize image

1 - Color reduction using preferred method
2 - Space out pixels
3 - Convert pixels to DMC values
4 - Generate SVG pattern
5 - Clean up the image
6 - Produce SVGs that are black and white without symbols, in color with symbols, or in color without symbols
7 - Generate the key table to link color to floss ID
'''

import sys
from PIL import Image
from color_matching import DMC_Matching
import numpy as np
from svg import SVG
from sklearn.cluster import KMeans, MeanShift, estimate_bandwidth
from sklearn.mixture import GaussianMixture
from tqdm import tqdm

def get_neighbors(position, matrix):
    '''
    Find pixel of interest's neighborhood and pull their values to help with cleaning up the final pattern
    :Param position: Pixel of interest
    :Param matrix: neighborhood you want to interrogate
    Returns a matrix of neighboring values
    '''
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    width = 1
    for i in range(max(0, position[0] - width), min(rows, position[0] + width + 1)):
        for j in range(max(0, position[1] - width), min(cols, position[1] + width + 1)):
            if not (i == position[0] and j == position[1]):
                yield matrix[i][j]

def resize(image, max_size):
    '''
    Resize the input image to match a maximum dimension while maintaining the aspect ratio.
    :Param image: input image to be resized, opened using the load_data function
    :Param max_size: (width, height) maximum desired dimensions
    :Return the resized image
    '''
    image.thumbnail(max_size, Image.LANCZOS)
    return image

def load_data(file_path):
    image = Image.open(file_path)
    return image

def resize(image, new_width):
    '''
    Resize the input image to match a maximum dimension while maintaining the aspect ratio.
    :Param image: input image to be resized, opened using the load_data function
    :Param new_width: (width, height) maximum desired dimensions
    :Return the resized image
    '''
    new_height = int(new_width * image.size[1] / image.size[0])
    resized_image = image.resize((new_width, new_height), Image.NEAREST)
    return resized_image

def kmeans_reduction(image, num_colors):
    '''
    Use KMeans to reduce the number of unique colors in an image represented by an array
    :Param image: Resized image you want to have reduce the number of colors for
    :Param num_colors: Desired number of unique colors
    Return Labels for each pixel and the palette of the identified colors
    '''    
    kmeans = KMeans(n_clusters=num_colors, random_state=18, n_init=15).fit(image)
    labels = kmeans.labels_
    palette = kmeans.cluster_centers_[:, :3]
    return labels, palette

def meanshift_reduction(image_array, num_colors):
    """
    Reduce the number of colors using Mean Shift clustering.
    :Param image_array: Flattened array representation of the image
    :Param num_colors: Number of unique colors to reduce to
    :Return: Labels for each pixel and the palette of reduced colors
    """
    bandwidth = estimate_bandwidth(image_array, quantile=0.2, n_samples=500)
    meanshift = MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(image_array)
    labels = meanshift.labels_
    palette = meanshift.cluster_centers_[:, :3]
    return labels, palette

def gmm_reduction(image_array, num_colors):
    """
    Reduce the number of colors using Gaussian Mixture Model (GMM) clustering.
    :Param image_array: Flattened array representation of the image
    :Param num_colors: Number of unique colors to reduce to
    :Return: Labels for each pixel and the palette of reduced colors
    """
    gmm = GaussianMixture(n_components=num_colors, random_state=18).fit(image_array)
    labels = gmm.predict(image_array)
    palette = gmm.means_[:, :3]
    return labels, palette

def color_reduction(image, method, num_colors):
    '''
    Reduce the number of colors using K-means clustering.
    :Param image: input image for color manipulation, pre-processed using the resize function
    :Param num_colors: How many unique colors you want to work with
    :Return an image composed of only the specified number of colors
    '''
    image = image.convert("RGB")
    image_array = np.array(image)
    height, width, channels = image_array.shape
    image_array = image_array.reshape(-1, channels)

    if method == 'kmeans':
        labels, palette = kmeans_reduction(image_array, num_colors)
    elif method == 'meanshift':
        labels, palette = meanshift_reduction(image_array, num_colors)
    elif method == 'gmm':
        labels, palette = gmm_reduction(image_array, num_colors)
    else:
        raise ValueError("Unsupported method. Please chose from 'kmeans', 'meanshift', or 'gmm'.")

    mapped_colors = palette[labels].reshape(height, width, channels).astype('uint8')
    return Image.fromarray(mapped_colors), labels.reshape(height, width), palette

# a - Processing options

if(len(sys.argv)<4):
    print("Function requires an input filename, number of colours, color reduction method, and stitch count. No quotes necessary.")
    sys.exit(0)

input_file_name = sys.argv[1]               # Input file name
num_colors = int(sys.argv[2])               # Number of colors to use in the pattern
color_reduction_method = sys.argv[3]        # Color reduction methodology
count = int(sys.argv[4])                    # Number of stitches on the x axis

col_sym = SVG(False, True, True)
blw_nsy = SVG(True, True, True)
col_nsy = SVG(False, False, False)
key = SVG(False, True, True)

# b - Open image

image = load_data(input_file_name)

# c - Resize image

new_width = count
pixel_size = int(new_width/count)
image = resize(image, new_width)
print("Image size is: ", image.size)

# Step 1 - Color reduction using preferred method
color_adjusted_image, labels, palette = color_reduction(image, color_reduction_method, num_colors)

# Step 2 - Space out pixels
# Step 3 - Convert pixels to DMC values

d = DMC_Matching()
svg_palette = [d.get_color_code(tuple(palette[i])) for i in range(num_colors)]

# Step 4 - Generate SVG pattern
x_count = color_adjusted_image.size[0]
y_count = color_adjusted_image.size[1]
svg_pattern = labels.tolist()

# Step 5 - Clean up the image
if True:
    for x in range(x_count):
        for y in range(y_count):
            gen = get_neighbors([y, x], svg_pattern)
            neighbors = []
            for n in gen:
                neighbors.append(n)
            if svg_pattern[y][x] not in neighbors:
                mode = max(neighbors, key = neighbors.count)
                svg_pattern[y][x] = mode

# Step 6 - Produce SVGs that are black and white, in color with symbols, or in color without symbols

svg_cell_size = 10
width = x_count * svg_cell_size
height = y_count * svg_cell_size

# col_sym.prep_for_drawing(width, height)
# col_sym.mid_arrows(svg_cell_size, width, height)
# blw_nsy.prep_for_drawing(width, height)
# blw_nsy.mid_arrows(svg_cell_size, width, height)
col_nsy.prep_for_drawing(width, height)
print("All is prepped.\n")

x = y = svg_cell_size       # To allow for the drawing of midpoint arrows
row_count = 0
for row in svg_pattern:
    col_count = 0
    for color_index in row:
        print(f"Processing row {row_count}, column {col_count} with color index {color_index}")
        # col_sym.add_rect(svg_palette, color_index, x, y, svg_cell_size)
        # blw_nsy.add_rect(svg_palette, color_index, x, y, svg_cell_size)
        col_nsy.add_rect(svg_palette, color_index, x, y, svg_cell_size)
        x += svg_cell_size
        col_count += 1
    y += svg_cell_size
    x = svg_cell_size
    row_count += 1

# blw_nsy.major_gridlines(svg_cell_size, width, height)
# col_sym.major_gridlines(svg_cell_size, width, height)
col_nsy.major_gridlines(svg_cell_size, width, height)

# Step 7 - Generate the key table to link color to floss ID
print("Starting step 9!\n")
size = 40
key.prep_for_drawing(size * 13, size * len(svg_palette))
x = y = 0
for i in range(len(svg_palette)):
    key.add_key_color(x, y, size, i, svg_palette[i])
    y += size

# Save the SVG files:) 
# col_sym.save('results/color_with_symbol.svg')
# blw_nsy.save('results/black_white_nosymbol.svg')
svg_pattern_name = 'results/pattern.svg'
svg_key_name = 'results/key.svg'

col_nsy.save(svg_pattern_name)
key.save(svg_key_name)
print("Everything should be saved!!!")

