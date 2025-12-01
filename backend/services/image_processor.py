from rembg import remove
from PIL import Image
import io

def process_pixel_art(image_bytes, output_path, remove_bg=True):
    # 1. 读取图片
    img = Image.open(io.BytesIO(image_bytes))
    
    # 2. 自动去背 (Rembg) - 这是生成 Sprite 的核心
    if remove_bg:
        img = remove(img)
    
    # 3. 调整大小/量化 (可选，保持像素清晰)
    # 如果图片太大，可以缩小再放大来制造复古感
    # img = img.resize((64, 64), Image.NEAREST)
    # img = img.resize((512, 512), Image.NEAREST)

    # 4. 保存
    img.save(output_path, format="PNG")