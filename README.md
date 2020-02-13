### Простейший телеграмм бот-напоминалка

## Оглавление.
1. Описание 
2. Установка и настройка
3. Использование

## **Описание**
Телеграмм бот, который присылает сообщение в назначенное время. 
Возможности минимальны:
1. Добавление напоминания.
2. Вывод списка напоминаний.
3. Удаление напоминания.
4. Отправка напоминаний пользователю.

Бот разделен на две части.
1. bot.py отвечает за создание, удаление, вывод список напоминаний в приложение  Телеграмм.
2. reminds_handlers.py за отправку пользователю в мессенджер Телеграмм. 
3. webapp за отображение напоминаний на сайте.


## **Установка и настройка**
Для правильной работы необходимо:
1. Python 3.7 и выше
2. Связь с сетью "Интернет"

Настройка:
1. Внести изменения в файл конфигурации. connect_settings.py

API_KEY = '' - ключ к боту, полученный от @botfather

PROXY_REMINDS_HANDLERS_PROXY = ''  -адрес прокси сервера

PROXY_REMINDS_HANDLERS_ACCOUNT = {"username": "", "password": ""} -пароль и  логин

DATABASE = "sqlite:///*.db" - путь к вашей базе данных SQLite


Установка:
1. Устанавливаем Python 3.7
2. Подготавливаем папку для установки
3. Устанавливаем необходимые пакеты: pip install -r requirements.txt
4. Копируем код с GitHub: https://github.com/dumbturtle/botreminder
5. Настроить файл connect_settings.py
6. Создаем базу данных python database/create_db.py
7. Для старта системы необходимо запустить скрипт: ws.sh


## **Использование**
 Раздел в разработке.
