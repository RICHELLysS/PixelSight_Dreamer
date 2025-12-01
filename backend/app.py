# backend/app.py

# 1. 第一步：导入标准库
import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# 2. 第二步：极其重要！先加载环境变量，再导入自定义模块
# 这样下面的 services 才能读到 .env 里的 Key
from dotenv import load_dotenv
load_dotenv() 

# 3. 第三步：导入你的业务逻辑
# (如果这里报错，说明 .env 文件格式还有问题，或者是 ai_generator.py 里有错)
from services.ai_generator import generate_optimized_prompt, generate_image_from_api
from services.image_processor import process_pixel_art

app = Flask(__name__)
CORS(app) # 允许前端跨域访问

# 静态文件存储路径
UPLOAD_FOLDER = 'static/generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === 修复 "Not Found" 的关键部分 ===
@app.route('/')
def home():
    """
    当你访问 http://127.0.0.1:5000/ 时显示的欢迎页。
    用于确认后端是否正在运行。
    """
    return "<h1>PixelSight Backend is Running!</h1><p>Status: Online</p>"

# === 静态文件服务 ===
@app.route('/static/generated/<path:filename>')
def serve_static(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# === 图片生成 API ===
@app.route('/api/generate-art', methods=['POST'])
def api_generate_art():
    try:
        data = request.json
        user_prompt = data.get('prompt')
        style = data.get('style', '16bit') 
        asset_type = data.get('type', 'character')
        
        print(f"Received request: {user_prompt} [{style}]")

        # 1. 使用 Gemini 优化提示词
        optimized_prompt = generate_optimized_prompt(user_prompt, style, asset_type)
        print(f"Gemini Optimized: {optimized_prompt}")

        # 2. 调用 Imagen 3 生成图片 (使用的是同一个 Gemini Key)
        raw_image_bytes = generate_image_from_api(optimized_prompt)

        # 3. 本地图像后处理 (去背 + 保存)
        filename = f"{uuid.uuid4()}.png"
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # 这里的 remove_bg=True 决定是否去背
        process_pixel_art(raw_image_bytes, save_path, remove_bg=True)

        # 返回图片 URL 给前端
        return jsonify({
            "status": "success",
            "url": f"http://127.0.0.1:5000/static/generated/{filename}",
            "prompt_used": optimized_prompt
        })

    except Exception as e:
        print(f"SERVER ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# === 音乐生成 API (占位符) ===
@app.route('/api/generate-music', methods=['POST'])
def api_generate_music():
    # 目前单 Gemini API 暂不支持音乐，这里返回一个提示
    return jsonify({
        "status": "error", 
        "message": "Music generation is currently disabled in Single-API mode."
    }), 501

if __name__ == '__main__':
    print("Starting PixelSight Backend...")
    print("Ensure you have created the .env file with GEMINI_API_KEY")
    app.run(debug=True, port=5000)