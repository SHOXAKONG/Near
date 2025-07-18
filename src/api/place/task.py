import requests
from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
import logging

from src.api.place.utils import convert_image
from src.apps.place.models import Place

logger = logging.getLogger(__name__)

@shared_task
def process_telegram_image(place_id, file_id):
    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        logger.error(f"Place with id={place_id} not found. Aborting image processing.")
        return

    try:
        file_info_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getFile?file_id={file_id}"
        file_info_res = requests.get(file_info_url, timeout=10)
        file_info_res.raise_for_status()
        file_path = file_info_res.json()['result']['file_path']

        file_url = f"https://api.telegram.org/file/bot{settings.BOT_TOKEN}/{file_path}"
        image_res = requests.get(file_url, timeout=15)
        image_res.raise_for_status()

        converted_image_bytes = convert_image(image_res.content, target_format='JPEG')
        image_name = f"{file_id}.jpg"
        image_content = ContentFile(converted_image_bytes, name=image_name)

        place.image = image_content
        place.save(update_fields=['image'])
        logger.info(f"Successfully processed and saved image for Place id={place_id}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Telegram for Place id={place_id}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while processing image for Place id={place_id}: {e}")

