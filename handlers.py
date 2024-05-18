"""Handler – функция которая принимает на вход текст входящего сообщения и context (dict) а возвращает bool:
True Если шаг пройдён,False Если данные введены неправильно"""
import re

re_name = re.compile(r'^[\w\-\s]{3,40}$')
re_email = re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b")


def handle_name(text, context):
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handle_email(text, context):
    mathes = re.findall(re_email, text)
    if len(mathes) > 0:
        context['email'] = mathes[0]
        return True
    else:
        return False
