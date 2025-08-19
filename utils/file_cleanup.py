# utils/file_cleanup.py

import os
import threading
import time

# 출력 파일을 일정 시간 뒤 삭제
def delete_file_after_delay(file_path, delay=60):
    def delete():
        time.sleep(delay)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"[삭제 완료] {file_path}")
            except Exception as e:
                print(f"[삭제 실패] {file_path} - {e}")
    threading.Thread(target=delete).start()

# 업로드 파일 즉시 삭제
def delete_file_now(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"[업로드 삭제 완료] {file_path}")
        except Exception as e:
            print(f"[업로드 삭제 실패] {file_path} - {e}")