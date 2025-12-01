import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# === 核心配置：只使用一个 Key ===
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Error: GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

# 设置安全过滤级别（防止 AI 拒绝生成游戏里的战斗素材）
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
}

def generate_optimized_prompt(user_input, style, asset_type):
    """
    步骤 1: 使用 Gemini 1.5 Flash (文本模型) 将用户的简单描述转化为专业的英文提示词
    """
    # 使用轻量级的 Flash 模型处理文本
    text_model = genai.GenerativeModel('gemini-1.5-flash')
    
    system_instruction = f"""
    You are an expert prompt engineer for Google Imagen 3 aimed at creating pixel art game assets. 
    User request: A {style} style {asset_type} described as "{user_input}".
    Convert this into a detailed, English prompt specifically for Imagen 3.
    
    Mandatory Keywords to include: "pixel art, {style} style, retro video game sprite, clean pixel grid, solid white background, flat 2d".
    If asset_type is 'character' or 'enemy', add: "full body shot, standing pose".
    
    Output ONLY the final English prompt string.
    """
    
    try:
        response = text_model.generate_content(
            system_instruction,
            safety_settings=safety_settings
        )
        optimized = response.text.strip()
        print(f"[Gemini Optimized Prompt]: {optimized}")
        return optimized
    except Exception as e:
        print(f"Prompt optimization failed, using raw input: {e}")
        # 如果优化失败，手动拼接一个简单的提示词
        return f"pixel art sprite of {user_input}, {style} style, white background"

def generate_image_from_api(prompt):
    """
    步骤 2: 使用 Imagen 3 (绘图模型) 根据优化后的提示词生成图片
    """
    print(f"[Imagen Generating] Prompt: {prompt}")
    
    # 使用专门的绘图模型 ID
    image_model = genai.GenerativeModel('imagen-3.0-generate-001')
    
    try:
        # 调用生成图片接口
        result = image_model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="1:1", # 生成正方形图片适合做素材
            safety_settings=safety_settings
        )
        
        # 检查是否成功生成
        if not result.images:
             raise Exception("Imagen returned no images. It might be blocked by safety filters.")

        # 返回第一张图片的二进制数据 (bytes)
        # 注意：Imagen 返回的是 JPEG 格式的 bytes
        return result.images[0].image_bytes
        
    except Exception as e:
        print(f"Imagen Generation Error: {e}")
        # 向上传递错误，让 app.py 处理
        raise e

# 音乐生成部分先留空，专注于图片功能
def generate_music_from_api(prompt, duration):
    raise NotImplementedError("Music generation using single Gemini API is not supported yet.")