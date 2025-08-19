import os
import zipfile
import time
from pdf2image import convert_from_path

def convert_pdf_to_images(input_path, output_dir, img_format="jpg", timestr=""):
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    if img_format == "jpg":
        pdf2image_fmt = "jpeg"
        pil_format = "JPEG"
        ext = "jpg"
    elif img_format == "png":
        pdf2image_fmt = "png"
        pil_format = "PNG"
        ext = "png"
    else:
        raise ValueError("지원하지 않는 이미지 포맷입니다. (jpg, png만 가능)")

    images = convert_from_path(input_path, fmt=pdf2image_fmt)

    image_files = []
    now = time.time()  # 현재 시간 미리 저장
    for i, image in enumerate(images):
        img_filename = f"{base_name}_page{i+1}_{timestr}.{ext}" if timestr else f"{base_name}_page{i+1}.{ext}"
        output_img = os.path.join(output_dir, img_filename)
        image.save(output_img, pil_format)

        # ✅ 수정일 현재 시간으로 설정
        os.utime(output_img, (now, now))

        image_files.append(output_img)

    # ZIP 파일명도 시분초 추가
    zip_filename = f"{base_name}_images_{timestr}.zip" if timestr else f"{base_name}_images.zip"
    zip_path = os.path.join(output_dir, zip_filename)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for img_file in image_files:
            arcname = os.path.basename(img_file)
            zipf.write(img_file, arcname=arcname)

    # 임시 파일 삭제
    for img_file in image_files:
        os.remove(img_file)

    return zip_path, zip_filename