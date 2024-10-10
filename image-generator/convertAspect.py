import cv2
import numpy as np
import os
from multiprocessing import Pool, cpu_count
from PIL import Image, ImageOps

# def make_square(args):
#     # Load the image
#     input_image_path, base_input_dir, base_output_dir = args
#     relative_path = os.path.relpath(input_image_path, base_input_dir)
#     output_image_path = os.path.join(base_output_dir, relative_path)
#     image = cv2.imread(input_image_path)

#     # Get the current dimensions of the image
#     height, width, channels = image.shape

#     # If the image is already square, no need to add bars
#     if height == width:
#         cv2.imwrite(output_path, image)
#         return

#     # Calculate the amount of padding needed to make the image square
#     if height > width:
#         # Add padding to the width (left and right)
#         padding = (height - width) // 2
#         new_image = cv2.copyMakeBorder(image, 0, 0, padding, padding, cv2.BORDER_CONSTANT, value=(0, 0, 0))
#     else:
#         # Add padding to the height (top and bottom)
#         padding = (width - height) // 2
#         new_image = cv2.copyMakeBorder(image, padding, padding, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))

#     # Save the new image
#     cv2.imwrite(output_image_path, new_image)
#     print(f"Image saved successfully as {output_image_path}")

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def make_square(args, color=(0, 0, 0)):
    # Open the image
    input_image_path, base_input_dir, base_output_dir = args
    relative_path = os.path.relpath(input_image_path, base_input_dir)
    output_image_path = os.path.join(base_output_dir, relative_path)
    ensure_dir(os.path.dirname(output_image_path))

    image = Image.open(input_image_path)

    # Get the dimensions of the image
    width, height = image.size

    # Check if the image is already square
    if width == height:
        image.save(output_image_path, format='WEBP')
        return

    # Determine the size for the square image
    new_size = max(width, height)

    # Create a new square image with the specified background color
    new_image = ImageOps.expand(image, border=(0, (new_size - height) // 2, 0, (new_size - height + 1) // 2), fill=color)

    # Save the image in the desired output path in .webp format
    new_image.save(output_image_path, format='WEBP')
    print(f"Image saved successfully as {output_image_path}")

def process_images_with_structure(input_dir, output_dir):
    image_paths = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.webp')):
                full_path = os.path.join(root, file)
                image_paths.append((full_path, input_dir, output_dir))
    
    with Pool(6) as p:
        p.map(make_square, image_paths)

input_dir = 'Tides/web3'
output_dir = 'Tides/squared'
process_images_with_structure(input_dir, output_dir)
