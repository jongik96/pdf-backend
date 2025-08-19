from flask import Blueprint, request, jsonify, send_from_directory
from services.pdf_extract_service import extract_pages
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
import os
from datetime import datetime
from werkzeug.utils import secure_filename

pdf_extract_bp = Blueprint("pdf_extract", __name__)

@pdf_extract_bp.route("/convert/pdf-extract", methods=["POST"])
def pdf_extract():
    if "file" not in request.files or "pages" not in request.form:
        return jsonify({"success": False, "error": "파일 및 페이지 정보 필요"}), 400

    file = request.files["file"]
    pages = request.form.get("pages", "")
    if not file or not pages:
        return jsonify({"success": False, "error": "입력값 오류"}), 400

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    original = os.path.splitext(secure_filename(file.filename))[0]
    ext = os.path.splitext(secure_filename(file.filename))[1]
    timestr = datetime.now().strftime("%H%M%S")

    input_path = os.path.join("uploads", f"{original}_{timestr}{ext}")
    output_filename = f"{original}_{timestr}_extracted{ext}"
    output_path = os.path.join("outputs", output_filename)

    file.save(input_path)

    try:
        extract_pages(input_path, output_path, pages)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    # ✅ 삭제 처리
    delete_file_now(input_path)                    # 업로드된 원본 PDF 즉시 삭제
    delete_file_after_delay(output_path, 60)       # 추출된 결과 PDF는 1분 후 삭제

    return jsonify({"success": True, "filename": output_filename})

@pdf_extract_bp.route("/download/<filename>", methods=["GET"])
def download_pdf_extract(filename):
    return send_from_directory("outputs", filename, as_attachment=True)