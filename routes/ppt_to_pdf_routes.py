from flask import Blueprint, request, jsonify
from services.ppt_to_pdf_service import convert_ppt_to_pdf
from utils.file_cleanup import delete_file_now, delete_file_after_delay
import os
from datetime import datetime
from werkzeug.utils import secure_filename

ppt_to_pdf_bp = Blueprint("ppt_to_pdf", __name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@ppt_to_pdf_bp.route("/convert/ppt-to-pdf", methods=["POST"])
def ppt_to_pdf_route():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "파일이 첨부되지 않았습니다."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "파일명이 없습니다."}), 400

    timestr = datetime.now().strftime("%H%M%S")
    base, ext = os.path.splitext(secure_filename(file.filename))
    input_filename = f"{base}_{timestr}{ext}"
    input_path = os.path.join(UPLOAD_FOLDER, input_filename)
    file.save(input_path)

    try:
        output_path, output_filename = convert_ppt_to_pdf(input_path, OUTPUT_FOLDER)

        delete_file_now(input_path)                   # 업로드 파일 즉시 삭제
        delete_file_after_delay(output_path, 60)      # 결과 PDF는 1분 후 삭제

        return jsonify({"success": True, "filename": output_filename})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500