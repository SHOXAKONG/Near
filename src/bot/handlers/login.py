import telebot
from django.contrib.auth import get_user_model
from ..models import TelegramProfile
from .. import utils, keyboards, api_client
from ..constants import UserSteps
from .start import show_main_menu
from .profile import show_profile_menu


def start_login(message, bot):
    profile, _ = TelegramProfile.objects.get_or_create(tg_id=message.chat.id)

    if profile.user:
        bot.send_message(message.chat.id, utils.t(profile, "Siz allaqachon tizimdasiz.", "Вы уже в системе."))
        return

    prompt = utils.t(profile, "Email manzilingizni kiriting:", "Введите ваш email:")

    bot.send_message(message.chat.id, prompt)

    profile.temp_data = {}
    profile.step = UserSteps.LOGIN_WAITING_FOR_EMAIL
    profile.save()


def process_login_email(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    profile.temp_data = {'email': message.text}

    prompt = utils.t(profile, "Parolni kiriting:", "Введите пароль:")
    bot.send_message(message.chat.id, prompt)

    profile.step = UserSteps.LOGIN_WAITING_FOR_PASSWORD
    profile.save()


def process_login_password(message, bot):
    profile = TelegramProfile.objects.get(tg_id=message.chat.id)
    email = profile.temp_data.get('email')
    password = message.text
    response = api_client.login_with_password(profile.language, email, password)

    if response.status_code == 200:
        api_data = response.json()
        access = api_data.get('access')
        refresh = api_data.get('refresh')
        User = get_user_model()

        try:
            logged_in_user = User.objects.get(email=email)
            profile.user = logged_in_user
            profile.access_token = access
            profile.refresh_token = refresh
            profile.save()

            user_data_response = api_client.get_user_data_from_api(profile)
            if user_data_response and user_data_response.status_code == 200:
                user_data = user_data_response.json()
                profile.is_entrepreneur = user_data.get('is_entrepreneur', False)
                profile.save(update_fields=['is_entrepreneur'])

            bot.send_message(message.chat.id, f"✅ {utils.t(profile, 'Xush kelibsiz!', 'Добро пожаловать!')}")
            show_main_menu(message, bot)

        except User.DoesNotExist:
            bot.send_message(message.chat.id,
                             f"❌ {utils.t(profile, 'Foydalanuvchi lokal bazada topilmadi.', 'Пользователь не найден в локальной базе.')}")
            profile.step = UserSteps.DEFAULT
            profile.save()
    else:
        profile.step = UserSteps.DEFAULT
        profile.save()

    profile.temp_data = {}