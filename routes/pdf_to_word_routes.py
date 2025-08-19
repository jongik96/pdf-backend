from flask import Blueprint, request, jsonify
import os
from datetime import datetime
from services.pdf_to_word_service import convert_pdf_to_word

pdf_to_word_bp = Blueprint("pdf_to_word", __name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@pdf_to_word_bp.route("/convert/pdf-to-word", methods=["POST"])
def handle_pdf_to_word():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Empty filename"}), 400

    # 시분초 붙인 이름 만들기
    timestr = datetime.now().strftime("%H%M%S")
    base, ext = os.path.splitext(file.filename)
    input_filename = f"{base}_{timestr}{ext}"
    input_path = os.path.join(UPLOAD_FOLDER, input_filename)
    file.save(input_path)

    try:
        output_path, output_filename = convert_pdf_to_word(input_path, OUTPUT_FOLDER, timestr)
        return jsonify({
            "success": True,
            "filename": output_filename
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500