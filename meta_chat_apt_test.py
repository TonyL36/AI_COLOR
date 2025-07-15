import base64
from openai import OpenAI
API_KEY = "Bearer sk-live-***"
BASE_URL = "https://llm-api.mmchat.xyz"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
prompt = """
给这张图片上色。
"""

print(open("C:/Users/Dell/Desktop/testing.png", "rb"))
result = client.images.edit(
    model="gpt-image-1",
    image=open("C:/Users/Dell/Desktop/testing.png", "rb"),
    prompt=prompt
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("gift-basket.png", "wb") as f:
    f.write(image_bytes)


