from PyPDF2 import PdfReader, PdfWriter
import os
import zipfile

OUTPUT_FOLDER = "outputs"

def split_pdf(input_path, ranges, output_base):
    with open(input_path, "rb") as f:
        reader = PdfReader(f)
        total_pages = len(reader.pages)
        outputs = []

        # ranges 예시: "1-3,5,7-8"
        parts = [r.strip() for r in ranges.split(",") if r.strip()]
        for idx, part in enumerate(parts):
            writer = PdfWriter()
            if "-" in part:
                start, end = [int(x) for x in part.split("-")]
                for p in range(start - 1, end):
                    if 0 <= p < total_pages:
                        writer.add_page(reader.pages[p])
            else:
                p = int(part) - 1
                if 0 <= p < total_pages:
                    writer.add_page(reader.pages[p])

            output_filename = f"{output_base}_part{idx+1}.pdf"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            with open(output_path, "wb") as out_f:
                writer.write(out_f)
            outputs.append(output_path)

    # 여러 파일 zip 묶기
    zip_filename = f"{output_base}_splits.zip"
    zip_path = os.path.join(OUTPUT_FOLDER, zip_filename)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file_path in outputs:
            zipf.write(file_path, os.path.basename(file_path))
            os.remove(file_path)  # 분할된 pdf 삭제(용량 절약)
    return zip_filename