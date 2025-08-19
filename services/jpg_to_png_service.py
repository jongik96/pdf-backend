from PIL import Image
import os

def jpg_to_png(input_path, output_path):
    with Image.open(input_path) as img:
        # PNG로 변환하여 저장
        img.convert("RGBA").save(output_path, "PNG")
    return output_path