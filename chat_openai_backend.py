import base64
import io
from flask import Flask, request, send_file, jsonify
from openai import OpenAI
from flask_cors import CORS



# ====== 配置 ======
API_KEY = "Bearer sk-live-***"
BASE_URL = "https://llm-api.mmchat.xyz"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

app = Flask(__name__)
CORS(app)  # 允许所有来源访问后端

# ====== 路由处理 ======
@app.route('/colorize', methods=['POST'])
def colorize_image():
    if 'image' not in request.files:
        return jsonify({"error": "未上传图像"}), 400

    image_file = request.files['image']
    prompt = request.form.get('prompt')
    if not prompt or prompt.strip() == "":
        prompt = "给这张图片上色。"

    try:
        print("Received:", image_file.filename, "Prompt:", prompt)

        # 读取图片内容为字节流，并赋予 .name 属性供 SDK 使用
        image_bytes = image_file.read()
        if len(image_bytes) == 0:
            return jsonify({"error": "图像为空"}), 400

        image_stream = io.BytesIO(image_bytes)
        image_stream.name = image_file.filename

        # === 关键调用：完全照你的格式 ===
        result = client.images.edit(
            model="gpt-image-1",
            image=image_stream,
            prompt=prompt
        )
        print("API 调用成功，返回结果结构：", result)

        # === 解析返回值 ===
        if not result.data or not result.data[0].b64_json:
            return jsonify({"error": "API 没有返回图像内容"}), 502

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # 可选调试写出
        with open("colored_image_debug.png", "wb") as f:
            f.write(image_bytes)

        # 返回图片 blob 给前端
        return send_file(
            io.BytesIO(image_bytes),
            mimetype="image/png",
            as_attachment=False,
            download_name="colorized.png"
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ====== 运行入口 ======
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
