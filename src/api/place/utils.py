import base64
import io
import json
import os
from io import BytesIO

from django.conf import settings
from PIL import Image


def t(profile, key_uz: str, key_ru: str) -> str:
    return key_uz if profile.language == 'uz' else key_ru


def decode_token(token: str) -> dict:
    try:
        payload_b64 = token.split('.')[1]
        payload_b64 += '=' * (-len(payload_b64) % 4)
        payload_json = base64.b64decode(payload_b64).decode('utf-8')
        return json.loads(payload_json)
    except Exception:
        return {}


def convert_image(image_bytes: bytes, target_format: str = 'JPEG', quality: int = 85) -> bytes:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        output_buffer = io.BytesIO()

        if target_format.upper() == 'JPEG':
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            image.save(output_buffer, format='JPEG', quality=quality, optimize=True)
        elif target_format.upper() == 'PNG':
            image.save(output_buffer, format='PNG', optimize=True)
        else:
            raise ValueError("Qo'llab-quvvatlanadigan formatlar: 'JPEG' yoki 'PNG'")

        return output_buffer.getvalue()
    except Exception:
        return image_bytes


def add_watermark(image_bytes: bytes) -> bytes:
    try:
        main_image = Image.open(BytesIO(image_bytes)).convert("RGBA")

        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'near-logo.png')

        if not os.path.exists(logo_path):
            print(f"OGOHLANTIRISH: Logotip fayli topilmadi: {logo_path}")
            return image_bytes

        logo_image = Image.open(logo_path).convert("RGBA")

        logo_width = main_image.width // 4
        if logo_width == 0:
            return image_bytes

        ratio = logo_width / float(logo_image.size[0])
        logo_height = int((float(logo_image.size[1]) * float(ratio)))
        resized_logo = logo_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

        padding = 5
        position = (
            padding,
            padding
        )

        main_image.paste(resized_logo, position, resized_logo)

        buffer = BytesIO()
        main_image.save(buffer, format='PNG')
        buffer.seek(0)

        return buffer.getvalue()
    except Exception as e:
        print(f"Logotip qo'shishda xatolik: {e}")
        return image_bytes
