from PyPDF2 import PdfReader, PdfWriter

def extract_pages(input_path, output_path, pages_str):
    """
    input_path: 원본 PDF 경로
    output_path: 추출 결과 PDF 경로
    pages_str: "1,3,5-7" 이런 식의 문자열
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # 페이지 번호 파싱 (1-based를 0-based로 변환)
    page_nums = set()
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            start, end = int(start), int(end)
            for i in range(start, end + 1):
                page_nums.add(i - 1)  # 0-based
        else:
            page_nums.add(int(part) - 1)
    
    for i in sorted(page_nums):
        if 0 <= i < len(reader.pages):
            writer.add_page(reader.pages[i])
    
    with open(output_path, "wb") as f:
        writer.write(f)