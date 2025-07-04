import requests
import telebot
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .start import show_main_menu
from ..models import TelegramProfile
from .. import utils, keyboards, api_client
from ..constants import UserSteps
from .profile import show_profile_menu
from .login import start_login


def start_registration(message, bot):
    profile, _ = TelegramProfile.objects.get_or_create(tg_id=message.chat.id)

    if profile.user:
        bot.send_message(message.chat.id, utils.t(profile, "Siz allaqachon tizimdasiz.", "Вы уже в системе."))
        return

    prompt = utils.t(profile, "Ismingizni kiriting:", "Введите ваше имя:")

    bot.send_message(message.chat.id, prompt)

    profile.step = UserSteps.REG_WAITING_FOR_FIRST_NAME
    profile.temp_data = {}
    profile.save()


def process_first_name(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['first_name'] = message.text

    prompt = utils.t(profile, "Familyangizni kiriting:", "Введите вашу фамилию:")
    bot.send_message(message.chat.id, prompt)

    profile.step = UserSteps.REG_WAITING_FOR_LAST_NAME
    profile.save()


def process_last_name(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['last_name'] = message.text

    prompt = utils.t(profile, "Email manzilingizni kiriting:", "Введите ваш email:")
    bot.send_message(message.chat.id, prompt)

    profile.step = UserSteps.REG_WAITING_FOR_EMAIL
    profile.save()


def process_email(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['email'] = message.text

    prompt = utils.t(profile, "Parol yarating:", "Создайте пароль:")
    bot.send_message(message.chat.id, prompt)

    profile.step = UserSteps.REG_WAITING_FOR_PASSWORD
    profile.save()


def process_password(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['password'] = message.text

    prompt = utils.t(profile, "Parolni tasdiqlang:", "Подтвердите пароль:")
    bot.send_message(message.chat.id, prompt)

    profile.step = UserSteps.REG_WAITING_FOR_PASSWORD_CONFIRM
    profile.save()


def process_password_confirm(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)

    if profile.temp_data.get('password') != message.text:
        bot.send_message(message.chat.id, utils.t(profile, "❌ Parollar mos kelmadi. Iltimos, qaytadan urinib ko'ring.",
                                                  "❌ Пароли не совпадают. Пожалуйста, попробуйте снова."))
        prompt = utils.t(profile, "Parol yarating:", "Создайте пароль:")
        bot.send_message(message.chat.id, prompt)
        profile.step = UserSteps.REG_WAITING_FOR_PASSWORD
        profile.save()
        return

    profile.temp_data['password_confirm'] = message.text
    bot.send_message(message.chat.id, utils.t(profile, "Ma'lumotlar yuborilmoqda...", "Отправляем данные..."))

    response = api_client.register_user(profile.language, profile.temp_data)

    if response and response.status_code == 201:
        User = get_user_model()
        reg_data = profile.temp_data
        try:
            new_user = User.objects.create_user(
                username=reg_data['email'], email=reg_data['email'], password=reg_data['password'],
                first_name=reg_data.get('first_name', ''), last_name=reg_data.get('last_name', '')
            )
            profile.user = new_user
            prompt = utils.t(profile,
                             "✅ Ro‘yxatdan o‘tish muvaffaqiyatli! Hisobingizni faollashtirish uchun emailingizga yuborilgan tasdiqlash kodini kiriting:",
                             "✅ Регистрация прошла успешно! Введите код подтверждения, отправленный на вашу электронную почту, чтобы активировать свою учетную запись:")
            bot.send_message(message.chat.id, prompt)
            profile.step = UserSteps.REG_WAITING_FOR_CONFIRMATION
        except IntegrityError:
            bot.send_message(message.chat.id,
                             f"❌ {utils.t(profile, 'Ushbu email bilan foydalanuvchi allaqachon mavjud.', 'Пользователь с таким email уже существует.')}")
            profile.step = UserSteps.DEFAULT
            show_profile_menu(message, bot)
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Lokal foydalanuvchi yaratishda noma'lum xatolik: {e}")
            profile.step = UserSteps.DEFAULT
            show_profile_menu(message, bot)
    else:
        error_msg = utils.t(profile, "Noma'lum xatolik.", "Неизвестная ошибка.")
        if response is not None:
            try:
                error_data = response.json()
                error_msg = error_data.get('detail', str(error_data))
            except requests.exceptions.JSONDecodeError:
                error_msg = f"Server xatosi (kod: {response.status_code})."
                if response.text:
                    error_msg += f" Server javobi: {response.text}"

        bot.send_message(message.chat.id, f"❌ Ro'yxatdan o'tishda xatolik: {error_msg}")
        profile.step = UserSteps.DEFAULT
        show_profile_menu(message, bot)

    profile.temp_data = {}
    profile.save()


# def process_confirmation_code(message, bot):
#     profile = TelegramProfile.objects.get(tg_id=message.chat.id)
#     code = message.text
#     response = api_client.register_user(profile.language, profile.temp_data)
#
#     if response and response.status_code == 201:
#         User = get_user_model()
#         reg_data = profile.temp_data
#         try:
#             new_user = User.objects.create_user(
#                 username=reg_data['email'], email=reg_data['email'], password=reg_data['password'],
#                 # ...
#             )
#             # Agar muvaffaqiyatli bo'lsa, keyingi qadamga o'tadi
#             profile.user = new_user
#             prompt = utils.t(profile, "✅ Ro‘yxatdan o‘tish muvaffaqiyatli! ...", "...")
#             bot.send_message(message.chat.id, prompt)
#             profile.step = UserSteps.REG_WAITING_FOR_CONFIRMATION
#
#         except IntegrityError:
#             # AGAR BUNDAY FOYDALANUVCHI BAZADA BOR BO'LSA, KOD SHU YERGA TUSHADI
#             bot.send_message(message.chat.id,
#                              f"❌ {utils.t(profile, 'Ushbu email bilan foydalanuvchi allaqachon mavjud.', 'Пользователь с таким email уже существует.')}")
#             profile.step = UserSteps.DEFAULT
#             show_profile_menu(message, bot)
#
#     else:
#         error_message = "Noma'lum xatolik"
#         if response is not None:
#             try:
#                 error_message = response.json().get('error', utils.t(profile, 'Kod xato yoki eskirgan.',
#                                                                      'Код неверный или просрочен.'))
#             except:
#                 pass
#         bot.send_message(message.chat.id, f"❌ {error_message}")
#         show_profile_menu(message, bot)
#
#     profile.step = UserSteps.DEFAULT
#     profile.save()