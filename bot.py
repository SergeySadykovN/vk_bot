# python v 3.11


import random
from time import sleep

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotEvent
from _token import token, _id
import logging

log = logging.getLogger('bot')


def configure_logger():
    """
    Функция для логирования в файл
    :return: bot.log
    """
    # logger = logging.getLogger('bot')
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('bot_log.log')
    stream_handler.setFormatter(logging.Formatter('%(asctime)s, %(levelname)s, %(message)s'))
    file_handler.setFormatter(logging.Formatter('%(asctime)s, %(levelname)s, %(message)s'))
    log.addHandler(stream_handler)
    log.addHandler(file_handler)
    stream_handler.setLevel(logging.INFO)
    log.setLevel(logging.DEBUG)


configure_logger()


class Bot:
    '''echo bot for vk group'''

    def __init__(self, id_group, _token):
        '''
        :param id_group: id group from vk
        :param _token: token from group
        '''
        self.group = id_group
        self.token = _token
        self.vk = vk_api.VkApi(token=_token)
        self.long_poller = VkBotLongPoll(self.vk, self.group)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception as exc:
                log.exception('Exception %s', exc)

    def on_event(self, event: VkBotEvent):
        """
        обработчик сообщений от бота
        :param event:  VkBotEvent
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            sleep(1)
            log.info('Event got %s', event)
            log.info('we received an event %s', event.type)
            peer_id = event.message.peer_id
            random_id = random.randint(0, 2 ** 20)
            text_message = str(event.message.text)
            self.api.messages.send(peer_id=peer_id,
                                   message=text_message,
                                   random_id=random_id)
            # try:
            #     self.api.messages.send(peer_id=peer_id, messages=text_message, random_id=random_id)
            # except Exception as exception:
            #     print(exception)

        else:
            log.debug("We don't know how to handle event with type %s", event.type)
            raise ValueError("We don't know how to handle event with type %s", event.type)
        #
        # if event.type == VkBotEventType.WALL_POST_NEW:
        #     print(event.type)
        #     print(event)
        #     print(event.message)
