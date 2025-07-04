import telebot
from . import utils


def get_language_selection_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🇺🇿 O‘zbek', '🇷🇺 Русский')
    markup.add('⬅️ Bosh menyu', '⬅️ Главное меню')
    return markup


def get_category_keyboard(profile, categories):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    for cat in categories:
        button = telebot.types.KeyboardButton(text=cat['name'])
        markup.add(button)
    back_button = telebot.types.KeyboardButton(text=utils.t(profile, '⬅️ Bosh menyu', '⬅️ Главное меню'))
    markup.add(back_button)

    return markup


def get_main_menu_keyboard(profile):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(
        utils.t(profile, 'Categoriya', 'Категории'),
        utils.t(profile, '👤 Profil', '👤 Профиль')
    )

    markup.add(
        utils.t(profile, '➕ Joy qo\'shish', '➕ Добавить место')
    )

    markup.add(
        utils.t(profile, "🌐 Tilni o'zgartirish", "🌐 Сменить язык"),
        utils.t(profile, "ℹ️ Bot haqida", "ℹ️ О боте")
    )
    return markup


def get_profile_menu_keyboard(profile):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    is_logged_in = bool(profile.user)

    if is_logged_in:
        markup.add(
            utils.t(profile, '📄 Mening ma\'lumotlarim', '📄 Мои данные'),
            utils.t(profile, '⬅️ Chiqish', '⬅️ Выход')
        )

        if not profile.is_entrepreneur:
            markup.add(
                utils.t(profile, '💼 Tadbirkor bo\'lish', '💼 Стать предпринимателем')
            )

    else:
        markup.add(
            utils.t(profile, '✅ Kirish', '✅ Вход'),
            utils.t(profile, '📝 Ro‘yxatdan o‘tish', '📝 Регистрация'),
            utils.t(profile, '🔑 Parolni unutdingizmi?', '🔑 Забыли пароль?')
        )

    markup.add(utils.t(profile, '⬅️ Bosh menyu', '⬅️ Главное меню'))
    return markup

def get_location_request_keyboard(profile):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    location_button_text = utils.t(profile, "📍 Joylashuvni yuborish", "📍 Отправить геолокацию")
    cancel_button_text = utils.t(profile, "❌ Bekor qilish", "❌ Отмена")
    markup.add(
        telebot.types.KeyboardButton(text=location_button_text, request_location=True),
        telebot.types.KeyboardButton(text=cancel_button_text)
    )
    return markup


def get_place_pagination_keyboard(profile, index, total_places, place):
    markup = telebot.types.InlineKeyboardMarkup()
    pagination_row = []
    if index > 0:
        pagination_row.append(telebot.types.InlineKeyboardButton(utils.t(profile, "⬅️ Oldingisi", "⬅️ Предыдущий"),
                                                                 callback_data=f"place_{index - 1}"))
    pagination_row.append(telebot.types.InlineKeyboardButton(f"{index + 1}/{total_places}", callback_data="no_action"))
    if index < total_places - 1:
        pagination_row.append(telebot.types.InlineKeyboardButton(utils.t(profile, "Keyingisi ➡️", "Следующий ➡️"),
                                                                 callback_data=f"place_{index + 1}"))
    markup.row(*pagination_row)

    place_location = place.get('location', {})
    if place_location.get('latitude') and place_location.get('longitude'):
        map_link = f"https://maps.google.com/maps?q={place_location['latitude']},{place_location['longitude']}"
        map_button_text = utils.t(profile, "📍 Xaritada ko'rish", "📍 Показать на карте")
        markup.add(telebot.types.InlineKeyboardButton(map_button_text, url=map_link))

    categories_button_text = utils.t(profile, "🔄 Kategoriyalar", "🔄 Категории")
    markup.add(telebot.types.InlineKeyboardButton(categories_button_text, callback_data="reshow_categories"))

    return markup

def get_add_place_confirmation_keyboard(profile):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    confirm_button = telebot.types.InlineKeyboardButton(
        text=f"✅ {utils.t(profile, 'Tasdiqlash', 'Подтвердить')}",
        callback_data="add_place_confirm"
    )
    cancel_button = telebot.types.InlineKeyboardButton(
        text=f"❌ {utils.t(profile, 'Bekor qilish', 'Отмена')}",
        callback_data="add_place_cancel"
    )
    markup.add(confirm_button, cancel_button)
    return markup