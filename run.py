# 创建应用实例
import sys

from wxcloudrun import app
from flask import Flask, request
import requests

app = Flask(__name__)

# 替换为你的小程序 AppID 和 AppSecret
APPID = 'wx5b6537f52133de0f'
SECRET = 'a40c0eaacf4e4b9d784ca9e9e2c66b11'

@app.route('/login', methods=['POST'])  # Fixed: Added 'POST' as a string
def login():
    # 获取前端发送的 code
    code = request.json.get('code')
    if not code:
        return {'error': 'Missing code'}, 400

    # 向微信服务器发送请求，换取 openid 和 session_key
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    data = response.json()

    if 'openid' in data:
        # 这里可以根据业务需求生成自定义的登录态信息（如 token）
        # 为了简单起见，这里直接返回 openid
        return {'openid': data['openid']}
    else:
        return {'error': data.get('errmsg', 'Unknown error')}, 500
# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])
