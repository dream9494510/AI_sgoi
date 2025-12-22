"""
AI 營養師聊天室 - 簡化版 (穩定可用)
支援對話記憶,避免過濾問題
"""

API_KEY = "AIzaSyAQ6mbQm6fttYW2se__-jTsOBBDrLLAPdU"

import google.generativeai as genai

print("=" * 60)
print("AI 營養師聊天室")
print("=" * 60)
print("特色: 支援對話記憶,AI 會記住之前的對話")
print("=" * 60)

# 配置
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 對話歷史
conversation = []

def ask_ai(question):
    """提問並記住對話"""
    global conversation

    # 構建上下文
    if conversation:
        # 只保留最近3輪(6則訊息)
        recent = conversation[-6:]
        context_parts = []
        for i, msg in enumerate(recent):
            role = "Q" if i % 2 == 0 else "A"
            # 限制長度避免過長
            content = msg[:150] if len(msg) > 150 else msg
            context_parts.append(f"{role}: {content}")

        context = "\n".join(context_parts)
        full_prompt = f"{context}\n\nQ: {question}\n\n請用繁體中文自然回答，語氣輕鬆友善。推薦選項控制在3項以內。不要使用markdown格式符號如**或##。"
    else:
        full_prompt = f"{question}\n\n請用繁體中文自然回答，語氣輕鬆友善。推薦選項控制在3項以內。不要使用markdown格式符號如**或##。"

    # 呼叫 AI
    try:
        response = model.generate_content(full_prompt)
        answer = response.text

        # 移除可能殘留的 markdown 符號
        answer = answer.replace('**', '').replace('##', '').replace('###', '')

        # 記錄對話
        conversation.append(question)
        conversation.append(answer)

        return answer
    except Exception as e:
        return f"[錯誤] {e}"

# 聊天循環
print("\n開始聊天")
print("-" * 60)
print("指令:")
print("  - 輸入問題,AI 會記住對話")
print("  - 'clear' 清除歷史")
print("  - 'history' 查看記錄")
print("  - 'q' 離開")
print("-" * 60)

conversation_count = 0

while True:
    try:
        user_input = input("\n你: ").strip()

        if not user_input:
            continue

        # 特殊指令
        if user_input.lower() in ['q', 'exit', 'quit']:
            print("\nAI: 再見!祝你健康!")
            break

        if user_input.lower() in ['clear', 'reset']:
            conversation = []
            conversation_count = 0
            print("\n[OK] 對話歷史已清除")
            continue

        if user_input.lower() == 'history':
            if conversation:
                print(f"\n對話記錄 ({len(conversation)} 則):")
                for i, msg in enumerate(conversation):
                    role = "你" if i % 2 == 0 else "AI"
                    preview = msg[:80] + "..." if len(msg) > 80 else msg
                    print(f"{i+1}. [{role}] {preview}")
            else:
                print("\n[!] 目前沒有對話記錄")
            continue

        if user_input.lower() in ['examples', 'help']:
            print("\n範例問題:")
            print("  1. 午餐推薦什麼菜?")
            print("  2. 剛才那個怎麼做? (測試記憶)")
            print("  3. 推薦健康的餐廳")
            print("  4. 減重可以吃水果嗎?")
            continue

        # 提問
        conversation_count += 1
        print(f"\nAI [第{conversation_count}輪,記憶{len(conversation)//2}輪]: ", end="", flush=True)

        answer = ask_ai(user_input)
        print(answer)

    except KeyboardInterrupt:
        print("\n\n[!] 中斷")
        break
    except EOFError:
        print("\n\n[!] 結束")
        break

# 統計
if conversation_count > 0:
    print("\n" + "=" * 60)
    print("對話統計")
    print("=" * 60)
    print(f"  總輪數: {conversation_count}")
    print(f"  記錄數: {len(conversation)//2} 輪")
    print("\n感謝使用!")
