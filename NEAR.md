# Near loyihasi haqida qisqacha hisobot

## 1. Kirish

Near loyihasi foydalanuvchilarga o‘zlariga eng yaqin bo‘lgan obyektlarni – dorixona, restoran, kafe, do‘kon, bankomat va boshqa xizmat ko‘rsatish nuqtalarini tezkor va qulay topishga yordam beruvchi tizimdir. Loyiha zamonaviy texnologiyalar asosida ishlab chiqilgan bo‘lib, unda geo-ma’lumotlar bilan ishlash, foydalanuvchi boshqaruvi va real vaqtli qidiruv imkoniyatlari asosiy o‘rin tutadi.

Tizimning asosiy maqsadi – foydalanuvchining lokatsiyasidan kelib chiqib, unga eng mos va eng yaqin obyektlarni aniq hisoblash hamda soddalashtirilgan interfeys orqali taqdim etishdir. Shu orqali loyiha kundalik hayotda foydalanuvchilarga vaqtni tejash va kerakli joyni topishda samarali yordamchi bo‘lib xizmat qiladi.

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
