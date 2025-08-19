from PIL import Image
import os
import pillow_heif
pillow_heif.register_heif_opener()

OUTPUT_FOLDER = "outputs"

def resize_image(input_path, output_path, width, height, keep_ratio=True):
    with Image.open(input_path) as img:
        if keep_ratio:
            img.thumbnail((width, height), Image.LANCZOS)
        else:
            img = img.resize((width, height), Image.LANCZOS)
        img.save(output_path)
    return output_path