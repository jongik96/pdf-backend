import os
import datetime
import subprocess
from werkzeug.utils import secure_filename

OUTPUT_DIR = "outputs"

def convert_excel_to_pdf(file):
    filename = secure_filename(file.filename)
    ext = filename.split('.')[-1].lower()
    base_name = os.path.splitext(filename)[0] or "excel"
    if ext not in ["xls", "xlsx", "csv"]:
        raise Exception("지원하지 않는 파일 형식입니다.")

    now = datetime.datetime.now().strftime('%H%M%S')
    temp_input_path = os.path.join(OUTPUT_DIR, f"{base_name}_{now}.{ext}")

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    file.save(temp_input_path)

    try:
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", OUTPUT_DIR,
            temp_input_path
        ], check=True)
    except Exception as e:
        raise Exception("LibreOffice 변환 실패: " + str(e))

    pdf_filename = f"{base_name}_{now}.pdf"
    pdf_file = os.path.join(OUTPUT_DIR, pdf_filename)
    if not os.path.exists(pdf_file):
        raise Exception("PDF 변환에 실패했습니다.")

    return pdf_file, pdf_filename