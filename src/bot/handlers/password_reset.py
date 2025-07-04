import telebot
from ..models import TelegramProfile
from .. import utils, keyboards, api_client
from ..constants import UserSteps
from .start import show_main_menu


def start_password_reset(message, bot):
    profile, _ = TelegramProfile.objects.get_or_create(tg_id=message.chat.id)
    prompt = utils.t(profile, "Parolni tiklash uchun emailingizni kiriting:",
                     "Введите ваш email для восстановления пароля:")

    # reply_markup parametri olib tashlandi
    bot.send_message(message.chat.id, prompt)

    profile.step = UserSteps.RESET_WAITING_FOR_EMAIL
    profile.save()


def process_email_for_reset(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    email = message.text
    profile.temp_data = {'email': email}
    profile.save()

    response = api_client.forgot_password(profile.language, email)

    if response.status_code == 200:
        bot.send_message(message.chat.id, response.json().get('message'))
        prompt = utils.t(profile, "Emailingizga yuborilgan kodni kiriting:", "Введите код из вашего письма:")
        bot.send_message(message.chat.id, prompt)
        profile.step = UserSteps.RESET_WAITING_FOR_CODE
    else:
        bot.send_message(message.chat.id, utils.t(profile, "❌ Email topilmadi.", "❌ Email не найден."))
        profile.step = UserSteps.DEFAULT

    profile.save()


def process_restore_code(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    code = message.text
    profile.temp_data['code'] = code
    profile.save()

    prompt = utils.t(profile, "Yangi parol yarating:", "Создайте новый пароль:")
    bot.send_message(message.chat.id, prompt)
    profile.step = UserSteps.RESET_WAITING_FOR_NEW_PASSWORD
    profile.save()


def process_restore_password(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    password = message.text
    profile.temp_data['password'] = password
    profile.save()

    prompt = utils.t(profile, "Yangi parolni tasdiqlang:", "Подтвердите новый пароль:")
    bot.send_message(message.chat.id, prompt)
    profile.step = UserSteps.RESET_WAITING_FOR_PASSWORD_CONFIRM
    profile.save()


def process_restore_password_confirm(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data['password_confirm'] = message.text

    data_to_send = profile.temp_data
    response = api_client.restore_password(profile.language, data_to_send)

    if response.status_code == 200:
        success_message = utils.t(profile,
                                  "✅ Parolingiz muvaffaqiyatli o'zgartirildi. Endi tizimga kirishingiz mumkin.",
                                  "✅ Ваш пароль успешно изменен. Теперь вы можете войти в систему.")
        bot.send_message(message.chat.id, success_message)
    else:
        error_message = response.json().get('error', utils.t(profile, 'Xatolik', 'Ошибка'))
        bot.send_message(message.chat.id, f"❌ {error_message}")

    profile.temp_data = {}
    profile.step = UserSteps.DEFAULT
    profile.save()
    from .profile import show_profile_menu
    show_profile_menu(message, bot)