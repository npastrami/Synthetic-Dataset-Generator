from PIL import ImageDraw, ImageFont
from io import BytesIO
import os
import random
from pdf2image import convert_from_bytes

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

def create_and_modify_copy(pdf_bytes, copy_index, bounding_boxes, generate_text_for_keyword, fonts_folder_path, blob_container_client, blob_name):
    # Convert PDF to image
    images = convert_from_bytes(pdf_bytes, dpi=300, first_page=1, last_page=1)
    img = images[0].convert('RGB')

    # Draw text on image
    draw_text_on_image(img, bounding_boxes, generate_text_for_keyword, fonts_folder_path)

    # Save the modified image to a buffer
    image_buffer = BytesIO()
    img.save(image_buffer, format='JPEG')
    image_buffer.seek(0)

    # Create a new blob client for the modified copy
    destination_jpeg_name = f"{blob_name.split('.')[0]}_copy_{copy_index}.jpeg"
    new_blob_client = blob_container_client.get_blob_client(destination_jpeg_name)

    # Upload the modified copy
    new_blob_client.upload_blob(image_buffer.read(), overwrite=True)
