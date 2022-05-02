import requests
import telebot
import random
import psycopg2
from telebot import types

connect = psycopg2.connect(database='Sensors_db', user='postgres', password='Getmpad123', host='localhost', port='5432')
print("Database opened successfully")
cursor = connect.cursor()

bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=["start"])
def hello(m, res=False):
    user_id = m.from_user.id
    username = m.from_user.username
    bot.send_message(m.chat.id, f'\nЗдравствуйте, {username}! Для получения справки, введите /help')

    cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
    result = cursor.fetchone()

    if not result:
        cursor.execute("INSERT INTO users(id, username) VALUES (%s, %s)", (user_id, username))
        connect.commit()


@bot.message_handler(commands=["stop"])
def goodbay(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("/start")
    markup.add(item)
    bot.send_message(m.chat.id, '\nДосвидания! Если захотите вернуться к работе с БД, нажмите /start.',
                     reply_markup=markup)


@bot.message_handler(commands=["help"])
def help_(m, res=False):
    bot.send_message(m.chat.id,
                     'Данный бот предназначен для работы с БД по авиационным датчикам.\nЧтобы перейти к доступным вам действиям, введите /BD')


@bot.message_handler(commands=['BD'])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Датчики температуры")
    item2 = types.KeyboardButton("Датчики давления")
    item3 = types.KeyboardButton("Расходомеры")
    item4 = types.KeyboardButton("Датчики влажности")
    item5 = types.KeyboardButton("Детекторы присутствия")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    bot.send_message(m.chat.id,
                     "Нажмите \n\nДатчики температуры, для того, чтобы получить список доступных датчиков температуры.\n\nДатчики давления, для того, чтобы увидеть спсиок датчиков давления."
                     "\n\nРасходомеры, для того, чтобы увидеть спсиок датчиков давления. \n\nДатчики влажности, для того, чтобы увидеть спсиок датчиков давления.\n\nДетекторы присутствия, для того, чтобы увидеть спсиок датчиков давления.",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.strip() == 'Датчики температуры':
        cursor.execute("SELECT concat(id, ' ', name) FROM temp")
        answer = cursor.fetchall()
        my_list = []
        for x in answer:
            my_list.append(' | '.join(x))
        my_str = '\n'.join(my_list)
        bot.send_message(message.chat.id, my_str)
        send = bot.send_message(message.chat.id,
                                '\n Чтобы посмотреть информацию по конкретному датчику, введите его индекс')
        bot.register_next_step_handler(send, info_temp)
    elif message.text.strip() == 'Датчики давления':
        cursor.execute("SELECT concat(id, ' ', name) FROM davl")
        answer = cursor.fetchall()
        my_list = []
        for x in answer:
            my_list.append(' | '.join(x))
        my_str = '\n'.join(my_list)
        bot.send_message(message.chat.id, my_str)
        send = bot.send_message(message.chat.id,
                                '\n Чтобы посмотреть информацию по конкретному датчику, введите его индекс')
        bot.register_next_step_handler(send, info_davl)
    elif message.text.strip() == 'Расходомеры':
        cursor.execute("SELECT concat(id, ' ', name) FROM rashodomers")
        answer = cursor.fetchall()
        my_list = []
        for x in answer:
            my_list.append(' | '.join(x))
        my_str = '\n'.join(my_list)
        bot.send_message(message.chat.id, my_str)
        send = bot.send_message(message.chat.id,
                                '\n Чтобы посмотреть информацию по конкретному датчику, введите его индекс')
        bot.register_next_step_handler(send, info_rashod)
    elif message.text.strip() == 'Датчики влажности':
        cursor.execute("SELECT concat(id, ' ', name) FROM vlazh")
        answer = cursor.fetchall()
        my_list = []
        for x in answer:
            my_list.append(' | '.join(x))
        my_str = '\n'.join(my_list)
        bot.send_message(message.chat.id, my_str)
        send = bot.send_message(message.chat.id,
                                '\n Чтобы посмотреть информацию по конкретному датчику, введите его индекс')
        bot.register_next_step_handler(send, info_vlazh)
    elif message.text.strip() == 'Детекторы присутствия':
        cursor.execute("SELECT concat(id, ' ', name) FROM detectors_pris")
        answer = cursor.fetchall()
        my_list = []
        for x in answer:
            my_list.append(' | '.join(x))
        my_str = '\n'.join(my_list)
        bot.send_message(message.chat.id, my_str)
        send = bot.send_message(message.chat.id,
                                '\n Чтобы посмотреть информацию по конкретному датчику, введите его индекс')
        bot.register_next_step_handler(send, info_dp)
    elif message.text.strip() == '//Edit//':
        send = bot.send_message(message.chat.id,
                                'Введите пароль для того, чтобы получить возможность редактировать БД.')
        bot.register_next_step_handler(send, auth)


def auth(m):
    if m.text.strip() != 'Getmpad123':
        bot.send_message(m.chat.id, 'Пароль введен неверно! Доступ запрещен!')
    else:
        bot.send_message(m.chat.id,
                         'Успешно! Доступ к редактированию открыт! Выберите действие, которое хотите совершить.')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Edit")
        markup.add(item1)
        send = bot.send_message(m.chat.id, 'Нажмите на кнопку, чтобы начать редактирование.', reply_markup=markup)
        bot.register_next_step_handler(send, edit1)


def edit1(message):
    if message.text.strip() == "Edit":
        cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = 'public'")
        answer = cursor.fetchall()
        my_list = []
        for x in answer:
            my_list.append(' | '.join(x))
        my_str = '\n'.join(my_list)
        bot.send_message(message.chat.id, my_str)
        send = bot.send_message(message.chat.id,
                                '\n Выберите таблицу, которую хотите редактировать.')
        bot.register_next_step_handler(send, edit2)


def edit2(message):
    if message.text.strip() == 'davl':
        bot.send_message(message.chat.id, "Выберите действие, которое хотите совершить.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Добавить датчик")
        item2 = types.KeyboardButton("Изменить")
        markup.add(item1)
        markup.add(item2)
        send = bot.send_message(message.chat.id,
                                "Нажмите \n\nДобавить датчик, для того, чтобы добавить дачтик.\n\nИзменить, для того, чтобы отредактировать таблицу.",
                                reply_markup=markup)
        bot.register_next_step_handler(send, edit3)
    elif message.text.strip() == 'temp':
        bot.send_message(message.chat.id, "Выберите действие, которое хотите совершить.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Добавить датчик")
        item2 = types.KeyboardButton("Изменить")
        markup.add(item1)
        markup.add(item2)
        send = bot.send_message(message.chat.id,
                                "Нажмите \n\nДобавить датчик, для того, чтобы добавить дачтик.\n\nИзменить, для того, чтобы отредактировать таблицу.",
                                reply_markup=markup)
        bot.register_next_step_handler(send, edit3)
    elif message.text.strip() == 'literature':
        bot.send_message(message.chat.id, "Выберите действие, которое хотите совершить.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Добавить датчик")
        item2 = types.KeyboardButton("Изменить")
        markup.add(item1)
        markup.add(item2)
        send = bot.send_message(message.chat.id,
                                "Нажмите \n\nДобавить датчик, для того, чтобы добавить дачтик.\n\nИзменить, для того, чтобы отредактировать таблицу.",
                                reply_markup=markup)
        bot.register_next_step_handler(send, edit3)
    elif message.text.strip() == 'rashodomers':
        bot.send_message(message.chat.id, "Выберите действие, которое хотите совершить.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Добавить датчик")
        item2 = types.KeyboardButton("Изменить")
        markup.add(item1)
        markup.add(item2)
        send = bot.send_message(message.chat.id,
                                "Нажмите \n\nДобавить датчик, для того, чтобы добавить дачтик.\n\nИзменить, для того, чтобы отредактировать таблицу.",
                                reply_markup=markup)
        bot.register_next_step_handler(send, edit3)
    elif message.text.strip() == 'vlazh':
        bot.send_message(message.chat.id, "Выберите действие, которое хотите совершить.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Добавить датчик")
        item2 = types.KeyboardButton("Изменить")
        markup.add(item1)
        markup.add(item2)
        send = bot.send_message(message.chat.id,
                                "Нажмите \n\nДобавить датчик, для того, чтобы добавить дачтик.\n\nИзменить, для того, чтобы отредактировать таблицу.",
                                reply_markup=markup)
        bot.register_next_step_handler(send, edit3)
    elif message.text.strip() == 'detector_pris':
        bot.send_message(message.chat.id, "Выберите действие, которое хотите совершить.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Добавить датчик")
        item2 = types.KeyboardButton("Изменить")
        markup.add(item1)
        markup.add(item2)
        send = bot.send_message(message.chat.id,
                                "Нажмите \n\nДобавить датчик, для того, чтобы добавить дачтик.\n\nИзменить, для того, чтобы отредактировать таблицу.",
                                reply_markup=markup)
        bot.register_next_step_handler(send, edit3)
    elif message.text.strip() == 'users':
        bot.send_message(message.chat.id, "Выберите действие, которое хотите совершить.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Добавить датчик")
        item2 = types.KeyboardButton("Изменить")
        markup.add(item1)
        markup.add(item2)
        send = bot.send_message(message.chat.id,
                                "Нажмите \n\nДобавить датчик, для того, чтобы добавить дачтик.\n\nИзменить, для того, чтобы отредактировать таблицу.",
                                reply_markup=markup)
        bot.register_next_step_handler(send, edit3)


def edit3(m):
    if m.text.strip() == "Добавить датчик":
        send1 = bot.send_message(m.chat.id, "Введите название датчика")
        bot.register_next_step_handler(send1, add_name)
    elif m.text.strip() == "Изменить":
        send2 = bot.send_message(m.chat.id, "Напишите название столбца, который хотите изменить.")
        bot.register_next_step_handler(send2, editor)


def add_name(message):
    pass


def editor(message):
    pass


def info_temp(message):
    cursor.execute(f"SELECT description FROM temp WHERE id = {message.text}")
    answer1 = cursor.fetchall()
    my_list1 = []
    for x in answer1:
        my_list1.append(' | '.join(x))
    my_str1 = '\n'.join(my_list1)
    bot.send_message(message.chat.id, my_str1)
    send = bot.send_message(message.chat.id,
                            "\n Введите название датчика температуры, инфо о котором вы хотите узнать.")
    # bot.register_next_step_handler(send, )


def info_davl(message):
    cursor.execute(f"SELECT description FROM davl WHERE id = {message.text}")
    answer1 = cursor.fetchall()
    my_list1 = []
    for x in answer1:
        my_list1.append(' | '.join(x))
    my_str1 = '\n'.join(my_list1)
    bot.send_message(message.chat.id, my_str1)
    send = bot.send_message(message.chat.id, "\n Введите название датчика давления, инфо о котором вы хотите узнать.")


def info_rashod(message):
    cursor.execute(f"SELECT description FROM rashodomers WHERE id = {message.text}")
    answer1 = cursor.fetchall()
    my_list1 = []
    for x in answer1:
        my_list1.append(' | '.join(x))
    my_str1 = '\n'.join(my_list1)
    bot.send_message(message.chat.id, my_str1)
    send = bot.send_message(message.chat.id, "\n Введите название расходомера, инфо о котором вы хотите узнать.")


def info_vlazh(message):
    cursor.execute(f"SELECT description FROM vlazh WHERE id = {message.text}")
    answer1 = cursor.fetchall()
    my_list1 = []
    for x in answer1:
        my_list1.append(' | '.join(x))
    my_str1 = '\n'.join(my_list1)
    bot.send_message(message.chat.id, my_str1)
    send = bot.send_message(message.chat.id, "\n Введите название датчика влажности, инфо о котором вы хотите узнать.")


def info_dp(message):
    cursor.execute(f"SELECT description FROM detectors_pris WHERE id = {message.text}")
    answer1 = cursor.fetchall()
    my_list1 = []
    for x in answer1:
        my_list1.append(' | '.join(x))
    my_str1 = '\n'.join(my_list1)
    bot.send_message(message.chat.id, my_str1)
    send = bot.send_message(message.chat.id,
                            "\n Введите название детектора присутствия, инфо о котором вы хотите узнать.")


def info_davl_spis(message):
    cursor.execute(f"SELECT name FROM ")
    answer = cursor.fetchall()
    my_list = []
    for x in answer:
        my_list.append(' | '.join(x))
    my_str = '\n'.join(my_list)
    bot.send_message(message.chat.id, my_str)


bot.polling(none_stop=True, interval=0)
