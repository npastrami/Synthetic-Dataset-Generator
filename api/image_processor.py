from PIL import ImageDraw, ImageFont, Image
from io import BytesIO
import os
import random
from pdf2image import convert_from_bytes
import numpy as np

def add_noise_to_image(image):
    # 10% Chance of adding noise
    if random.random() < 0.90:
        return image
    
    # Convert PIL Image to numpy array
    np_image = np.array(image)

    # Generate Gaussian noise
    noise = np.random.normal(0, 0.75, np_image.shape).astype(np.uint8)

    # Add the noise to the image
    noisy_image = np_image + noise

    # Ensure the values are within the valid range
    noisy_image = np.clip(noisy_image, 0, 255)

    # Convert the noisy image back to PIL Image
    noisy_image_pil = Image.fromarray(noisy_image)
    
    print("printing noisy")

    return noisy_image_pil

def draw_text_on_image(img, bounding_boxes, generate_text_for_keyword, fonts_folder_path):
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size

    # Get a list of all .ttf files in the Fonts folder
    available_fonts = [f for f in os.listdir(fonts_folder_path) if f.endswith('.ttf')]

    for keyword, boxes in bounding_boxes.items():
        if not isinstance(boxes[0][0], list):  # Check if not a nested list
            boxes = [boxes]  # Make it a list of one item for uniform handling

        for box in boxes:
            text = generate_text_for_keyword(keyword)
            if text:
                # Randomly select a font and size
                random_font_name = random.choice(available_fonts)
                random_font_size = random.randint(25, 33)

                try:
                    font = ImageFont.truetype(f"{fonts_folder_path}/{random_font_name}", random_font_size)
                except IOError:
                    font = ImageFont.load_default()

                x, y = box[0]  # Top-left coordinates
                x += random.randint(-10, 10)  # Random displacement
                y += random.randint(-10, 10)

                if 0 <= x < img_width and 0 <= y < img_height:
                    draw.text((x, y), text, font=font, fill=(0, 0, 0))  # using black
                    #draw.text((x, y), text, font=font, fill=(255, 0, 0)) # using red
                    #draw.text((x, y), text, font=font, fill=(0, 0, 255)) # using blue

def create_and_modify_copy(pdf_bytes, copy_index, bounding_boxes, generate_text_for_keyword, fonts_folder_path, blob_container_client, blob_name):
    # Convert PDF to image
    images = convert_from_bytes(pdf_bytes, dpi=300, first_page=1, last_page=1)
    img = images[0].convert('RGB')

    # Draw text on image
    draw_text_on_image(img, bounding_boxes, generate_text_for_keyword, fonts_folder_path)
    
    img = add_noise_to_image(img)

    # Save the modified image to a buffer
    image_buffer = BytesIO()
    img.save(image_buffer, format='JPEG')
    image_buffer.seek(0)

    # Create a new blob client for the modified copy
    destination_jpeg_name = f"{blob_name.split('.')[0]}_copy_{copy_index}.jpeg"
    new_blob_client = blob_container_client.get_blob_client(destination_jpeg_name)

    # Upload the modified copy
    new_blob_client.upload_blob(image_buffer.read(), overwrite=True)
