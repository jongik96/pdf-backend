from flask import Blueprint, request, jsonify, send_from_directory
from services.pdf_split_service import split_pdf
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
import os
from datetime import datetime
from werkzeug.utils import secure_filename

pdf_split_bp = Blueprint("pdf_split", __name__)

@pdf_split_bp.route("/convert/pdf-split", methods=["POST"])
def pdf_split():
    if "file" not in request.files or "ranges" not in request.form:
        return jsonify({"success": False, "error": "파일과 범위를 모두 입력하세요."}), 400

    file = request.files["file"]
    ranges = request.form["ranges"]

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    timestr = datetime.now().strftime("%H%M%S")
    base, ext = os.path.splitext(secure_filename(file.filename))
    input_filename = f"{base}_{timestr}{ext}"
    input_path = os.path.join("uploads", input_filename)

    file.save(input_path)
    try:
        output_base = f"{base}_{timestr}"
        zip_filename = split_pdf(input_path, ranges, output_base)
        zip_path = os.path.join("outputs", zip_filename)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    # ✅ 삭제 처리
    delete_file_now(input_path)
    delete_file_after_delay(zip_path, 60)

    return jsonify({"success": True, "filename": zip_filename})

@pdf_split_bp.route("/download/<filename>", methods=["GET"])
def download_pdf_split(filename):
    return send_from_directory("outputs", filename, as_attachment=True)