# services/image_compress_service.py

from PIL import Image
import os
import pillow_heif
pillow_heif.register_heif_opener()

OUTPUT_FOLDER = "outputs"

def compress_image(input_path, output_path, quality=70):
    with Image.open(input_path) as img:
        # JPEG은 quality로 압축, PNG는 optimize 사용
        ext = os.path.splitext(output_path)[-1].lower()
        if ext in [".jpg", ".jpeg"]:
            img = img.convert("RGB")  # JPEG 저장을 위해 RGB 변환
            img.save(output_path, "JPEG", quality=quality, optimize=True)
        elif ext == ".png":
            img.save(output_path, "PNG", optimize=True, compress_level=9)
        else:
            img.save(output_path)  # 기타 포맷은 그대로 저장
    return output_path