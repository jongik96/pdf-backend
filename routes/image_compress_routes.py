from flask import Blueprint, request, jsonify, send_from_directory
from services.image_compress_service import compress_image
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
import os
from datetime import datetime

image_compress_bp = Blueprint("image_compress", __name__)

@image_compress_bp.route("/convert/image-compress", methods=["POST"])
def image_compress():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]
    quality = int(request.form.get("quality", 70))

    if not file:
        return jsonify({"success": False, "error": "Invalid params"}), 400

    base, ext = os.path.splitext(file.filename)
    timestr = datetime.now().strftime("%H%M%S")
    input_filename = f"{base}_{timestr}{ext}"
    output_filename = f"{base}_{timestr}_compressed{ext}"

    input_path = os.path.join("uploads", input_filename)
    output_path = os.path.join("outputs", output_filename)

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    file.save(input_path)
    compress_image(input_path, output_path, quality)

    # ✅ 업로드된 원본 이미지 삭제
    delete_file_now(input_path)

    # ✅ 압축된 이미지 1분 뒤 삭제
    delete_file_after_delay(output_path, delay=60)

    return jsonify({"success": True, "filename": output_filename})

@image_compress_bp.route("/download/<filename>", methods=["GET"])
def download_compressed(filename):
    return send_from_directory("outputs", filename, as_attachment=True)