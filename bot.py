import os
import time
import requests

TOKEN = os.getenv("TOKEN", "8753053580:AAE8aNobN3ZmZYcvGbuKaivzyZa2Jx5_peY")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "5394090858"))

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?timeout=30"
    if offset:
        url += f"&offset={offset}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print("خطأ في الاتصال:", e)
        return None

def send_message(chat_id, text, reply_to_message_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id
    requests.post(url, json=payload)

def main():
    print("🚀 البوت يعمل الآن على السيرفر ومستعد لاستقبال الرسائل...")
    last_update_id = None
    
    while True:
        data = get_updates(offset=last_update_id)
        if data and "result" in data:
            for update in data["result"]:
                last_update_id = update["update_id"] + 1
                
                if "message" in update and "text" in update["message"]:
                    msg = update["message"]
                    user = msg["from"]
                    user_text = msg["text"]
                    chat_type = msg["chat"]["type"]
                    user_id = user["id"]
                    
                    if chat_type == "private" and user_id != ADMIN_CHAT_ID:
                        send_message(user_id, "تم استلام رسالتك بنجاح وسيتم تحويلها للمشرف للرد عليك.")
                        
                        admin_text = (
                            f"📩 **رسالة جديدة من مستخدم:**\n"
                            f"👤 الاسم: {user.get('first_name', '')} (@{user.get('username', 'لا يوجد')})\n"
                            f"🆔 المعرف: `{user_id}`\n\n"
                            f"💬 **النص:** {user_text}"
                        )
                        send_message(ADMIN_CHAT_ID, admin_text)

        time.sleep(1)

if __name__ == "__main__":
    main()
  
