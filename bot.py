import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotEvent
from _token import token, id_group


class Bot:
    def __init__(self, group_id, token):
        self.group = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            print('Получено событие')
            try:
                self.on_event(event)
            except Exception as err:
                print(err)

    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event.type)
            print(event)
            peer_id = event.message.peer_id
            random_id = random.randint(0, 2 ** 20)
            text_message = str(event.message.text)
            try:
                self.api.messages.send(peer_id=peer_id, message=text_message, random_id=random_id)
            except Exception as exc:
                print('Exception: ', exc)

        if event.type == VkBotEventType.WALL_POST_NEW:
            print(event.type)
            print(event)
            print(event.message)


if __name__ == '__main__':
    bot = Bot(id_group, token)
    bot.run()
