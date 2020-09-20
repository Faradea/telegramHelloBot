# coding=utf-8
from datetime import datetime
from pip._vendor import requests


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot1171047679:AAGgG15of_Oe8chBIWaSQ1JttCFJ9SBAk-o/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset, 'allowed_updates': 'message'}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        print(result_json)
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if get_result:
            if len(get_result) > 3:
                last_update = get_result[-1]
            else:
                last_update = get_result[0]
        else:
            last_update = None

        return last_update


greet_bot = BotHandler("1171047679:AAGgG15of_Oe8chBIWaSQ1JttCFJ9SBAk-o")
trigger_request = 'да'
trigger_response = "манда"
now = datetime.now()


def main():
    new_offset = None

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        print last_update
        if last_update:
            last_chat_text = None
            last_chat_id = None
            last_update_id = last_update.get('update_id')
            last_chat_message = last_update.get('message')
            if last_chat_message:
                last_chat_text = last_chat_message.get('text')
                last_chat_id = last_chat_message.get('chat').get('id')

            if last_chat_text:
                print last_update['message']['text'].lower().encode('utf8')
                if last_update['message']['text'].lower().encode('utf8') == trigger_request:
                    greet_bot.send_message(last_chat_id, trigger_response)

            new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
