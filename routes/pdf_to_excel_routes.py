from flask import Blueprint, request, jsonify
import os
from services.pdf_to_excel_service import convert_pdf_to_excel
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가
from datetime import datetime
from werkzeug.utils import secure_filename

pdf_to_excel_bp = Blueprint("pdf_to_excel", __name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@pdf_to_excel_bp.route("/convert/pdf-to-excel", methods=["POST"])
def handle_pdf_to_excel():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Empty filename"}), 400

    excel_format = request.form.get("format", "xlsx")
    if excel_format not in ("xlsx", "csv"):
        excel_format = "xlsx"

    timestr = datetime.now().strftime("%H%M%S")
    base, ext = os.path.splitext(secure_filename(file.filename))
    input_filename = f"{base}_{timestr}{ext}"
    input_path = os.path.join(UPLOAD_FOLDER, input_filename)

    file.save(input_path)

    try:
        output_path, output_filename = convert_pdf_to_excel(
            input_path, OUTPUT_FOLDER, excel_format, timestr
        )

        # ✅ 파일 삭제 처리
        delete_file_now(input_path)                    # 업로드 파일 즉시 삭제
        delete_file_after_delay(output_path, 60)       # 변환 결과는 1분 후 삭제

        return jsonify({
            "success": True,
            "message": "변환에 성공했습니다.",
            "filename": output_filename
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500