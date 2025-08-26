# Near loyihasi haqida qisqacha hisobot

## 1. Kirish

Ushbu loyiha **Python** va **Django** yordamida ishlab chiqildi. Loyihaning asosiy maqsadi foydalanuvchilar uchun qulay va samarali tizim yaratish bo‘lib, unda backend asosiy rolni o‘ynaydi. Loyihaning dastlabki rejalashtirilgan qismi frontend bilan integratsiya qilish bo‘lgan, biroq frontend bilimlari yetarli bo‘lmagani uchun loyiha **Telegram bot** orqali amalga oshirildi.

**Near loyihasi** foydalanuvchiga o‘ziga eng yaqin joylarni (dorixona, restoran, kafe, do‘kon, bankomat va boshqalar) topishda yordam beradi.

---

## 2. Texnologiyalar

* **Django (Python)** – asosiy backend framework sifatida
* **Django REST Framework (DRF)** – API yozish uchun
* **PostgreSQL + PostGIS** – ma’lumotlar bazasi va geo-ma’lumotlar uchun
* **Docker** – deploy va konteynerlash jarayonlarida
* **Telegram Bot API** – foydalanuvchilar bilan muloqot qilish uchun

---

## 3. Loyiha tuzilishi

Loyiha quyidagi asosiy komponentlardan tashkil topgan:

* **User boshqaruvi** – ro‘yxatdan o‘tish, login, token asosidagi autentifikatsiya
* **Place boshqaruvi** – joylarni (restoran, dorixona, kafe va boshqalar) qo‘shish, tahrirlash
* **Search History** – foydalanuvchilar tomonidan amalga oshirilgan qidiruvlarni saqlash
* **Admin panel** – admin obyektlarni boshqaradi, foydalanuvchi faoliyatini kuzatadi
* **Telegram bot** – foydalanuvchiga eng yaqin joylarni ko‘rsatadi, admin bilan chat qilish imkoniyatini beradi

---

## 4. Telegram bot

Frontend o‘rniga ishlab chiqilgan Telegram bot quyidagi funksiyalarni bajaradi:

* Foydalanuvchi lokatsiya yuboradi va bot unga eng yaqin joylarni qaytaradi
* Har bir joy haqida nom, manzil, masofa va xaritada ko‘rish linki ko‘rsatiladi
* Admin va foydalanuvchi o‘rtasida chat qilish imkoniyati mavjud
* Qidiruvlar tarixi saqlanadi va statistikada aks etadi

---

## 5. Afzalliklari

* **GeoDjango + PostGIS** orqali tezkor va aniq geo-hisoblash
* **Telegram bot** yordamida foydalanuvchilar uchun qulay interfeys
* **Admin** tomonidan joylar va foydalanuvchilarni boshqarish imkoniyati
* **Docker** orqali deploy qilinishi mumkin

---

## 6. Xulosa

**Near loyihasi** odamlarning eng yaqin obyektlarni tez va qulay topish muammosini hal qiladi. Telegram bot frontend o‘rnini bosgan holda, loyiha amaliy jihatdan sinovdan o‘tkazildi. Keyingi bosqichlarda loyiha uchun to‘liq frontend qismi ishlab chiqilishi, kengaytirilgan qidiruv imkoniyatlari va foydalanuvchi statistikasi qo‘shilishi rejalashtirilmoqda.
