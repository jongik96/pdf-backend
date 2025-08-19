from flask import Blueprint, request, jsonify
from services.image_to_pdf_service import convert_images_to_pdf
from utils.file_cleanup import delete_file_now, delete_file_after_delay  # ✅ 추가

image_to_pdf_bp = Blueprint("image_to_pdf", __name__)

@image_to_pdf_bp.route("/convert/image-to-pdf", methods=["POST"])
def image_to_pdf():
    if "files" not in request.files:
        return jsonify({"success": False, "error": "No files uploaded"}), 400

    files = request.files.getlist("files")
    if not files or len(files) == 0:
        return jsonify({"success": False, "error": "No files found"}), 400

    try:
        image_paths, output_path, filename = convert_images_to_pdf(files)

        # ✅ 업로드된 이미지들 삭제
        for path in image_paths:
            delete_file_now(path)

        # ✅ 변환된 PDF는 1분 후 삭제
        delete_file_after_delay(output_path, delay=60)

        return jsonify({"success": True, "filename": filename})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500