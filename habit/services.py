import os

import requests
from dotenv import load_dotenv


load_dotenv(override=True)

TG_URL = os.getenv('TG_URL')
TG_API_KEY = os.getenv('TG_API_KEY')

def send_message(text, chat_id):
    """
        Отправляет текстовое сообщение в указанный чат Telegram.

        Args:
            text: Текст сообщения для отправки.
            chat_id: Идентификатор чата Telegram, в который необходимо отправить сообщение.

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: Если произошла ошибка при отправке запроса к API Telegram.
            (Implicitly - because `requests.get` can raise this. It's good practice to document this).

        Example:
            send_message("Привет, мир!", "123456789")  # Sends "Привет, мир!" to chat ID 123456789.
        """
    params = {
        'text': text,
        'chat_id': chat_id,
    }
    response = requests.get(f'{TG_URL}{TG_API_KEY}/sendMessage', params=params)

if __name__ == "__main__":
    send_message('Самое время для полезной привычки!', 5152132161)  # пользователю 123456 ушло сообщение "Привет"
