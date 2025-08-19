import os
from pdf2docx import Converter

def convert_pdf_to_word(input_path, output_dir, timestr=""):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_filename = f"{base_name}_{timestr}.docx" if timestr else f"{base_name}.docx"
    output_path = os.path.join(output_dir, output_filename)

    cv = Converter(input_path)
    cv.convert(
        output_path,
        start=0, end=None,
        preserve_font=True,
        preserve_layout=True,
        extract_image=True,
        extract_table=True
    )
    cv.close()
    return output_path, output_filename