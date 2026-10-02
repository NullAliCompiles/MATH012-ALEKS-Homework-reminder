#AI USAGE DISCLAIMER:
#The core code was hand-written
#AI was used to review the code, fix errors, and improve variable naming

import os
import time
import requests
import schedule
from dotenv import load_dotenv

BLACKBOARD_LINK = "https://blackboard.kfupm.edu.sa/ultra/courses/_17883_1/outline"

MESSAGE =  f"\
تذكير بواجب ALEKS!!\n\
ينتهي الواجب يوم بكرا السبت الساعة 11:59PM\n\n\
ملاحظة: الواجبات عليها 7% من المعدل\n\n\
رابط البلاكبورد:\n \
{BLACKBOARD_LINK}\
"

load_dotenv() #load the env file

def get_required_env(name):
    value = os.getenv(name)
    if not value: #if one of the env variaples are missing (like API Token or group id)
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value #if everything's good, go ahead


id_instance = get_required_env("API_INSTANCE_ID")
api_token = get_required_env("API_TOKEN")
group_id = get_required_env("MATH_GROUP_ID")


def send_ALEKS_hw_reminder():
    url = f"https://api.green-api.com/waInstance{id_instance}/sendMessage/{api_token}"

    payload = {
        "chatId": group_id,
        "message": MESSAGE
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        #if message was sent succsesfully (or however it's spelled)
        if response.status_code == 200:
            print("✅ Message sent")
        else: #if an error happens, print the error number and details
            print(f"❌ Failed to send message.\nError code: {response.status_code}\n")
            print(f"Error details:\n{response.text}\n")

    except requests.RequestException as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    # Schedule the reminder for Friday at 7:00 PM.
    schedule.every().friday.at("19:00").do(send_ALEKS_hw_reminder)

    while True:
        schedule.run_pending()
        time.sleep(45)

    #in case you wanna test if the message does get sent or not, uncomment the line underneath:
    #send_ALEKS_hw_reminder()