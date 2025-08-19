from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Hello, this is a test PDF for conversion.", ln=True)
pdf.cell(200, 10, txt="It will be converted to a Word document.", ln=True)
pdf.output("example.pdf")

print("✅ example.pdf 생성 완료")
