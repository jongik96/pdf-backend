import os
from PIL import Image, ImageOps
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

def _flatten_to_rgb(img: Image.Image, bg=(255, 255, 255)) -> Image.Image:
    """
    투명/팔레트/그레이스케일 이미지를 PDF 안전한 RGB로 평면화.
    - EXIF 회전 반영
    - Alpha 제거 (SMask 방지)
    - P(팔레트) → RGB
    - L/LA(그레이스케일) → RGB
    """
    # EXIF 회전 보정
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    # 팔레트(투명 포함 가능) → RGBA로 우선 변환
    if img.mode == "P":
        img = img.convert("RGBA")

    # Alpha가 있는 경우 흰 배경으로 합성해 완전한 RGB로 평면화
    if img.mode in ("RGBA", "LA"):
        base = Image.new("RGB", img.size, bg)
        if img.mode == "LA":
            # L + alpha → RGB로 승격 후 합성
            rgb = img.convert("RGBA")
            base.paste(rgb, mask=rgb.split()[-1])
        else:
            base.paste(img, mask=img.split()[-1])
        img = base
    elif img.mode != "RGB":
        # L/CMYK 등은 RGB로 강제 변환
        img = img.convert("RGB")

    # 모바일에서 썸네일/ICC로 인한 이중표시 방지: 메타 제거
    img.info.pop("icc_profile", None)
    img.info.pop("exif", None)

    return img

def convert_images_to_pdf(files):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    image_paths = []
    images = []

    first_filename = files[0].filename if files else "images"
    name, _ = os.path.splitext(secure_filename(first_filename))
    timestr = datetime.now().strftime("%H%M%S")
    base_filename = f"{name}_{timestr}"

    # 파일 저장 및 이미지 읽기/정규화
    for file in files:
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]
        saved_filename = f"{os.path.splitext(filename)[0]}_{timestr}{ext}"
        saved_path = os.path.join(UPLOAD_DIR, saved_filename)

        file.save(saved_path)
        image_paths.append(saved_path)

        try:
            with Image.open(saved_path) as im:
                safe_im = _flatten_to_rgb(im)
                # PDF 저장 시 참조 가능한 독립 이미지로 복사
                images.append(safe_im.copy())
        except Exception:
            continue

    if not images:
        raise Exception("No valid images to convert.")

    pdf_path = os.path.join(OUTPUT_DIR, f"{base_filename}.pdf")

    # PIL의 PDF 저장: 첫 장 + 나머지 추가
    # resolution을 적당히 주면 일부 뷰어에서의 스케일 이슈도 줄어듭니다.
    images[0].save(
        pdf_path,
        "PDF",
        save_all=True,
        append_images=images[1:] if len(images) > 1 else [],
        resolution=300,
    )

    # 리소스 정리
    for im in images:
        try:
            im.close()
        except Exception:
            pass

    return image_paths, pdf_path, os.path.basename(pdf_path)