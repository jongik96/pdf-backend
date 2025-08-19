from flask import Blueprint, request, jsonify
import os
from services.pdf_to_image_service import convert_pdf_to_images
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
from datetime import datetime
from werkzeug.utils import secure_filename

pdf_to_image_bp = Blueprint("pdf_to_image", __name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@pdf_to_image_bp.route("/convert/pdf-to-image", methods=["POST"])
def handle_pdf_to_image():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Empty filename"}), 400

    img_format = request.form.get("format", "jpg").lower()
    if img_format not in ["jpg", "png"]:
        return jsonify({"success": False, "error": "지원하지 않는 포맷입니다. (jpg, png만 가능)"}), 400

    timestr = datetime.now().strftime("%H%M%S")
    base, ext = os.path.splitext(secure_filename(file.filename))
    input_filename = f"{base}_{timestr}{ext}"
    input_path = os.path.join(UPLOAD_FOLDER, input_filename)

    file.save(input_path)

    try:
        zip_path, zip_filename = convert_pdf_to_images(input_path, OUTPUT_FOLDER, img_format, timestr)

        # ✅ 삭제 처리
        delete_file_now(input_path)              # 업로드된 PDF는 즉시 삭제
        delete_file_after_delay(zip_path, 60)    # 변환된 이미지 ZIP은 1분 후 삭제

        return jsonify({
            "success": True,
            "message": "변환에 성공했습니다.",
            "filename": zip_filename
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500