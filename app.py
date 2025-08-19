from flask import Flask
from flask_cors import CORS
from routes.pdf_to_word_routes import pdf_to_word_bp
from routes.download_routes import download_bp
from routes.pdf_to_image_routes import pdf_to_image_bp
from routes.pdf_to_excel_routes import pdf_to_excel_bp
from routes.pdf_to_ppt_routes import pdf_to_ppt_bp
from routes.word_to_pdf_routes import word_to_pdf_bp
from routes.image_to_pdf_routes import image_to_pdf_bp
from routes.excel_to_pdf_routes import excel_to_pdf_bp
from routes.ppt_to_pdf_routes import ppt_to_pdf_bp
from routes.image_resize_routes import image_resize_bp
from routes.image_compress_routes import image_compress_bp
from routes.jpg_to_png_routes import jpg_to_png_bp
from routes.png_to_jpg_routes import png_to_jpg_bp
from routes.heic_to_jpg_routes import heic_to_jpg_bp
from routes.jpg_to_webp_routes import jpg_to_webp_bp
from routes.png_to_webp_routes import png_to_webp_bp

from routes.pdf_merge_routes import pdf_merge_bp
from routes.pdf_split_routes import pdf_split_bp
from routes.pdf_remove_routes import pdf_remove_bp
from routes.pdf_extract_routes import pdf_extract_bp
from routes.pdf_compress_routes import pdf_compress_bp



import os

app = Flask(__name__)
CORS(app)

OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ✅ Blueprint 등록 (Flask 인스턴스 생성 후!)
app.register_blueprint(pdf_to_word_bp)
app.register_blueprint(pdf_to_image_bp) 
app.register_blueprint(download_bp)
app.register_blueprint(pdf_to_excel_bp)
app.register_blueprint(pdf_to_ppt_bp)
app.register_blueprint(word_to_pdf_bp)
app.register_blueprint(image_to_pdf_bp)
app.register_blueprint(excel_to_pdf_bp)
app.register_blueprint(ppt_to_pdf_bp)
app.register_blueprint(image_resize_bp)
app.register_blueprint(image_compress_bp)
app.register_blueprint(jpg_to_png_bp)
app.register_blueprint(png_to_jpg_bp)
app.register_blueprint(heic_to_jpg_bp)
app.register_blueprint(jpg_to_webp_bp)
app.register_blueprint(png_to_webp_bp)

app.register_blueprint(pdf_merge_bp)
app.register_blueprint(pdf_split_bp)
app.register_blueprint(pdf_remove_bp)
app.register_blueprint(pdf_extract_bp)
app.register_blueprint(pdf_compress_bp)

@app.route("/", methods=["GET"])
def index():
    return "✅ PDF 변환 서버 작동 중입니다.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)