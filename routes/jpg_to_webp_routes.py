from flask import Blueprint, request, jsonify, send_from_directory
from services.jpg_to_webp_service import jpg_to_webp
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
import os
from datetime import datetime
from werkzeug.utils import secure_filename

jpg_to_webp_bp = Blueprint("jpg_to_webp", __name__)

@jpg_to_webp_bp.route("/convert/jpg-to-webp", methods=["POST"])
def convert_jpg_to_webp():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file or not (file.filename.lower().endswith(".jpg") or file.filename.lower().endswith(".jpeg")):
        return jsonify({"success": False, "error": "JPG 파일만 지원됩니다."}), 400

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    name, _ = os.path.splitext(secure_filename(file.filename))
    timestr = datetime.now().strftime("%H%M%S")
    input_filename = f"{name}_{timestr}.jpg"
    input_path = os.path.join("uploads", input_filename)
    output_filename = f"{name}_{timestr}.webp"
    output_path = os.path.join("outputs", output_filename)

    file.save(input_path)
    jpg_to_webp(input_path, output_path)

    # ✅ 삭제 처리
    delete_file_now(input_path)                    # 업로드 JPG 즉시 삭제
    delete_file_after_delay(output_path, 60)       # 변환된 WEBP 1분 후 삭제

    return jsonify({"success": True, "filename": output_filename})

@jpg_to_webp_bp.route("/download/<filename>", methods=["GET"])
def download_jpg_to_webp(filename):
    return send_from_directory("outputs", filename, as_attachment=True)