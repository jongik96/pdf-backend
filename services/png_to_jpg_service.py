from PIL import Image

def png_to_jpg(input_path, output_path):
    with Image.open(input_path) as img:
        # PNG 투명 배경은 하얀색으로 변환 (JPG는 알파 채널 없음)
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            background.save(output_path, "JPEG")
        else:
            img.convert("RGB").save(output_path, "JPEG")