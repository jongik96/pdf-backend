from flask import Blueprint, request, jsonify, send_from_directory
from services.pdf_merge_service import merge_pdfs
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
import os
from datetime import datetime
from werkzeug.utils import secure_filename

pdf_merge_bp = Blueprint("pdf_merge", __name__)

@pdf_merge_bp.route("/convert/pdf-merge", methods=["POST"])
def pdf_merge():
    files = request.files.getlist("files")
    if not files or len(files) < 2:
        return jsonify({"success": False, "error": "최소 2개 이상의 PDF 파일을 업로드하세요."}), 400

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    input_paths = []
    for file in files:
        base = os.path.splitext(secure_filename(file.filename))[0]
        ext = os.path.splitext(secure_filename(file.filename))[1]
        timestr = datetime.now().strftime("%H%M%S")
        filename = f"{base}_{timestr}{ext}"
        input_path = os.path.join("uploads", filename)
        file.save(input_path)
        input_paths.append(input_path)

    first_base = os.path.splitext(secure_filename(files[0].filename))[0]
    timestr = datetime.now().strftime("%H%M%S")
    output_filename = f"{first_base}_{timestr}_merged.pdf"
    output_path = os.path.join("outputs", output_filename)

    merge_pdfs(input_paths, output_path)

    # ✅ 업로드된 PDF들 삭제
    for path in input_paths:
        delete_file_now(path)

    # ✅ 병합된 결과 PDF는 1분 뒤 삭제
    delete_file_after_delay(output_path, 60)

    return jsonify({"success": True, "filename": output_filename})

@pdf_merge_bp.route("/download/<filename>", methods=["GET"])
def download_merged_pdf(filename):
    return send_from_directory("outputs", filename, as_attachment=True)