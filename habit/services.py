import os

import requests
from dotenv import load_dotenv


load_dotenv(override=True)

TG_URL = os.getenv('TG_URL')
TG_API_KEY = os.getenv('TG_API_KEY')

def send_message(text, chat_id):
    params = {
        'text': text,
        'chat_id': chat_id,
    }
    response = requests.get(f'{TG_URL}{TG_API_KEY}/sendMessage', params=params)

if __name__ == "__main__":
    send_message('Самое время для полезной привычки!', 5152132161)  # пользователю 123456 ушло сообщение "Привет"
