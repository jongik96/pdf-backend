import os
import subprocess
from datetime import datetime

def convert_word_to_pdf(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # 확장자 제거, 시분초 추가
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    timestr = datetime.now().strftime("%H%M%S")
    pdf_name = f"{base_name}_{timestr}.pdf"
    output_path = os.path.join(output_dir, pdf_name)

    # LibreOffice 변환
    result = subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", output_dir, input_path
    ], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"LibreOffice 변환 오류: {result.stderr}")

    # LibreOffice는 기본적으로 base_name.pdf로 출력하므로 재명명
    orig_pdf = os.path.join(output_dir, f"{base_name}.pdf")
    if os.path.exists(orig_pdf) and orig_pdf != output_path:
        os.rename(orig_pdf, output_path)

    return output_path, os.path.basename(output_path)