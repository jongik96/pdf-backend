from flask import Blueprint, request, jsonify, send_from_directory
from services.png_to_webp_service import png_to_webp
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
import os
from datetime import datetime

png_to_webp_bp = Blueprint("png_to_webp", __name__)

@png_to_webp_bp.route("/convert/png-to-webp", methods=["POST"])
def convert_png_to_webp():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file or not file.filename.lower().endswith(".png"):
        return jsonify({"success": False, "error": "PNG 파일만 지원됩니다."}), 400

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    base, _ = os.path.splitext(file.filename)
    timestr = datetime.now().strftime("%H%M%S")
    input_filename = f"{base}_{timestr}.png"
    output_filename = f"{base}_{timestr}.webp"
    input_path = os.path.join("uploads", input_filename)
    output_path = os.path.join("outputs", output_filename)

    file.save(input_path)
    png_to_webp(input_path, output_path)

    # ✅ 삭제 처리
    delete_file_now(input_path)                  # 업로드된 PNG 즉시 삭제
    delete_file_after_delay(output_path, 60)     # 변환된 WEBP는 1분 후 삭제

    return jsonify({"success": True, "filename": output_filename})

@png_to_webp_bp.route("/download/<filename>", methods=["GET"])
def download_png_to_webp(filename):
    return send_from_directory("outputs", filename, as_attachment=True)