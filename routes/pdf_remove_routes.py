from flask import Blueprint, request, jsonify, send_from_directory
from services.pdf_remove_service import remove_pages
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
import os
from datetime import datetime
from werkzeug.utils import secure_filename

pdf_remove_bp = Blueprint("pdf_remove", __name__)

@pdf_remove_bp.route("/convert/pdf-remove", methods=["POST"])
def pdf_remove():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]
    pages = request.form.get("pages", "")

    if not file or not pages.strip():
        return jsonify({"success": False, "error": "잘못된 요청"}), 400

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    timestr = datetime.now().strftime("%H%M%S")
    base, ext = os.path.splitext(secure_filename(file.filename))

    input_filename = f"{base}_{timestr}{ext}"
    input_path = os.path.join("uploads", input_filename)
    output_filename = f"{base}_{timestr}_removed{ext}"
    output_path = os.path.join("outputs", output_filename)

    file.save(input_path)
    remove_pages(input_path, output_path, pages)

    # ✅ 삭제 처리
    delete_file_now(input_path)
    delete_file_after_delay(output_path, 60)

    return jsonify({"success": True, "filename": output_filename})

@pdf_remove_bp.route("/download/<filename>", methods=["GET"])
def download_removed(filename):
    return send_from_directory("outputs", filename, as_attachment=True)