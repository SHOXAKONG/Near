import telebot
import requests
from decouple import config
import json
import os

BOT_TOKEN = config('BOT_TOKEN')
BASE_URL = config('BASE_URL')

LANGUAGE_FILE = 'user_languages.json'

bot = telebot.TeleBot(BOT_TOKEN)

def save_languages(data):
    with open(LANGUAGE_FILE, 'w') as f:
        json.dump(data, f)


def load_languages():
    if not os.path.exists(LANGUAGE_FILE):
        return {}
    try:
        with open(LANGUAGE_FILE, 'r') as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

user_conversation_data = {}
user_language = load_languages()
logged_in_users = {}


def show_main_menu(chat_id, lang):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    if chat_id in logged_in_users:
        if lang == 'uz':
            markup.add('🔍 Joy qidirish', '⬅️ Chiqish', "🌐 Tilni o'zgartirish")
        else:
            markup.add('🔍 Поиск места', '⬅️ Выход', "🌐 Сменить язык")
        prompt = "Menyu" if lang == 'uz' else "Меню"
    else:
        if lang == 'uz':
            markup.add('📝 Ro‘yxatdan o‘tish', '✅ Kirish', '🔑 Parolni unutdingizmi?', "🌐 Tilni o'zgartirish")
        else:
            markup.add('📝 Регистрация', '✅ Вход', '🔑 Забыли пароль?', "🌐 Сменить язык")
        prompt = "Nimani xohlaysiz?" if lang == 'uz' else "Что вы хотите сделать?"
    bot.send_message(chat_id, prompt, reply_markup=markup)

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    if chat_id in user_language:
        lang = user_language[chat_id]
        show_main_menu(chat_id, lang)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('🇺🇿 O‘zbek', '🇷🇺 Русский')
        bot.send_message(chat_id, "Tilni tanlang / Выберите язык:", reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text in ['🇺🇿 O‘zbek', '🇷🇺 Русский'])
def select_language(message):
    chat_id = message.chat.id
    lang = 'uz' if 'O‘zbek' in message.text else 'ru'
    user_language[chat_id] = lang
    save_languages(user_language)
    bot.send_message(chat_id, "✅ Til tanlandi!" if lang == 'uz' else "✅ Язык выбран!")
    show_main_menu(chat_id, lang)


@bot.message_handler(func=lambda msg: msg.text in [
    '📝 Ro‘yxatdan o‘tish', '📝 Регистрация', '✅ Kirish', '✅ Вход',
    '🔑 Parolni unutdingizmi?', '🔑 Забыли пароль?', '⬅️ Chiqish', '⬅️ Выход',
    '🔍 Joy qidirish', '🔍 Поиск места', "🌐 Tilni o'zgartirish", "🌐 Сменить язык"
])
def handle_main_menu_actions(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id] = {}
    action = message.text

    if 'Ro‘yxatdan' in action or 'Регистрация' in action:
        prompt = "Ismingizni kiriting:" if lang == 'uz' else "Введите ваше имя:"
        msg = bot.send_message(chat_id, prompt)
        bot.register_next_step_handler(msg, process_first_name_step)
    elif 'Kirish' in action or 'Вход' in action:
        prompt = "Email manzilingizni kiriting:" if lang == 'uz' else "Введите ваш email:"
        msg = bot.send_message(chat_id, prompt)
        bot.register_next_step_handler(msg, process_login_email_step)
    elif 'Parolni unutdingizmi?' in action or 'Забыли пароль?' in action:
        prompt = "Parolni tiklash uchun emailingizni kiriting:" if lang == 'uz' else "Введите ваш email для восстановления пароля:"
        msg = bot.send_message(chat_id, prompt)
        bot.register_next_step_handler(msg, process_forgot_password_email_step)
    elif 'Chiqish' in action or 'Выход' in action:
        if chat_id in logged_in_users:
            del logged_in_users[chat_id]
        success_message = "Siz tizimdan chiqdingiz." if lang == 'uz' else "Вы вышли из системы."
        bot.send_message(chat_id, f"✅ {success_message}")
        show_main_menu(chat_id, lang)
    elif "Tilni o'zgartirish" in action or "Сменить язык" in action:
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('🇺🇿 O‘zbek', '🇷🇺 Русский')
        bot.send_message(chat_id, "Tilni tanlang / Выберите язык:", reply_markup=markup)
    elif 'Joy qidirish' in action or 'Поиск места' in action:
        if chat_id not in logged_in_users:
            bot.send_message(chat_id,
                             "Bu funksiyadan foydalanish uchun tizimga kiring." if lang == 'uz' else "Пожалуйста, войдите в систему, чтобы использовать эту функцию.")
            return
        start_category_search(message)


def start_category_search(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    try:
        access_token = logged_in_users[chat_id].get('access')
        headers = {'Authorization': f'Bearer {access_token}'}
        url = f"{BASE_URL}/{lang}/api/category/"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            categories = response.json()
            markup = telebot.types.InlineKeyboardMarkup()
            buttons = [telebot.types.InlineKeyboardButton(cat['name'], callback_data=f"cat_{cat['id']}") for cat in
                       categories]
            markup.add(*buttons)
            markup.add(telebot.types.InlineKeyboardButton("⬅️ Bosh menyu" if lang == 'uz' else "⬅️ Главное меню",
                                                          callback_data="back_to_main"))
            bot.send_message(chat_id, "Kategoriyani tanlang:" if lang == 'uz' else "Выберите категорию:",
                             reply_markup=markup)
        else:
            bot.send_message(chat_id,
                             "Kategoriyalarni yuklashda xatolik." if lang == 'uz' else "Ошибка при загрузке категорий.")
    except Exception as e:
        print(e)
        bot.send_message(chat_id, "Xatolik yuz berdi." if lang == 'uz' else "Произошла ошибка.")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    chat_id = call.message.chat.id
    lang = user_language.get(chat_id, 'uz')
    data = call.data

    if data.startswith("place_"):
        index = int(data.split('_')[1])
        show_paginated_place(chat_id, index, call.message.message_id)

    elif data == "back_to_main_from_place":
        bot.delete_message(chat_id, call.message.message_id)
        if chat_id in user_conversation_data:
            if 'places' in user_conversation_data.get(chat_id, {}):
                del user_conversation_data[chat_id]['places']
            if 'message_id' in user_conversation_data.get(chat_id, {}):
                del user_conversation_data[chat_id]['message_id']
        show_main_menu(chat_id, lang)

    elif data == "back_to_main":
        bot.delete_message(chat_id, call.message.message_id)
        show_main_menu(chat_id, lang)
    elif data == "back_to_cat_list":
        bot.delete_message(chat_id, call.message.message_id)
        start_category_search(call.message)
    elif data.startswith("cat_"):
        category_id = data.split('_')[1]
        user_conversation_data[chat_id] = {'category_id': category_id}
        try:
            access_token = logged_in_users[chat_id].get('access')
            headers = {'Authorization': f'Bearer {access_token}'}
            url = f"{BASE_URL}/{lang}/api/subcategory/?category={category_id}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                subcategories = response.json()
                markup = telebot.types.InlineKeyboardMarkup()
                buttons = [telebot.types.InlineKeyboardButton(scat['name'], callback_data=f"subcat_{scat['id']}") for
                           scat in subcategories]
                markup.add(*buttons)
                markup.add(telebot.types.InlineKeyboardButton("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
                                                              callback_data="back_to_cat_list"))
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                      text="Bo'limni tanlang:" if lang == 'uz' else "Выберите подкатегорию:",
                                      reply_markup=markup)
            else:
                bot.answer_callback_query(call.id,
                                          "Bo'limlarni yuklashda xatolik." if lang == 'uz' else "Ошибка при загрузке подкатегорий.")
        except Exception as e:
            print(e)
            bot.answer_callback_query(call.id, "Xatolik." if lang == 'uz' else "Ошибка.")
    elif data.startswith("subcat_"):
        subcategory_id = data.split('_')[1]
        user_conversation_data[chat_id]['subcategory_id'] = subcategory_id
        bot.delete_message(chat_id, call.message.message_id)
        prompt = "Joylashuvingizni yuboring." if lang == 'uz' else "Отправьте вашу геолокацию."
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        location_button_text = "📍 Joylashuvni yuborish" if lang == 'uz' else "📍 Отправить геолокацию"
        cancel_button_text = "❌ Bekor qilish" if lang == 'uz' else "❌ Отмена"
        markup.add(telebot.types.KeyboardButton(text=location_button_text, request_location=True),
                   telebot.types.KeyboardButton(text=cancel_button_text))
        msg = bot.send_message(chat_id, prompt, reply_markup=markup)
        bot.register_next_step_handler(msg, process_final_search_step)


@bot.message_handler(content_types=['location'])
def handle_location_for_search(message):
    process_final_search_step(message)


def process_final_search_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')

    if hasattr(message, 'text') and message.text in ["❌ Bekor qilish", "❌ Отмена"]:
        show_main_menu(chat_id, lang)
        return
    if not hasattr(message, 'location') or not message.location:
        prompt = "Iltimos, joylashuvingizni tugma orqali yuboring." if lang == 'uz' else "Пожалуйста, отправьте вашу геолокацию с помощью кнопки."
        msg = bot.send_message(chat_id, prompt)
        bot.register_next_step_handler(msg, process_final_search_step)
        return

    try:
        lat = message.location.latitude
        lon = message.location.longitude
        category_id = user_conversation_data[chat_id].get('category_id')
        subcategory_id = user_conversation_data[chat_id].get('subcategory_id')
        access_token = logged_in_users[chat_id].get('access')
        headers = {'Authorization': f'Bearer {access_token}'}
        prefix = f"{BASE_URL}/{lang}/api"
        url = f"{prefix}/place/"
        params = {'latitude': lat, 'longitude': lon, 'category': category_id, 'subcategory': subcategory_id}

        response = requests.get(url, headers=headers, params=params)

        searching_message = "Qidirilmoqda..." if lang == 'uz' else "Идёт поиск..."
        bot.send_message(chat_id, searching_message, reply_markup=telebot.types.ReplyKeyboardRemove())

        if response.status_code == 200:
            response_data = response.json()
            places = response_data.get('results', [])
            if not places:
                bot.send_message(chat_id, "Hech narsa topilmadi." if lang == 'uz' else "Ничего не найдено.")
                show_main_menu(chat_id, lang)
            else:
                results_header = "Qidiruv natijalari:" if lang == 'uz' else "Результаты поиска:"
                bot.send_message(chat_id, results_header)
                user_conversation_data[chat_id]['places'] = places
                show_paginated_place(chat_id, 0)
        else:
            bot.send_message(chat_id,
                             "Qidirishda xatolik yuz berdi." if lang == 'uz' else "Произошла ошибка при поиске.")
            show_main_menu(chat_id, lang)

    except Exception as e:
        error_text = "Xatolik yuz berdi." if lang == 'uz' else "Произошла ошибка."
        bot.send_message(chat_id, f"❌ {error_text}")
        print(f"An error occurred in final search: {e}")
        show_main_menu(chat_id, lang)


def show_paginated_place(chat_id, index, message_id=None):
    lang = user_language.get(chat_id, 'uz')
    places = user_conversation_data.get(chat_id, {}).get('places', [])
    if not places or index < 0 or index >= len(places):
        return

    place = places[index]
    name = place.get('name', 'Nomsiz')
    description = place.get('description', '')
    distance = place.get('distance')
    image_url = place.get('image')
    place_location = place.get('location', {})
    place_lat = place_location.get('latitude')
    place_lon = place_location.get('longitude')

    caption = f"<b>{name}</b>\n\n"
    if description:
        caption += f"{description}\n\n"
    if distance:
        caption += f"Masofa: {distance:.2f} km\n" if lang == 'uz' else f"Расстояние: {distance:.2f} км\n"
    if place_lat and place_lon:
        map_link = f"https://maps.google.com/?q={place_lat},{place_lon}"
        link_text = "Xaritada ko'rish" if lang == 'uz' else "Показать на карте"
        caption += f'<a href="{map_link}">{link_text}</a>'

    markup = telebot.types.InlineKeyboardMarkup()
    row = []
    if index > 0:
        row.append(telebot.types.InlineKeyboardButton("⬅️ Oldingisi" if lang == 'uz' else "⬅️ Предыдущий",
                                                      callback_data=f"place_{index - 1}"))

    row.append(telebot.types.InlineKeyboardButton(f"{index + 1}/{len(places)}", callback_data="no_action"))

    if index < len(places) - 1:
        row.append(telebot.types.InlineKeyboardButton("Keyingisi ➡️" if lang == 'uz' else "Следующий ➡️",
                                                      callback_data=f"place_{index + 1}"))

    markup.row(*row)
    markup.add(telebot.types.InlineKeyboardButton("⬅️ Bosh menyu" if lang == 'uz' else "⬅️ Главное меню",
                                                  callback_data="back_to_main_from_place"))

    try:
        if message_id:
            if image_url:
                media = telebot.types.InputMediaPhoto(media=image_url, caption=caption, parse_mode='HTML')
                bot.edit_message_media(chat_id=chat_id, message_id=message_id, media=media, reply_markup=markup)
            else:  # If there is no image, edit the text and markup
                bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=caption, reply_markup=markup,
                                         parse_mode='HTML')

        else:
            if image_url:
                sent_message = bot.send_photo(chat_id, photo=image_url, caption=caption, parse_mode='HTML',
                                              reply_markup=markup)
            else:
                sent_message = bot.send_message(chat_id, caption, parse_mode='HTML', reply_markup=markup,
                                                disable_web_page_preview=True)
            user_conversation_data[chat_id]['message_id'] = sent_message.message_id
    except Exception as e:
        print(f"Error showing paginated place: {e}")
        if message_id:
            bot.delete_message(chat_id, message_id)
        if image_url:
            sent_message = bot.send_photo(chat_id, photo=image_url, caption=caption, parse_mode='HTML',
                                          reply_markup=markup)
        else:
            sent_message = bot.send_message(chat_id, caption, parse_mode='HTML', reply_markup=markup,
                                            disable_web_page_preview=True)
        user_conversation_data[chat_id]['message_id'] = sent_message.message_id


def process_first_name_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['first_name'] = message.text
    prompt = "Familyangizni kiriting:" if lang == 'uz' else "Введите вашу фамилию:"
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_last_name_step)


def process_last_name_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['last_name'] = message.text
    prompt = "Email manzilingizni kiriting:" if lang == 'uz' else "Введите ваш email:"
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_email_step)


def process_email_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['email'] = message.text
    prompt = "Parol yarating:" if lang == 'uz' else "Создайте пароль:"
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_password_step)


def process_password_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['password'] = message.text
    prompt = "Parolni tasdiqlang:" if lang == 'uz' else "Подтвердите пароль:"
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_password_confirm_step)


def process_password_confirm_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['password_confirm'] = message.text
    try:
        prefix = f"{BASE_URL}/{lang}/api/auth"
        url = f"{prefix}/register/"
        data = user_conversation_data[chat_id]
        processing_message = "Ma'lumotlar yuborilmoqda..." if lang == 'uz' else "Отправляем данные..."
        bot.send_message(chat_id, processing_message)
        response = requests.post(url, json=data)
        response_data = response.json()
        if response.status_code == 201:
            success_message = response_data.get('message', "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
            bot.send_message(chat_id, f"✅ {success_message}")
            prompt = "Hisobingizni faollashtirish uchun emailingizga yuborilgan kodni kiriting:" if lang == 'uz' else "Введите код из вашего письма для активации аккаунта:"
            msg = bot.send_message(chat_id, prompt)
            bot.register_next_step_handler(msg, process_confirmation_code_step)
        else:
            error_message = response_data.get('email', [response_data.get('detail', "Ro'yxatdan o'tishda xatolik.")])[0]
            bot.send_message(chat_id, f"❌ {error_message}")
    except Exception as e:
        error_text = "Xatolik yuz berdi." if lang == 'uz' else "Произошла ошибка."
        bot.send_message(chat_id, f"❌ {error_text}")
    finally:
        if chat_id in user_conversation_data:
            del user_conversation_data[chat_id]


def process_confirmation_code_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    confirmation_code = message.text
    try:
        prefix = f"{BASE_URL}/{lang}/api/auth"
        url = f"{prefix}/confirm/"
        data = {"code": confirmation_code}
        response = requests.post(url, json=data)
        response_data = response.json()
        if response.status_code == 200:
            success_message = response_data.get('message', "Hisobingiz faollashtirildi!")
            bot.send_message(chat_id, f"✅ {success_message}")
            prompt = "Iltimos, tizimga kiring." if lang == 'uz' else "Пожалуйста, войдите в систему."
            bot.send_message(chat_id, prompt)
            show_main_menu(chat_id, lang)
        else:
            error_message = response_data.get('error', "Kod xato.")
            bot.send_message(chat_id, f"❌ {error_message}")
    except Exception as e:
        error_text = "Xatolik yuz berdi." if lang == 'uz' else "Произошла ошибка."
        bot.send_message(chat_id, f"❌ {error_text}")


def process_login_email_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id] = {'email': message.text}
    prompt = "Parolni kiriting:" if lang == 'uz' else "Введите пароль:"
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_login_password_step)


def process_login_password_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['password'] = message.text
    try:
        prefix = f"{BASE_URL}/{lang}/api/auth"
        url = f"{prefix}/login/"
        data = user_conversation_data[chat_id]
        response = requests.post(url, json=data)
        response_data = response.json()
        if response.status_code == 200:
            logged_in_users[chat_id] = {'access': response_data.get('access'), 'refresh': response_data.get('refresh')}
            bot.send_message(chat_id, "✅ Xush kelibsiz!" if lang == 'uz' else "✅ Добро пожаловать!")
            show_main_menu(chat_id, lang)
        else:
            bot.send_message(chat_id, "❌ Email yoki parol xato." if lang == 'uz' else "❌ Неверный email или пароль.")
            show_main_menu(chat_id, lang)
    except Exception as e:
        error_text = "Xatolik yuz berdi." if lang == 'uz' else "Произошла ошибка."
        bot.send_message(chat_id, f"❌ {error_text}")
    finally:
        if chat_id in user_conversation_data:
            del user_conversation_data[chat_id]


def process_forgot_password_email_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    email = message.text
    user_conversation_data[chat_id] = {'email': email}
    try:
        prefix = f"{BASE_URL}/{lang}/api/auth"
        url = f"{prefix}/forgot_password/"
        response = requests.post(url, json={'email': email})
        if response.status_code == 200:
            bot.send_message(chat_id, response.json().get('message'))
            prompt = "Emailingizga yuborilgan kodni kiriting:" if lang == 'uz' else "Введите код из вашего письма:"
            msg = bot.send_message(chat_id, prompt)
            bot.register_next_step_handler(msg, process_restore_code_step)
        else:
            bot.send_message(chat_id, "❌ Email topilmadi." if lang == 'uz' else "❌ Email не найден.")
    except Exception as e:
        error_text = "Xatolik yuz berdi." if lang == 'uz' else "Произошла ошибка."
        bot.send_message(chat_id, f"❌ {error_text}")


def process_restore_code_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['code'] = message.text
    prompt = "Yangi parol yarating:" if lang == 'uz' else "Создайте новый пароль:"
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_restore_password_step)


def process_restore_password_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['password'] = message.text
    prompt = "Yangi parolni tasdiqlang:" if lang == 'uz' else "Подтвердите новый пароль:"
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_restore_password_confirm_step)


def process_restore_password_confirm_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['password_confirm'] = message.text
    try:
        prefix = f"{BASE_URL}/{lang}/api/auth"
        url = f"{prefix}/restore_password/"
        data = user_conversation_data[chat_id]
        response = requests.post(url, json=data)
        if response.status_code == 200:
            bot.send_message(chat_id, "✅ Parolingiz muvaffaqiyatli o'zgartirildi. Endi tizimga kirishingiz mumkin.")
            show_main_menu(chat_id, lang)
        else:
            bot.send_message(chat_id, f"❌ {response.json().get('error', 'Xatolik')}")
    except Exception as e:
        error_text = "Xatolik yuz berdi." if lang == 'uz' else "Произошла ошибка."
        bot.send_message(chat_id, f"❌ {error_text}")
    finally:
        if chat_id in user_conversation_data:
            del user_conversation_data[chat_id]
