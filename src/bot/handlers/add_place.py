import json
import telebot
from ..models import TelegramProfile
from .. import utils, keyboards, api_client
from ..constants import UserSteps
from .start import show_main_menu


def start_add_place(message, bot):
    profile, _ = TelegramProfile.objects.get_or_create(tg_id=message.chat.id)

    if not profile.user:
        bot.send_message(message.chat.id, utils.t(profile, "Bu amal uchun avval tizimga kiring.",
                                                  "Для этого действия необходимо войти в систему."))
        return

    bot.send_message(message.chat.id, utils.t(profile, "Statusingiz tekshirilmoqda...", "Проверяем ваш статус..."))
    response = api_client.get_user_data_from_api(profile)

    if not (response and response.status_code == 200):
        bot.send_message(message.chat.id,
                         utils.t(profile, "Foydalanuvchi ma'lumotlarini tekshirishda xatolik yuz berdi.",
                                 "Произошла ошибка при проверке данных пользователя."))
        return

    api_data = response.json()
    user_role = api_data.get('role', 'user')

    if user_role.lower() == 'entrepreneur':
        bot.send_message(message.chat.id, utils.t(profile, "Siz tadbirkorsiz. Yangi joy qo'shish boshlandi.",
                                                  "Вы предприниматель. Начато добавление нового места."))
        _begin_add_place_flow(message, bot, profile)

    elif user_role.lower() == 'user':
        bot.send_message(message.chat.id,
                         utils.t(profile, "Sizning statusingizni tadbirkorga o'zgartirish uchun so'rov yuborilmoqda...",
                                 "Отправляется запрос на изменение вашего статуса на предпринимателя..."))
        be_response = api_client.become_entrepreneur(profile)

        if be_response and be_response.status_code == 200:
            profile.is_entrepreneur = True
            profile.save(update_fields=['is_entrepreneur'])

            success_text = utils.t(profile,
                                   "Tabriklaymiz, sizning statusingiz tadbirkorga o'zgartirildi! Endi joy qo'shishingiz mumkin.",
                                   "Поздравляем, ваш статус изменен на предпринимателя! Теперь вы можете добавить место.")
            bot.send_message(message.chat.id, f"✅ {success_text}")
            _begin_add_place_flow(message, bot, profile)
        else:
            # Agar tadbirkor qilishda xatolik bo'lsa
            error_text = utils.t(profile, "Sizni tadbirkorga o'tkazishda xatolik yuz berdi.",
                                 "Произошла ошибка при смене вашего статуса на предпринимателя.")
            bot.send_message(message.chat.id, f"❌ {error_text}")
    else:
        bot.send_message(message.chat.id, utils.t(profile, "Sizning rolingiz joy qo'shishga ruxsat bermaydi.",
                                                  "Ваша роль не позволяет добавлять места."))


def _begin_add_place_flow(message, bot, profile):
    prompt = utils.t(profile, "Joy nomini kiriting (O'zbekcha):", "Введите название места (Узбекский):")
    bot.send_message(message.chat.id, prompt)

    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_NAME_UZ
    profile.temp_data = {}
    profile.save()

def process_place_name_uz(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['name_uz'] = message.text
    bot.send_message(message.chat.id, "Joy nomini kiriting (Ruscha):")
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
        bot.send_message(message.chat.id, "Joy kategoriyasini tanlang:", reply_markup=markup)
        profile.step = UserSteps.PLACE_ADD_WAITING_FOR_CATEGORY
        profile.save()
    else:
        bot.send_message(message.chat.id, "Kategoriyalarni yuklab bo'lmadi. Bosh menyu.")
        show_main_menu(message, bot)


def process_place_category(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    category_name = message.text
    category_id = next(
        (cat['id'] for cat in profile.temp_data.get('all_categories', []) if cat['name'] == category_name), None)

    if not category_id:
        bot.send_message(message.chat.id, "Iltimos, pastdagi tugmalardan birini tanlang.")
        return

    profile.temp_data['category'] = category_id
    profile.temp_data['category_name'] = category_name

    prompt = "Joylashuvni xaritadan belgilab yuboring:"
    markup = keyboards.get_location_request_keyboard(profile)
    bot.send_message(message.chat.id, prompt, reply_markup=markup)
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_LOCATION
    profile.save()


def process_place_location(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    if not message.location:
        bot.send_message(message.chat.id, "Iltimos, lokatsiyani tugma orqali yuboring.")
        return

    profile.temp_data['latitude'] = message.location.latitude
    profile.temp_data['longitude'] = message.location.longitude

    bot.send_message(message.chat.id, "Bog'lanish uchun ma'lumot kiriting (telefon raqam):",
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_CONTACT
    profile.save()


def process_place_contact(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['contact'] = message.text
    bot.send_message(message.chat.id, "Joy haqida qisqacha tavsif yozing (O'zbekcha):")
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_DESCRIPTION_UZ
    profile.save()


def process_place_description_uz(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['description_uz'] = message.text
    bot.send_message(message.chat.id, "Joy haqida qisqacha tavsif yozing (Ruscha):")
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_DESCRIPTION_RU
    profile.save()


def process_place_description_ru(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['description_ru'] = message.text
    bot.send_message(message.chat.id, "Joyning asosiy rasmini yuboring:")
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_IMAGE
    profile.save()


def process_place_image(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    if not message.photo:
        bot.send_message(message.chat.id, "Iltimos, faqat rasm yuboring.")
        return

    profile.temp_data['image'] = message.photo[-1].file_id
    _show_confirmation_message(message, bot, profile)


def _show_confirmation_message(message, bot, profile):
    data = profile.temp_data

    confirmation_text = f"""
<b>Iltimos, ma'lumotlarni tekshiring:</b>

<b>Nomi (UZ):</b> {data.get('name_uz')}
<b>Nomi (RU):</b> {data.get('name_ru')}
<b>Kategoriya:</b> {data.get('category_name')}
<b>Lokatsiya:</b> Lat: {data.get('latitude')}, Lon: {data.get('longitude')}
<b>Kontakt:</b> {data.get('contact')}
<b>Tavsif (UZ):</b> {data.get('description_uz')}
<b>Tavsif (RU):</b> {data.get('description_ru')}
"""

    markup = keyboards.get_add_place_confirmation_keyboard(profile)
    bot.send_photo(message.chat.id, data['image'], caption=confirmation_text, reply_markup=markup, parse_mode='HTML')
    profile.step = UserSteps.PLACE_ADD_WAITING_FOR_CONFIRMATION
    profile.save()


def process_add_place_confirm(call, bot):
    profile = TelegramProfile.objects.get(tg_id=call.message.chat.id)

    if not profile.user:
        bot.answer_callback_query(call.id, "Xatolik: Foydalanuvchi topilmadi.", show_alert=True)
        return

    latitude = profile.temp_data.get("latitude")
    longitude = profile.temp_data.get("longitude")

    location_dict = None
    if latitude and longitude:
        location_dict = {
            "latitude": latitude,
            "longitude": longitude
        }

    data_to_send = {
        "name": profile.temp_data.get("name_uz"),
        "name_uz": profile.temp_data.get("name_uz"),
        "name_ru": profile.temp_data.get("name_ru"),
        "description": profile.temp_data.get("description_uz"),
        "description_uz": profile.temp_data.get("description_uz"),
        "description_ru": profile.temp_data.get("description_ru"),
        "category": profile.temp_data.get("category"),
        "contact": profile.temp_data.get("contact"),
        "user": profile.user.id,
        "image": profile.temp_data.get("image"),
        "location": json.dumps(location_dict) if location_dict else ""
    }

    response = api_client.add_place(profile, data_to_send)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if response and response.status_code == 201:
        bot.send_message(call.message.chat.id, "✅ Joy muvaffaqiyatli qo'shildi!")
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
            f"❌ Joy qo'shishda xatolik yuz berdi:\n\n{error_details}",
            parse_mode="Markdown"
        )

    profile.temp_data = {}
    profile.step = UserSteps.DEFAULT
    profile.save()
    from .start import show_main_menu
    show_main_menu(call.message, bot)


def process_add_place_cancel(call, bot):
    profile = TelegramProfile.objects.get(tg_id=call.message.chat.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "❌ Joy qo'shish bekor qilindi.")
    profile.temp_data = {}
    profile.step = UserSteps.DEFAULT
    profile.save()
    show_main_menu(call.message, bot)