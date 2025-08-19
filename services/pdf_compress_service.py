import tempfile
import subprocess
import os
from datetime import datetime
from werkzeug.utils import secure_filename

DOWNLOAD_FOLDER = "outputs"

def compress_pdf_with_ghostscript(input_pdf_file, quality="ebook"):
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    # 입력 파일 임시 저장 (delete=False로 나중에 직접 삭제)
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_input:
        input_pdf_file.save(temp_input.name)
        input_path = temp_input.name

    original_name = os.path.splitext(secure_filename(input_pdf_file.filename))[0]
    timestr = datetime.now().strftime("%H%M%S")
    output_filename = f"{original_name}_{timestr}_compressed.pdf"
    output_path = os.path.join(DOWNLOAD_FOLDER, output_filename)

    gs_quality = {
        "printer": "/printer",
        "ebook": "/ebook",
        "screen": "/screen"
    }.get(quality, "/ebook")

    gs_cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={gs_quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]

    try:
        subprocess.check_call(gs_cmd)
    except Exception as e:
        if os.path.exists(input_path):
            os.remove(input_path)
        return False, str(e)

    # input_path는 삭제하지 않고, 라우터에서 삭제하도록 넘김
    return True, input_path, output_path, output_filename