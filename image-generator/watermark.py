from PIL import Image
import os


def add_image_on_top(base_image_path, top_image_path, output_path, position):
    try:
        # Open the base image and ensure it is in RGBA mode
        base_image = Image.open(base_image_path).convert("RGBA")
        
        # Open the top image and ensure it is in RGBA mode
        top_image = Image.open(top_image_path).convert("RGBA")
        
        # Create a new image with the same size as the base image, also in RGBA mode
        result = Image.new('RGBA', base_image.size)
        
        # Paste the base image onto the result
        result.paste(base_image, (0, 0))
        
        # Use the alpha channel of the top image as the mask for pasting
        mask = top_image.split()[3]  # The alpha channel is the 4th channel in RGBA images
        
        # Paste the top image onto the result at the specified position, using its alpha channel as the mask
        result.paste(top_image, position, mask)
        
        # Save the result
        result.save(output_path)
        print(f"Image saved successfully as {output_path}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def convert_jpeg_to_png(jpeg_path, png_path):
    try:
        image = Image.open(jpeg_path)
        image.save(png_path, "PNG")
        print(f"Converted {jpeg_path} to {png_path}")
    except Exception as e:
        print(f"Error converting {jpeg_path} to PNG: {str(e)}")


# Example usage
base_images_dir = 'Tides/og_high'
# Ensure top_image_path and position are defined as before

# List all files in the base_images_dir
files = os.listdir(base_images_dir)

# Filter out files to only include images (e.g., .png, .jpg)
jpgs = [file for file in files if file.lower().endswith(('.jpg', '.jpeg'))]

top_image_path = 'Tides/logo.jpg'
# output_path = 'path/to/output_image.png'
position = (50, 50)  # X, Y coordinates where the top image will be placed

# for image_file in jpgs:
#     base_image_path = os.path.join(base_images_dir, image_file)
#     output_image_path = os.path.join(base_images_dir, image_file)  # Modify output path as needed
#     if image_file.lower().endswith('.jpg') or image_file.lower().endswith('.jpeg'):
#         png_image_path = os.path.splitext(output_image_path)[0] + '.png'
#         convert_jpeg_to_png(base_image_path, png_image_path)
#         base_image_path = png_image_path  # Update base_image_path to the new PNG file
files = os.listdir(base_images_dir)

pngs = [file for file in files if file.lower().endswith(('.png'))]

for image_file in pngs:
    base_image_path = os.path.join(base_images_dir, image_file)
    output_image_path = os.path.join('Tides/watermarked', image_file)

    add_image_on_top(base_image_path, top_image_path, output_image_path, position)

print("Processing completed.")