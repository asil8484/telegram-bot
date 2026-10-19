import time
import requests

TOKEN = "8975153762:AAHX4ReeQFDFKIm7I-LPyopVKpA0EMvFrBQ"
MESSAGE = "https://t.me/+moU32bb8C2piYTUx"

# أيدي حسابك لتلقي الإشعارات الفورية
ADMIN_ID = 8729436707

SAVED_CHATS = {-1004422941187}
last_update_id = 0

def send_admin_alert(text):
    """دالة لإرسال إشعار إلى حسابك الشخصي على الخاص"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": ADMIN_ID, "text": text})
    except Exception as e:
        print(f"Error sending admin alert: {e}")

def update_active_chats():
    global last_update_id
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_update_id + 1}"
    try:
        response = requests.get(url).json()
        if response.get("ok"):
            results = response.get("result", [])
            for result in results:
                update_id = result.get("update_id", 0)
                if update_id > last_update_id:
                    last_update_id = update_id

                # 1. الترحيب بالمستخدمين في الخاص مع الزر
                if "message" in result and "chat" in result["message"]:
                    msg = result["message"]
                    chat = msg["chat"]
                    
                    if chat.get("type") == "private":
                        user_id = chat.get("id")
                        welcome_text = "هلا حبيبي لمشاهده المقاطع شارك الرابط ادناه في 2 مجموعات"
                        
                        # لوحة الأزرار الشفافة
                        reply_markup = {
                            "inline_keyboard": [
                                [
                                    {
                                        "text": "مقاطع",
                                        "url": "https://t.me/irprbnbot?startgroup=start"
                                    }
                                ]
                            ]
                        }
                        
                        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                        payload = {
                            "chat_id": user_id,
                            "text": welcome_text,
                            "reply_markup": reply_markup
                        }
                        try:
                            requests.post(send_url, json=payload)
                        except Exception as e:
                            print(f"Error sending welcome message: {e}")

                # 2. متابعة المجموعات وإرسال الإشعارات للآدمين
                chat = None
                if "message" in result and "chat" in result["message"]:
                    chat = result["message"]["chat"]
                elif "my_chat_member" in result and "chat" in result["my_chat_member"]:
                    chat_data = result["my_chat_member"]
                    chat = chat_data.get("chat", {})
                    
                    new_member = chat_data.get("new_chat_member", {})
                    if new_member.get("status") in ["member", "administrator"]:
                        chat_title = chat.get("title", "لا يوجد")
                        chat_id_val = chat.get("id")
                        chat_username = f"@{chat.get('username')}" if chat.get("username") else "لا يوجد"
                        
                        added_by = chat_data.get("from", {})
                        user_name = added_by.get("first_name", "مستخدم")
                        user_username = f"@{added_by.get('username')}" if added_by.get("username") else "لا يوجد"
                        user_id = added_by.get("id", "لا يوجد")
                        
                        bot_status = "عضو" if new_member.get("status") == "member" else "مشرف"

                        if chat_id_val not in SAVED_CHATS:
                            SAVED_CHATS.add(chat_id_val)
                            total_chats = len(SAVED_CHATS)
                            
                            alert_text = (
                                f"🆕 قام مستخدم جديد بإضافة البوت الخاص بك إلى مجموعة\n\n"
                                f"📌 معلومات المجموعة:\n"
                                f"• الاسم: {chat_title}\n"
                                f"• الأيدي: {chat_id_val}\n"
                                f"• المعرّف: {chat_username}\n"
                                f"👥 الاعضاء: —\n"
                                f"🔑 صلاحيات البوت: 👤 {bot_status}\n\n"
                                f"👤 معلومات العضو الذي قام بالإضافة:\n"
                                f"• الاسم: {user_name}\n"
                                f"• المعرّف: {user_username}\n"
                                f"• الآيدي: {user_id}\n"
                                f"🌐 اللغة: —\n\n"
                                f"📊 إجمالي المحادثات حتى الآن: {total_chats}"
                            )
                            send_admin_alert(alert_text)

                if chat and chat.get("type") in ["group", "supergroup"]:
                    SAVED_CHATS.add(chat["id"])
    except Exception as e:
        print(f"Error fetching chats: {e}")

def send_messages():
    update_active_chats()
    
    if not SAVED_CHATS:
        return

    for chat_id in list(SAVED_CHATS):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": MESSAGE
        }
        try:
            res = requests.post(url, json=payload).json()
            if not res.get("ok"):
                pass
        except Exception as e:
            print(f"Error sending to {chat_id}: {e}")

if __name
