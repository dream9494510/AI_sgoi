"""
AI 聊天 API 後端
提供 HTTP API 給前端使用
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

API_KEY = "AIzaSyAQ6mbQm6fttYW2se__-jTsOBBDrLLAPdU"

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 配置 Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 儲存每個用戶的對話記錄 (使用 session_id)
conversations = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    """處理聊天請求"""
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')

        if not message:
            return jsonify({'error': '訊息不能為空'}), 400

        # 獲取該 session 的對話記錄
        if session_id not in conversations:
            conversations[session_id] = []

        conversation = conversations[session_id]

        # 構建上下文
        if conversation:
            # 只保留最近3輪(6則訊息)
            recent = conversation[-6:]
            context_parts = []
            for i, msg in enumerate(recent):
                role = "Q" if i % 2 == 0 else "A"
                content = msg[:150] if len(msg) > 150 else msg
                context_parts.append(f"{role}: {content}")

            context = "\n".join(context_parts)
            full_prompt = f"{context}\n\nQ: {message}\n\n請用繁體中文自然回答，語氣輕鬆友善。推薦選項控制在3項以內。不要使用markdown格式符號如**或##。"
        else:
            full_prompt = f"{message}\n\n請用繁體中文自然回答，語氣輕鬆友善。推薦選項控制在3項以內。不要使用markdown格式符號如**或##。"

        # 呼叫 AI
        response = model.generate_content(full_prompt)
        answer = response.text

        # 移除可能殘留的 markdown 符號
        answer = answer.replace('**', '').replace('##', '').replace('###', '')

        # 記錄對話
        conversation.append(message)
        conversation.append(answer)

        return jsonify({
            'success': True,
            'response': answer,
            'session_id': session_id
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """清除對話記錄"""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')

        if session_id in conversations:
            conversations[session_id] = []

        return jsonify({
            'success': True,
            'message': '對話記錄已清除'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """健康檢查"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("=" * 60)
    print("AI 聊天 API 伺服器")
    print("=" * 60)
    print("API 端點: http://localhost:5000")
    print("  - POST /api/chat    - 聊天")
    print("  - POST /api/clear   - 清除記錄")
    print("  - GET  /api/health  - 健康檢查")
    print("=" * 60)
    app.run(debug=True, port=5000)
