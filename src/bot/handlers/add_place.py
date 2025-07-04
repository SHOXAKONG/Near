import json
import telebot
from ..models import TelegramProfile
from .. import utils, keyboards, api_client
from ..constants import UserSteps
from .start import show_main_menu


def start_add_place(message, bot):
    profile, _ = TelegramProfile.objects.get_or_create(tg_id=message.chat.id)
    if not profile.user or not profile.is_entrepreneur:
        bot.send_message(message.chat.id, utils.t(profile, "Bu funksiya faqat tasdiqlangan tadbirkorlar uchun.",
                                                  "Эта функция только для подтвержденных предпринимателей."))
        return

    prompt = utils.t(profile, "Yangi joy qo'shish boshlandi.\n\nJoy nomini kiriting (O'zbekcha):",
                     "Начато добавление нового места.\n\nВведите название места (Узбекский):")
    bot.send_message(message.chat.id, prompt)

    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_NAME_UZ
    profile.temp_data = {}
    profile.save()


def process_place_name_uz(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['name_uz'] = message.text
    prompt = utils.t(profile, "Joy nomini kiriting (Ruscha):", "Введите название места (Русский):")
    bot.send_message(message.chat.id, prompt)
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_NAME_RU
    profile.save()


def process_place_name_ru(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['name_ru'] = message.text

    response = api_client.get_categories(profile)
    if response and response.status_code == 200:
        categories = response.json()
        profile.temp_data['all_categories'] = categories
        markup = keyboards.get_category_keyboard(profile, categories)
        prompt = utils.t(profile, "Joy kategoriyasini tanlang:", "Выберите категорию места:")
        bot.send_message(message.chat.id, prompt, reply_markup=markup)
        profile.step = UserSteps.PLACE_ADD_WAITING_FOR_CATEGORY
        profile.save()
    else:
        bot.send_message(message.chat.id, utils.t(profile, "Kategoriyalarni yuklab bo'lmadi. Bosh menyu.",
                                                  "Не удалось загрузить категории. Главное меню."))
        show_main_menu(message, bot)


def process_place_category(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    category_name = message.text
    category_id = next(
        (cat['id'] for cat in profile.temp_data.get('all_categories', []) if cat['name'] == category_name), None)

    if not category_id:
        bot.send_message(message.chat.id, utils.t(profile, "Iltimos, pastdagi tugmalardan birini tanlang.",
                                                  "Пожалуйста, выберите одну из кнопок ниже."))
        return

    profile.temp_data['category'] = category_id
    profile.temp_data['category_name'] = category_name

    prompt = utils.t(profile, "Joylashuvni xaritadan belgilab yuboring:", "Отправьте геолокацию места:")
    markup = keyboards.get_location_request_keyboard(profile)
    bot.send_message(message.chat.id, prompt, reply_markup=markup)
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_LOCATION
    profile.save()


def process_place_location(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    if not message.location:
        bot.send_message(message.chat.id, utils.t(profile, "Iltimos, lokatsiyani tugma orqali yuboring.",
                                                  "Пожалуйста, отправьте геолокацию с помощью кнопки."))
        return

    profile.temp_data['latitude'] = message.location.latitude
    profile.temp_data['longitude'] = message.location.longitude
    prompt = utils.t(profile, "Bog'lanish uchun ma'lumot kiriting (telefon raqam):",
                     "Введите контактную информацию (номер телефона):")
    bot.send_message(message.chat.id, prompt, reply_markup=telebot.types.ReplyKeyboardRemove())
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_CONTACT
    profile.save()


def process_place_contact(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['contact'] = message.text
    prompt = utils.t(profile, "Joy haqida qisqacha tavsif yozing (O'zbekcha):",
                     "Напишите краткое описание места (Узбекский):")
    bot.send_message(message.chat.id, prompt)
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_DESCRIPTION_UZ
    profile.save()


def process_place_description_uz(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['description_uz'] = message.text
    prompt = utils.t(profile, "Joy haqida qisqacha tavsif yozing (Ruscha):",
                     "Напишите краткое описание места (Русский):")
    bot.send_message(message.chat.id, prompt)
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_DESCRIPTION_RU
    profile.save()


def process_place_description_ru(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['description_ru'] = message.text
    prompt = utils.t(profile, "Joyning asosiy rasmini yuboring:", "Отправьте главное фото места:")
    bot.send_message(message.chat.id, prompt)
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_IMAGE
    profile.save()


def process_place_image(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    if not message.photo:
        bot.send_message(message.chat.id,
                         utils.t(profile, "Iltimos, faqat rasm yuboring.", "Пожалуйста, отправьте только фото."))
        return

    profile.temp_data['image'] = message.photo[-1].file_id
    _show_confirmation_message(message, bot, profile)


def _show_confirmation_message(message, bot, profile):
    data = profile.temp_data
    confirmation_text = (
        f"<b>{utils.t(profile, 'Iltimos, ma\'lumotlarni tekshiring:', 'Пожалуйста, проверьте данные:')}</b>\n\n"
        f"<b>{utils.t(profile, 'Nomi (UZ)', 'Название (УЗ)')}:</b> {data.get('name_uz')}\n"
        f"<b>{utils.t(profile, 'Nomi (RU)', 'Название (РУ)')}:</b> {data.get('name_ru')}\n"
        f"<b>{utils.t(profile, 'Kategoriya', 'Категория')}:</b> {data.get('category_name')}\n"
        f"<b>{utils.t(profile, 'Lokatsiya', 'Локация')}:</b> Lat: {data.get('latitude')}, Lon: {data.get('longitude')}\n"
        f"<b>{utils.t(profile, 'Kontakt', 'Контакт')}:</b> {data.get('contact')}\n"
        f"<b>{utils.t(profile, 'Tavsif (UZ)', 'Описание (УЗ)')}:</b> {data.get('description_uz')}\n"
        f"<b>{utils.t(profile, 'Tavsif (RU)', 'Описание (РУ)')}:</b> {data.get('description_ru')}\n"
    )
    markup = keyboards.get_add_place_confirmation_keyboard(profile)
    bot.send_photo(message.chat.id, data['image'], caption=confirmation_text, reply_markup=markup, parse_mode='HTML')
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_CONFIRMATION
    profile.save()


def process_add_place_confirm(call, bot):
    profile = TelegramProfile.objects.get(tg_id=call.message.chat.id)
    if not profile.user:
        bot.answer_callback_query(call.id, "Xatolik: Foydalanuvchi topilmadi.", show_alert=True)
        return

    data_to_send = {
        "name": profile.temp_data.get("name_uz"), "name_uz": profile.temp_data.get("name_uz"),
        "name_ru": profile.temp_data.get("name_ru"),
        "description": profile.temp_data.get("description_uz"),
        "description_uz": profile.temp_data.get("description_uz"),
        "description_ru": profile.temp_data.get("description_ru"),
        "category": profile.temp_data.get("category"), "location": json.dumps(
            {"latitude": profile.temp_data.get("latitude"),
             "longitude": profile.temp_data.get("longitude")}) if profile.temp_data.get("latitude") else None,
        "contact": profile.temp_data.get("contact"), "image": profile.temp_data.get("image"), "user": profile.user.id
    }

    response = api_client.add_place(profile, data_to_send)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if response and response.status_code == 201:
        bot.send_message(call.message.chat.id,
                         f"✅ {utils.t(profile, 'Joy muvaffaqiyatli qo''shildi!', 'Место успешно добавлено!')}")
    else:
        error_details = "Noma'lum server xatoligi."
        if response is not None:
            try:
                error_data = response.json()
                formatted_errors = []
                for field, messages in error_data.items():
                    msg = messages[0] if isinstance(messages, list) else messages
                    formatted_errors.append(f"`{field}`: {msg}")
                error_details = "\n".join(formatted_errors)
            except:
                error_details = response.text
        bot.send_message(
            call.message.chat.id,
            f"❌ {utils.t(profile, 'Joy qo''shishda xatolik yuz berdi. Iltimos, ma''lumotlarni tekshiring', 'Произошла ошибка при добавлении места. Пожалуйста, проверьте данные')}:\n\n{error_details}",
            parse_mode="Markdown"
        )

    profile.temp_data = {}
    profile.step = UserSteps.DEFAULT
    profile.save()
    show_main_menu(call.message, bot)


def process_add_place_cancel(call, bot):
    profile = TelegramProfile.objects.get(tg_id=call.message.chat.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id,
                     f"❌ {utils.t(profile, 'Joy qo''shish bekor qilindi.', 'Добавление места отменено.')}")
    profile.temp_data = {}
    profile.step = UserSteps.DEFAULT
    profile.save()
    show_main_menu(call.message, bot)