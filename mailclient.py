#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
"""
    Простой_email_клиент

    для работы в нашей сети скопируйте и выполните следующие строки:
    echo -e 'MAIL_SERVER=10.0.7.67\nMAIL_SERVER_PORT=25\nMAIL_LOGIN=\nMAIL\
        _PSSWD=\nMAIL_FROM=\nMAIL_TO=\nMAIL_CODING=utf-8' >> ./env

    запуск через run :
    ./run ./env ./mailclient.py

"""
import os
import smtplib
from email.mime.text import MIMEText
#===============================================================================
def is_str(value):
    """
    Проверка типа
    """
    if not isinstance(value, str):
        raise TypeError('String is required.')
    return True


def is_env(env_list):
    """
    Проверка наличия треюуемых переменных окружения
    """
    for env in env_list:
        if not os.environ.get(env):
            raise ValueError('{0} not exists'.format(env))

def check_responce(responce):
    """
    Проверка ответа сервера
        responce: ответ сервера
    """
    if not responce:
        return 'Recive error'
    if len(responce) != 0:
        return responce
    if responce[0] != 235:
        return responce


class Mailclient:
    """
    Простой отправитель текстовых сообщений
    """
    def __init__(self, subject='Lovely yours...', text_type=''):
        """
        subjecta: Заголовок которым будут сопровождаться все письма
        text_type: тип текста в письме -
             'html': для странички,
             'plain'/'': для простого письма
        """
        env_list = [
            'MAIL_SERVER',
            'MAIL_SERVER_PORT',
            'MAIL_LOGIN',
            'MAIL_PSSWD',
            'MAIL_FROM',
            'MAIL_TO',
            'MAIL_CODING',
        ]
        is_env(env_list)

        if is_str(text_type):
            self.__text_type = text_type

        if is_str(subject):
            self.__subject = subject

        self.__con_param = {
            key.lower():os.environ.get(key) for key in env_list
        }

    @property
    def get_params(self):
        """
        Получить параметры клиента
        """
        return self.__con_param


    def __recive(self, server, msg_obj):
        """
        Метод в котором перехватываются события
            server: объект соединения с сревером
            message: объект сообщение
        """
        resp = server.login(
            self.__con_param['mail_login'],
            self.__con_param['mail_psswd']
        )

        if check_responce(resp) is not None:
            resp = server.sendmail(
                self.__con_param['mail_from'],
                self.__con_param['mail_to'],
                msg_obj.as_string(),
            )
        server.close()

        return check_responce(resp)


    def sent(self, message='Hello! This is my test mail! Forever yours. Bug'):
        """
        Отправка сообщения
            message: текст сообщения, строка
        """
        is_str(message)

        msg = MIMEText(message, self.__text_type, self.__con_param['mail_coding'])
        msg['subject'] = self.__subject
        msg['to'] = self.__con_param['mail_to']
        msg['from'] = self.__con_param['mail_from']

        server = smtplib.SMTP(
            self.__con_param['mail_server'], self.__con_param['mail_server_port']
        )
        return self.__recive(server, msg)

#===============================================================================
if __name__ == "__main__":
    MC = Mailclient()
    print(MC.get_params)
    MC.sent()
