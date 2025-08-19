import os
import subprocess

def convert_ppt_to_pdf(input_path, output_dir):
    base = os.path.splitext(os.path.basename(input_path))[0]
    pdf_filename = f"{base}.pdf"
    output_path = os.path.join(output_dir, pdf_filename)

    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        input_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0 or not os.path.exists(output_path):
        raise Exception(f"변환 실패: {result.stderr.decode('utf-8')}")

    return output_path, pdf_filename