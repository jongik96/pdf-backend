# services/pdf_remove_service.py
from PyPDF2 import PdfReader, PdfWriter

def remove_pages(input_path, output_path, remove_pages):
    # remove_pages: "2,5,8-10"
    reader = PdfReader(input_path)
    writer = PdfWriter()
    total = len(reader.pages)

    # 문자열을 실제 인덱스 리스트로 변환 (1부터 시작)
    pages_to_remove = set()
    for part in remove_pages.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            pages_to_remove.update(range(start, end + 1))
        else:
            pages_to_remove.add(int(part))
    pages_to_remove = {i-1 for i in pages_to_remove if 1 <= i <= total}

    for i in range(total):
        if i not in pages_to_remove:
            writer.add_page(reader.pages[i])

    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path