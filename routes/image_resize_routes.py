from flask import Blueprint, request, jsonify, send_from_directory
from services.image_resize_service import resize_image
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
import os
from datetime import datetime
from werkzeug.utils import secure_filename

image_resize_bp = Blueprint("image_resize", __name__)

@image_resize_bp.route("/convert/image-resize", methods=["POST"])
def image_resize():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]
    width = int(request.form.get("width", 0))
    height = int(request.form.get("height", 0))
    keep_ratio = request.form.get("keepRatio", "true").lower() == "true"

    if not file or width <= 0 or height <= 0:
        return jsonify({"success": False, "error": "Invalid params"}), 400

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    name, ext = os.path.splitext(file.filename)
    name = secure_filename(name)
    timestr = datetime.now().strftime("%H%M%S")

    input_filename = f"{name}_{timestr}{ext}"
    input_path = os.path.join("uploads", input_filename)
    output_filename = f"{name}_{width}x{height}_{timestr}{ext}"
    output_path = os.path.join("outputs", output_filename)

    file.save(input_path)
    resize_image(input_path, output_path, width, height, keep_ratio)

    # ✅ 업로드된 원본 이미지 삭제
    delete_file_now(input_path)

    # ✅ 리사이즈된 이미지 1분 뒤 삭제
    delete_file_after_delay(output_path, delay=60)

    return jsonify({"success": True, "filename": output_filename})

@image_resize_bp.route("/download/<filename>", methods=["GET"])
def download_resized(filename):
    return send_from_directory("outputs", filename, as_attachment=True)