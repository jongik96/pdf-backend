from flask import Blueprint, request, jsonify, send_from_directory
from services.heic_to_jpg_service import heic_to_jpg
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
import os
from datetime import datetime

heic_to_jpg_bp = Blueprint("heic_to_jpg", __name__)

@heic_to_jpg_bp.route("/convert/heic-to-jpg", methods=["POST"])
def convert_heic_to_jpg():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file or not file.filename.lower().endswith(".heic"):
        return jsonify({"success": False, "error": "HEIC 파일만 지원됩니다."}), 400

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    base = os.path.splitext(file.filename)[0]
    timestr = datetime.now().strftime("%H%M%S")
    input_filename = f"{base}_{timestr}.heic"
    output_filename = f"{base}_{timestr}.jpg"

    input_path = os.path.join("uploads", input_filename)
    output_path = os.path.join("outputs", output_filename)

    file.save(input_path)
    heic_to_jpg(input_path, output_path)

    # ✅ 업로드 파일 즉시 삭제
    delete_file_now(input_path)

    # ✅ 변환된 JPG 1분 후 삭제
    delete_file_after_delay(output_path, delay=60)

    return jsonify({"success": True, "filename": output_filename})

@heic_to_jpg_bp.route("/download/<filename>", methods=["GET"])
def download_heic_to_jpg(filename):
    return send_from_directory("outputs", filename, as_attachment=True)