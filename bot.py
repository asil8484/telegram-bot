import time
import requests

TOKEN = "8975153762:AAHX4ReeQFDFKIm7I-LPyopVKpA0EMvFrBQ"
MESSAGE = "https://t.me/+moU32bb8C2piYTUx"

SAVED_CHATS = {-1004422941187}

def update_active_chats():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    try:
        response = requests.get(url).json()
        if response.get("ok"):
            for result in response.get("result", []):
                chat = None
                if "message" in result and "chat" in result["message"]:
                    chat = result["message"]["chat"]
                elif "my_chat_member" in result and "chat" in result["my_chat_member"]:
                    chat = result["my_chat_member"]["chat"]
                
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
    print("Bot started...")
    while True:
        send_messages()
        time.sleep(180)
