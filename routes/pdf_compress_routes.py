from flask import Blueprint, request, jsonify
from services.pdf_compress_service import compress_pdf_with_ghostscript
from utils.file_cleanup import delete_file_now, delete_file_after_delay

pdf_compress_bp = Blueprint("pdf_compress", __name__)

@pdf_compress_bp.route("/convert/pdf-compress", methods=["POST"])
def compress_pdf_route():
    if "file" not in request.files:
        return jsonify(success=False, error="파일이 없습니다.")

    file = request.files["file"]
    quality = request.form.get("quality", "ebook")

    result = compress_pdf_with_ghostscript(file, quality)

    if result[0] is True:
        _, input_path, output_path, filename = result

        # ✅ 삭제 처리
        delete_file_now(input_path)                    # 임시 업로드 파일 즉시 삭제
        delete_file_after_delay(output_path, 60)       # 압축된 PDF는 1분 후 삭제

        return jsonify(success=True, filename=filename)
    else:
        return jsonify(success=False, error=result[1])