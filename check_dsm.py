import requests
import os
import warnings

warnings.filterwarnings("ignore")

DSM_URL = os.environ.get("DSM_URL")
TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

STATUS_FILE = "status.txt"

print("Script started")
print(f"DSM_URL: {DSM_URL}")
print(f"TG_TOKEN present: {bool(TG_TOKEN)}")
print(f"TG_CHAT_ID: {TG_CHAT_ID}")
print(f"Status file exists: {os.path.exists(STATUS_FILE)}")

def is_dsm_up():
    try:
        r = requests.get(DSM_URL, timeout=10, verify=False)
        return r.status_code == 200 and "Synology" in r.text
    except Exception:
        return False

def send_message(text):
    if not TG_TOKEN or not TG_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TG_CHAT_ID,
        "text": text
    })

previous = None
if os.path.exists(STATUS_FILE):
    previous = open(STATUS_FILE).read().strip()

current = "UP" if is_dsm_up() else "DOWN"

if current != previous:
    if current == "DOWN":
        send_message("❌ Сервер Offline")
    else:
        send_message("✅ Сервер Online")

    with open(STATUS_FILE, "w") as f:
        f.write(current)
