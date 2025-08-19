from PIL import Image

def png_to_webp(input_path, output_path):
    with Image.open(input_path) as img:
        img.save(output_path, "WEBP")