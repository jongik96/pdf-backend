# routes/download_routes.py
from flask import Blueprint, send_from_directory, abort
import os, mimetypes, urllib.parse
from werkzeug.utils import safe_join

download_bp = Blueprint("download_bp", __name__)

# 프로젝트 루트 기준 outputs 폴더
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'outputs')
OUTPUT_FOLDER = os.path.abspath(OUTPUT_FOLDER)

@download_bp.route("/download/<path:filename>", methods=["GET"])
def download_file(filename):
    # 경로 탐 traversal 방지 + 실제 파일 확인
    safe_path = safe_join(OUTPUT_FOLDER, filename)
    if not safe_path or not os.path.isfile(safe_path):
        abort(404, description="파일을 찾을 수 없습니다.")

    # MIME 추정 (없으면 octet-stream)
    guessed, _ = mimetypes.guess_type(safe_path)
    mime = guessed or "application/octet-stream"

    # 표시 파일명 (한글/유니코드 대응)
    display_name = os.path.basename(safe_path)
    quoted = urllib.parse.quote(display_name)

    # Flask 기본 attachment 헤더에 추가로 RFC5987 포함
    resp = send_from_directory(
        OUTPUT_FOLDER,
        display_name,
        as_attachment=True,
        mimetype=mime
    )
    # filename*(RFC5987)까지 명시 — 인앱/모바일에서 파일명 깨짐 방지
    resp.headers["Content-Disposition"] = (
        f"attachment; filename*=UTF-8''{quoted}"
    )
    # 인앱 안전성 & 캐시 (짧게)
    resp.headers["Cache-Control"] = "private, max-age=600"
    resp.headers["X-Content-Type-Options"] = "nosniff"

    return resp