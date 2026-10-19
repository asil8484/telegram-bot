import time
import requests

TOKEN = "8975153762:AAHX4ReeQFDFKIm7I-LPyopVKpA0EMvFrBQ"
MESSAGE = "https://t.me/+moU32bb8C2piYTUx"

# أيدي حسابك الصحيح لتلقي الإشعارات
ADMIN_ID = 8729436707

SAVED_CHATS = {-1004422941187}

def send_admin_alert(text):
    """دالة لإرسال إشعار إلى حسابك الشخصي على الخاص"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": ADMIN_ID, "text": text})
    except Exception as e:
        print(f"Error sending admin alert: {e}")

def update_active_chats():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    try:
        response = requests.get(url).json()
        if response.get("ok"):
            for result in response.get("result", []):
                chat = None
                chat_title = "مجموعة"
                
                if "message" in result and "chat" in result["message"]:
                    chat = result["message"]["chat"]
                    chat_title = chat.get("title", "مجموعة")
                elif "my_chat_member" in result and "chat" in result["my_chat_member"]:
                    chat = result["my_chat_member"]["chat"]
                    chat_title = chat.get("title", "مجموعة")
                    
                    # التحقق مما إذا تم إضافة البوت حديثاً للمجموعة
                    new_member = result["my_chat_member"].get("new_chat_member", {})
                    if new_member.get("status") in ["member", "administrator"]:
                        user_who_added = result["my_chat_member"].get("from", {}).get("first_name", "مستخدم")
                        chat_id_val = chat.get("id")
                        
                        if chat_id_val not in SAVED_CHATS:
                            # إرسال إشعار لك على الخاص
                            alert_text = (
                                f"🚨 تم إضافة البوت إلى مجموعة جديدة!\n\n"
                                f"📌 اسم المجموعة: {chat_title}\n"
                                f"🆔 الأيدي: {chat_id_val}\n"
                                f"👤 بواسطة: {user_who_added}"
                            )
                            send_admin_alert(alert_text)
                
                if chat and chat.get("type") in ["group", "supergroup"]:
                    SAVED_CHATS.add(chat["id"])
    except Exception as e:
        print(f"Error fetching chats: {e}")

def send_messages():
    update_active_chats()
    
    if not SAVED_CHATS:
        print("No groups found yet. Send a message in the group!")
        return

    for chat_id in list(SAVED_CHATS):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": MESSAGE
        }
        try:
            res = requests.post(url, json=payload).json()
            if res.get("ok"):
                print(f"Sent to group: {chat_id}")
            else:
                print(f"Failed for {chat_id}: {res.get('description')}")
        except Exception as e:
            print(f"Error sending to {chat_id}: {e}")

if __name__ == "__main__":
    print("Bot started with correct admin notifications...")
    while True:
        send_messages()
        time.sleep(180)
