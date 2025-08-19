from flask import Blueprint, request, jsonify, send_from_directory
from services.excel_to_pdf_service import convert_excel_to_pdf
import os
from utils.file_cleanup import delete_file_now, delete_file_after_delay

excel_to_pdf_bp = Blueprint('excel_to_pdf', __name__)

@excel_to_pdf_bp.route('/convert/excel-to-pdf', methods=['POST'])
def excel_to_pdf():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': '파일이 없습니다.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': '파일명이 없습니다.'}), 400

    try:
        pdf_path, pdf_filename = convert_excel_to_pdf(file)

        # ✅ 업로드 파일 삭제 (convert_excel_to_pdf 내부에서 저장한 경로 기준)
        if hasattr(file, 'filename'):
            upload_path = os.path.join("uploads", file.filename)
            delete_file_now(upload_path)

        # ✅ 출력 파일 삭제 예약
        delete_file_after_delay(pdf_path, delay=60)

        return jsonify({'success': True, 'filename': pdf_filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@excel_to_pdf_bp.route('/download/<filename>', methods=['GET'])
def download(filename):
    directory = os.path.abspath("outputs")
    return send_from_directory(directory, filename, as_attachment=True)