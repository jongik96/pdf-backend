from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from services.pdf_to_ppt_service import convert_pdf_to_ppt
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
from datetime import datetime

pdf_to_ppt_bp = Blueprint("pdf_to_ppt", __name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@pdf_to_ppt_bp.route("/convert/pdf-to-ppt", methods=["POST"])
def pdf_to_ppt():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "파일이 없습니다."}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "파일명이 없습니다."}), 400

    timestr = datetime.now().strftime("%H%M%S")
    base, ext = os.path.splitext(secure_filename(file.filename))
    filename = f"{base}_{timestr}{ext}"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    try:
        output_path, output_filename = convert_pdf_to_ppt(input_path, OUTPUT_FOLDER, timestr)

        # ✅ 출력 파일 1분 뒤 삭제 예약
        delete_file_after_delay(output_path, 60)

        return jsonify({
            "success": True,
            "filename": output_filename
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # ✅ 업로드 파일 즉시 삭제
        delete_file_now(input_path)