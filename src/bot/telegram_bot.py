import telebot
import requests
from decouple import config
import json
import os
import base64

try:
    BOT_TOKEN = config('BOT_TOKEN')
    BASE_URL = config('BASE_URL')
except (ImportError, RuntimeError):
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    BASE_URL = os.environ.get('BASE_URL')

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


def t(chat_id, key_uz, key_ru):
    lang = user_language.get(chat_id, 'uz')
    return key_uz if lang == 'uz' else key_ru


def show_main_menu(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup.add(
        t(chat_id, 'Categoriya', 'Категории'),
        t(chat_id, '👤 Profil', '👤 Профиль'),
        t(chat_id, "🌐 Tilni o'zgartirish", "🌐 Сменить язык")
    )
    prompt = t(chat_id, "Bosh menyu", "Главное меню")
    bot.send_message(chat_id, prompt, reply_markup=markup)


def show_profile_menu(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    prompt = t(chat_id, "Profil", "Профиль")

    if chat_id in logged_in_users:
        markup.add(
            t(chat_id, '📄 Mening ma\'lumotlarim', '📄 Мои данные'),
            t(chat_id, '⬅️ Chiqish', '⬅️ Выход')
        )
        markup.add(t(chat_id, '⬅️ Bosh menyu', '⬅️ Главное меню'))
    else:
        markup.add(
            t(chat_id, '✅ Kirish', '✅ Вход'),
            t(chat_id, '📝 Ro‘yxatdan o‘tish', '📝 Регистрация'),
            t(chat_id, '🔑 Parolni unutdingizmi?', '🔑 Забыли пароль?')
        )
        markup.add(t(chat_id, '⬅️ Bosh menyu', '⬅️ Главное меню'))

    bot.send_message(chat_id, prompt, reply_markup=markup)


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    if chat_id in user_language:
        show_main_menu(chat_id)
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
    show_main_menu(chat_id)


@bot.message_handler(func=lambda msg: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    action = message.text

    if chat_id in user_conversation_data:
        user_conversation_data[chat_id] = {}

    if action in [t(chat_id, 'Categoriya', 'Категории')]:
        start_category_search(message)
    elif action in [t(chat_id, '👤 Profil', '👤 Профиль')]:
        show_profile_menu(chat_id)
    elif action in [t(chat_id, "🌐 Tilni o'zgartirish", "🌐 Сменить язык")]:
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('🇺🇿 O‘zbek', '🇷🇺 Русский')
        bot.send_message(chat_id, "Tilni tanlang / Выберите язык:", reply_markup=markup)
    elif action in [t(chat_id, '⬅️ Bosh menyu', '⬅️ Главное меню')]:
        show_main_menu(chat_id)
    elif action in [t(chat_id, '📄 Mening ma\'lumotlarim', '📄 Мои данные')]:
        if chat_id in logged_in_users:
            user_data = logged_in_users[chat_id]
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            email = user_data.get('email', 'N/A')

            data_message = (
                f"<b>{t(chat_id, 'Sizning maʼlumotlaringiz', 'Ваши данные')}:</b>\n\n"
                f"👤 <b>{t(chat_id, 'Ism, Familiya', 'Имя, Фамилия')}:</b> {first_name} {last_name}\n"
                f"📧 <b>Email:</b> {email}"
            )
            bot.send_message(chat_id, data_message, parse_mode='HTML')
        else:
            bot.send_message(chat_id, t(chat_id, "Siz tizimda emassiz.", "Вы не в системе."))
            show_main_menu(chat_id)
    elif action in [t(chat_id, '📝 Ro‘yxatdan o‘tish', '📝 Регистрация')]:
        prompt = t(chat_id, "Ismingizni kiriting:", "Введите ваше имя:")
        msg = bot.send_message(chat_id, prompt, reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_first_name_step)
    elif action in [t(chat_id, '✅ Kirish', '✅ Вход')]:
        prompt = t(chat_id, "Email manzilingizni kiriting:", "Введите ваш email:")
        msg = bot.send_message(chat_id, prompt, reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_login_email_step)
    elif action in [t(chat_id, '🔑 Parolni unutdingizmi?', '🔑 Забыли пароль?')]:
        prompt = t(chat_id, "Parolni tiklash uchun emailingizni kiriting:",
                   "Введите ваш email для восстановления пароля:")
        msg = bot.send_message(chat_id, prompt, reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_forgot_password_email_step)
    elif action in [t(chat_id, '⬅️ Chiqish', '⬅️ Выход')]:
        if chat_id in logged_in_users:
            del logged_in_users[chat_id]
        success_message = t(chat_id, "Siz tizimdan chiqdingiz.", "Вы вышли из системы.")
        bot.send_message(chat_id, f"✅ {success_message}")
        show_main_menu(chat_id)


def get_auth_headers(chat_id):
    if chat_id in logged_in_users and 'access' in logged_in_users[chat_id]:
        access_token = logged_in_users[chat_id]['access']
        return {'Authorization': f'Bearer {access_token}'}
    return {}


def start_category_search(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    try:
        headers = get_auth_headers(chat_id)
        url = f"{BASE_URL}/{lang}/api/category/"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            categories = response.json()
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            buttons = [telebot.types.InlineKeyboardButton(cat['name'], callback_data=f"cat_{cat['id']}") for cat in
                       categories]
            markup.add(*buttons)
            markup.add(telebot.types.InlineKeyboardButton(t(chat_id, "⬅️ Bosh menyu", "⬅️ Главное меню"),
                                                          callback_data="back_to_main"))
            bot.send_message(chat_id, t(chat_id, "Kategoriyani tanlang:", "Выберите категорию:"), reply_markup=markup)
        else:
            bot.send_message(chat_id,
                             t(chat_id, "Kategoriyalarni yuklashda xatolik.", "Ошибка при загрузке категорий."))
    except Exception as e:
        bot.send_message(chat_id, t(chat_id, "Xatolik yuz berdi.", "Произошла ошибка."))


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    chat_id = call.message.chat.id
    lang = user_language.get(chat_id, 'uz')
    data = call.data

    if data.startswith("cat_"):
        category_id = data.split('_')[1]
        user_conversation_data[chat_id] = {'category_id': category_id}
        bot.delete_message(chat_id, call.message.message_id)
        prompt = t(chat_id, "Joylashuvingizni yuboring.", "Отправьте вашу геолокацию.")
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        location_button_text = t(chat_id, "📍 Joylashuvni yuborish", "📍 Отправить геолокацию")
        cancel_button_text = t(chat_id, "❌ Bekor qilish", "❌ Отмена")
        markup.add(telebot.types.KeyboardButton(text=location_button_text, request_location=True),
                   telebot.types.KeyboardButton(text=cancel_button_text))
        msg = bot.send_message(chat_id, prompt, reply_markup=markup)
        bot.register_next_step_handler(msg, process_location_step)

    elif data.startswith("place_"):
        index = int(data.split('_')[1])
        show_paginated_place(chat_id, index, call.message.message_id)

    elif data == "back_to_main":
        bot.delete_message(chat_id, call.message.message_id)
        show_main_menu(chat_id)

    elif data == "back_to_main_from_place":
        bot.delete_message(chat_id, call.message.message_id)
        if chat_id in user_conversation_data:
            user_conversation_data[chat_id].pop('places', None)
            user_conversation_data[chat_id].pop('message_id', None)
        show_main_menu(chat_id)


@bot.message_handler(content_types=['location'])
def handle_location_for_search(message):
    process_location_step(message)


def log_search_activity(chat_id, category_id):
    if chat_id not in logged_in_users:
        return

    try:
        lang = user_language.get(chat_id, 'uz')
        headers = get_auth_headers(chat_id)
        url = f"{BASE_URL}/{lang}/api/search-history/"

        data = {
            'category': category_id
        }

        response = requests.post(url, json=data, headers=headers, timeout=5)
        if response.status_code not in [200, 201]:
            print(f"Warning: Failed to log search activity for user {chat_id}. Status: {response.status_code}")

    except Exception as e:
        print(f"Warning: Exception while logging search activity for user {chat_id}: {e}")


def process_location_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')

    if message.text and message.text in [t(chat_id, "❌ Bekor qilish", "❌ Отмена")]:
        show_main_menu(chat_id)
        return
    if not message.location:
        prompt = t(chat_id, "Iltimos, joylashuvingizni tugma orqali yuboring.",
                   "Пожалуйста, отправьте вашу геолокацию с помощью кнопки.")
        msg = bot.send_message(chat_id, prompt)
        bot.register_next_step_handler(msg, process_location_step)
        return

    try:
        lat = message.location.latitude
        lon = message.location.longitude
        category_id = user_conversation_data.get(chat_id, {}).get('category_id')

        if category_id:
            log_search_activity(chat_id, category_id)

        headers = get_auth_headers(chat_id)
        url = f"{BASE_URL}/{lang}/api/place/"
        params = {'latitude': lat, 'longitude': lon, 'category': category_id}

        searching_message = t(chat_id, "Qidirilmoqda...", "Идёт поиск...")
        bot.send_message(chat_id, searching_message, reply_markup=telebot.types.ReplyKeyboardRemove())

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            response_data = response.json()
            places = response_data.get('results', [])
            if not places:
                bot.send_message(chat_id, t(chat_id, "Hech narsa topilmadi.", "Ничего не найдено."))
                show_main_menu(chat_id)
            else:
                bot.send_message(chat_id, t(chat_id, "Qidiruv natijalari:", "Результаты поиска:"))
                user_conversation_data.setdefault(chat_id, {})['places'] = places
                show_paginated_place(chat_id, 0)
        else:
            bot.send_message(chat_id, t(chat_id, "Qidirishda xatolik yuz berdi.", "Произошла ошибка при поиске."))
            show_main_menu(chat_id)

    except Exception as e:
        bot.send_message(chat_id, f"❌ {t(chat_id, 'Xatolik yuz berdi.', 'Произошла ошибка.')}")
        show_main_menu(chat_id)


def show_paginated_place(chat_id, index, message_id=None):
    lang = user_language.get(chat_id, 'uz')
    places = user_conversation_data.get(chat_id, {}).get('places', [])
    if not places or not (0 <= index < len(places)):
        return

    place = places[index]
    name = place.get('name', t(chat_id, 'Nomsiz', 'Без названия'))
    description = place.get('description', '')
    distance = place.get('distance')
    image_url = place.get('image')
    place_location = place.get('location', {})
    place_lat = place_location.get('latitude')
    place_lon = place_location.get('longitude')

    caption = f"<b>{name}</b>\n\n"
    if description:
        caption += f"{description}\n\n"
    if distance is not None:
        caption += f"{t(chat_id, 'Masofa', 'Расстояние')}: {distance:.2f} km\n"

    markup = telebot.types.InlineKeyboardMarkup()
    row = []
    if index > 0:
        row.append(telebot.types.InlineKeyboardButton(t(chat_id, "⬅️ Oldingisi", "⬅️ Предыдущий"),
                                                      callback_data=f"place_{index - 1}"))
    row.append(telebot.types.InlineKeyboardButton(f"{index + 1}/{len(places)}", callback_data="no_action"))
    if index < len(places) - 1:
        row.append(telebot.types.InlineKeyboardButton(t(chat_id, "Keyingisi ➡️", "Следующий ➡️"),
                                                      callback_data=f"place_{index + 1}"))

    markup.row(*row)

    if place_lat and place_lon:
        map_link = f"https://maps.google.com/?q={place_lat},{place_lon}"
        map_button_text = t(chat_id, "📍 Xaritada ko'rish", "📍 Показать на карте")
        markup.add(telebot.types.InlineKeyboardButton(map_button_text, url=map_link))

    markup.add(telebot.types.InlineKeyboardButton(t(chat_id, "⬅️ Bosh menyu", "⬅️ Главное меню"),
                                                  callback_data="back_to_main_from_place"))

    try:
        if message_id:
            if image_url:
                media = telebot.types.InputMediaPhoto(media=image_url, caption=caption, parse_mode='HTML')
                bot.edit_message_media(chat_id=chat_id, message_id=message_id, media=media, reply_markup=markup)
            else:
                bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=caption, reply_markup=markup,
                                         parse_mode='HTML')
        else:
            if image_url:
                sent_message = bot.send_photo(chat_id, photo=image_url, caption=caption, parse_mode='HTML',
                                              reply_markup=markup)
            else:
                sent_message = bot.send_message(chat_id, caption, parse_mode='HTML', reply_markup=markup,
                                                disable_web_page_preview=True)
            user_conversation_data.setdefault(chat_id, {})['message_id'] = sent_message.message_id
    except Exception as e:
        if message_id: bot.delete_message(chat_id, message_id)
        if image_url:
            sent_message = bot.send_photo(chat_id, photo=image_url, caption=caption, parse_mode='HTML',
                                          reply_markup=markup)
        else:
            sent_message = bot.send_message(chat_id, caption, parse_mode='HTML', reply_markup=markup,
                                            disable_web_page_preview=True)
        user_conversation_data.setdefault(chat_id, {})['message_id'] = sent_message.message_id


def process_first_name_step(message):
    chat_id = message.chat.id
    user_conversation_data.setdefault(chat_id, {})['first_name'] = message.text
    prompt = t(chat_id, "Familyangizni kiriting:", "Введите вашу фамилию:")
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_last_name_step)


def process_last_name_step(message):
    chat_id = message.chat.id
    user_conversation_data[chat_id]['last_name'] = message.text
    prompt = t(chat_id, "Email manzilingizni kiriting:", "Введите ваш email:")
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_email_step)


def process_email_step(message):
    chat_id = message.chat.id
    user_conversation_data[chat_id]['email'] = message.text
    prompt = t(chat_id, "Parol yarating:", "Создайте пароль:")
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_password_step)


def process_password_step(message):
    chat_id = message.chat.id
    user_conversation_data[chat_id]['password'] = message.text
    prompt = t(chat_id, "Parolni tasdiqlang:", "Подтвердите пароль:")
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_password_confirm_step)


def process_password_confirm_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['password_confirm'] = message.text

    try:
        url = f"{BASE_URL}/{lang}/api/auth/register/"
        data = user_conversation_data.get(chat_id, {})
        bot.send_message(chat_id, t(chat_id, "Ma'lumotlar yuborilmoqda...", "Отправляем данные..."))
        response = requests.post(url, json=data)
        response_data = response.json()

        if response.status_code == 201:
            success_message = response_data.get('message', t(chat_id, "Muvaffaqiyatli ro'yxatdan o'tdingiz!",
                                                             "Вы успешно зарегистрировались!"))
            bot.send_message(chat_id, f"✅ {success_message}")
            prompt = t(chat_id, "Hisobingizni faollashtirish uchun emailingizga yuborilgan kodni kiriting:",
                       "Введите код из вашего письма для активации аккаунта:")
            msg = bot.send_message(chat_id, prompt)
            bot.register_next_step_handler(msg, process_confirmation_code_step)
        else:
            error_msg = response_data.get('email', [
                response_data.get('detail', t(chat_id, "Ro'yxatdan o'tishda xatolik.", "Ошибка при регистрации."))])[0]
            bot.send_message(chat_id, f"❌ {error_msg}")
            show_profile_menu(chat_id)
    except Exception as e:
        bot.send_message(chat_id, f"❌ {t(chat_id, 'Xatolik yuz berdi.', 'Произошла ошибка.')}")
        show_profile_menu(chat_id)
    finally:
        if chat_id in user_conversation_data: user_conversation_data.pop(chat_id, None)


def process_confirmation_code_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    confirmation_code = message.text
    try:
        url = f"{BASE_URL}/{lang}/api/auth/confirm/"
        response = requests.post(url, json={"code": confirmation_code})
        if response.status_code == 200:
            bot.send_message(chat_id, f"✅ {response.json().get('message')}")
            bot.send_message(chat_id, t(chat_id, "Iltimos, tizimga kiring.", "Пожалуйста, войдите в систему."))
            show_profile_menu(chat_id)
        else:
            bot.send_message(chat_id, f"❌ {response.json().get('error', t(chat_id, 'Kod xato.', 'Неверный код.'))}")
            show_profile_menu(chat_id)
    except Exception as e:
        bot.send_message(chat_id, f"❌ {t(chat_id, 'Xatolik yuz berdi.', 'Произошла ошибка.')}")
        show_profile_menu(chat_id)


def process_login_email_step(message):
    chat_id = message.chat.id
    user_conversation_data.setdefault(chat_id, {})['email'] = message.text
    prompt = t(chat_id, "Parolni kiriting:", "Введите пароль:")
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_login_password_step)


def process_login_password_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['password'] = message.text

    try:
        url_login = f"{BASE_URL}/{lang}/api/auth/login/"
        data = user_conversation_data.get(chat_id, {})
        response_login = requests.post(url_login, json=data)

        if response_login.status_code == 200:
            login_data = response_login.json()
            access_token = login_data.get('access')
            user_id = None

            try:
                payload_b64 = access_token.split('.')[1]
                payload_b64 += '=' * (-len(payload_b64) % 4)
                payload_json = base64.b64decode(payload_b64).decode('utf-8')
                payload_data = json.loads(payload_json)
                user_id = payload_data.get('user_id')

                if not user_id:
                    raise ValueError("user_id not found in token payload")

            except Exception:
                logged_in_users[chat_id] = {'access': access_token, 'refresh': login_data.get('refresh')}
                bot.send_message(chat_id, t(chat_id, "✅ Kirish muvaffaqiyatli, lekin profil yuklanmadi.",
                                            "✅ Вход успешен, но не удалось загрузить профиль."))
                show_main_menu(chat_id)
                return

            headers = {'Authorization': f'Bearer {access_token}'}
            url_user = f"{BASE_URL}/{lang}/api/auth/users-data/{user_id}/"
            response_user = requests.get(url_user, headers=headers)

            if response_user.status_code == 200:
                user_data = response_user.json()
                logged_in_users[chat_id] = {
                    'access': access_token,
                    'refresh': login_data.get('refresh'),
                    'email': user_data.get('email'),
                    'first_name': user_data.get('first_name'),
                    'last_name': user_data.get('last_name')
                }
                bot.send_message(chat_id, t(chat_id, "✅ Xush kelibsiz!", "✅ Добро пожаловать!"))
                show_main_menu(chat_id)
            else:
                logged_in_users[chat_id] = {'access': access_token, 'refresh': login_data.get('refresh')}
                bot.send_message(chat_id, t(chat_id, "✅ Kirish muvaffaqiyatli, lekin profil yuklanmadi.",
                                            "✅ Вход успешен, но не удалось загрузить профиль."))
                show_main_menu(chat_id)
        else:
            bot.send_message(chat_id, f"❌ {t(chat_id, 'Email yoki parol xato.', 'Неверный email или пароль.')}")
            show_profile_menu(chat_id)
    except Exception as e:
        bot.send_message(chat_id, f"❌ {t(chat_id, 'Xatolik yuz berdi.', 'Произошла ошибка.')}")
        show_profile_menu(chat_id)
    finally:
        if chat_id in user_conversation_data:
            user_conversation_data.pop(chat_id, None)


def process_forgot_password_email_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    email = message.text
    user_conversation_data[chat_id] = {'email': email}
    try:
        url = f"{BASE_URL}/{lang}/api/auth/forgot_password/"
        response = requests.post(url, json={'email': email})
        if response.status_code == 200:
            bot.send_message(chat_id, response.json().get('message'))
            prompt = t(chat_id, "Emailingizga yuborilgan kodni kiriting:", "Введите код из вашего письма:")
            msg = bot.send_message(chat_id, prompt)
            bot.register_next_step_handler(msg, process_restore_code_step)
        else:
            bot.send_message(chat_id, t(chat_id, "❌ Email topilmadi.", "❌ Email не найден."))
            show_profile_menu(chat_id)
    except Exception as e:
        bot.send_message(chat_id, f"❌ {t(chat_id, 'Xatolik yuz berdi.', 'Произошла ошибка.')}")
        show_profile_menu(chat_id)


def process_restore_code_step(message):
    chat_id = message.chat.id
    user_conversation_data[chat_id]['code'] = message.text
    prompt = t(chat_id, "Yangi parol yarating:", "Создайте новый пароль:")
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_restore_password_step)


def process_restore_password_step(message):
    chat_id = message.chat.id
    user_conversation_data[chat_id]['password'] = message.text
    prompt = t(chat_id, "Yangi parolni tasdiqlang:", "Подтвердите новый пароль:")
    msg = bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(msg, process_restore_password_confirm_step)


def process_restore_password_confirm_step(message):
    chat_id = message.chat.id
    lang = user_language.get(chat_id, 'uz')
    user_conversation_data[chat_id]['password_confirm'] = message.text
    try:
        url = f"{BASE_URL}/{lang}/api/auth/restore_password/"
        data = user_conversation_data.get(chat_id, {})
        response = requests.post(url, json=data)
        if response.status_code == 200:
            bot.send_message(chat_id,
                             t(chat_id, "✅ Parolingiz muvaffaqiyatli o'zgartirildi. Endi tizimga kirishingiz mumkin.",
                               "✅ Ваш пароль успешно изменен. Теперь вы можете войти в систему."))
            show_profile_menu(chat_id)
        else:
            bot.send_message(chat_id, f"❌ {response.json().get('error', t(chat_id, 'Xatolik', 'Ошибка'))}")
            show_profile_menu(chat_id)
    except Exception as e:
        bot.send_message(chat_id, f"❌ {t(chat_id, 'Xatolik yuz berdi.', 'Произошла ошибка.')}")
        show_profile_menu(chat_id)
    finally:
        if chat_id in user_conversation_data:
            del user_conversation_data[chat_id]
