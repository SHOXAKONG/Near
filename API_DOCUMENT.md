# NEAR API Hujjati / NEAR API Документация

Ushbu hujjat **NEAR loyihasi API** uchun tuzilgan bo‘lib, ikki tilda: **o‘zbek** va **rus** tillarida keltirilgan.  
API JWT orqali autentifikatsiya qilinadi.

---

# Avtorizatsiya (Auth)

## Ro‘yxatdan o‘tish / Регистрация
**POST** `/uz/api/auth/register/`  
**POST** `/ru/api/auth/register/`

**Request JSON**
```json
{
  "email": "user@example.com",
  "first_name": "Ali",
  "last_name": "Valiyev",
  "password": "Parol123",
  "password_confirm": "Parol123"
}
```

**Response (201)**
```json
{
  "id": 15,
  "email": "user@example.com",
  "first_name": "Ali",
  "last_name": "Valiyev",
  "is_active": true,
  "role": "user",
  "age": 25
}
```

---

## Login / Вход
**POST** `/uz/api/auth/login/`  
**POST** `/ru/api/auth/login/`

**Request JSON**
```json
{
  "email": "user@example.com",
  "password": "Parol123"
}
```

**Response (200)**
```json
{
  "access": "ACCESS_TOKEN_EXAMPLE",
  "refresh": "REFRESH_TOKEN_EXAMPLE"
}
```

---

## Tokenni yangilash / Обновление токена
**POST** `/uz/api/auth/login-token/refresh/`  
**POST** `/ru/api/auth/login-token/refresh/`

**Request JSON**
```json
{
  "refresh": "REFRESH_TOKEN_EXAMPLE"
}
```

**Response (200)**
```json
{
  "access": "NEW_ACCESS_TOKEN"
}
```

---

## Logout / Выход
**DELETE** `/uz/api/auth/logout/`  
**DELETE** `/ru/api/auth/logout/`

**Response (200)**  
```json
{}
```

---

## Parolni unutganda / Забыли пароль
**POST** `/uz/api/auth/forgot_password/`  
**POST** `/ru/api/auth/forgot_password/`

**Request JSON**
```json
{
  "email": "user@example.com"
}
```

**Response (201)**
```json
{
  "email": "user@example.com"
}
```

---

## Parolni tiklash / Восстановление пароля
**POST** `/uz/api/auth/restore_password/`  
**POST** `/ru/api/auth/restore_password/`

**Request JSON**
```json
{
  "code": "123456",
  "password": "NewPassword123",
  "password_confirm": "NewPassword123"
}
```

**Response (201)**
```json
{
  "code": "123456"
}
```

---

# Kategoriyalar / Категории

## Ro‘yxat olish / Получить список
**GET** `/uz/api/category/`  
**GET** `/ru/api/category/`

**Response (200)**
```json
{
  "count": 2,
  "results": [
    {"id": 1, "name": "Restoran / Ресторан"},
    {"id": 2, "name": "Do‘kon / Магазин"}
  ]
}
```

---

## Yangi kategoriya qo‘shish / Добавить категорию
**POST** `/uz/api/category/`  
**POST** `/ru/api/category/`

**Request JSON**
```json
{
  "name": "Restoran"
}
```

**Response (201)**
```json
{
  "id": 1,
  "name": "Restoran / Ресторан"
}
```

---

## Bitta kategoriya olish / Получить категорию
**GET** `/uz/api/category/{id}/`  
**GET** `/ru/api/category/{id}/`

**Response (200)**
```json
{
  "id": 1,
  "name": "Restoran / Ресторан"
}
```

---

## Kategoriyani yangilash / Обновить категорию
**PUT/PATCH** `/uz/api/category/{id}/`  
**PUT/PATCH** `/ru/api/category/{id}/`

**Request JSON**
```json
{
  "name": "Do‘kon"
}
```

**Response (200)**
```json
{
  "id": 1,
  "name": "Do‘kon / Магазин"
}
```

---

## Kategoriyani o‘chirish / Удалить категорию
**DELETE** `/uz/api/category/{id}/`  
**DELETE** `/ru/api/category/{id}/`

**Response (204)**
```json
{}
```

---

# Joylar (Place) / Места

## Joy qo‘shish / Добавить место
**POST** `/uz/api/place/`  
**POST** `/ru/api/place/`

**Request JSON**
```json
{
  "name": "Cafe Bon",
  "name_uz": "Cafe Bon",
  "name_ru": "Кафе Бон",
  "category": 2,
  "contact": "+998901234567",
  "location": {
    "latitude": 41.2995,
    "longitude": 69.2401
  },
  "description": "Chiroyli kafe",
  "description_uz": "Chiroyli kafe",
  "description_ru": "Красивое кафе"
}
```

**Response (201)**
```json
{
  "id": 10,
  "name": "Cafe Bon",
  "name_uz": "Cafe Bon",
  "name_ru": "Кафе Бон",
  "category": 2,
  "contact": "+998901234567",
  "location": {
    "latitude": 41.2995,
    "longitude": 69.2401
  },
  "distance": null,
  "created_at": "2025-08-26T12:00:00Z",
  "updated_at": "2025-08-26T12:00:00Z",
  "image_url": null,
  "description": "Chiroyli kafe",
  "description_uz": "Chiroyli kafe",
  "description_ru": "Красивое кафе"
}
```

---

## Joyni yangilash / Обновить место
**PUT/PATCH** `/uz/api/place/{id}/`  
**PUT/PATCH** `/ru/api/place/{id}/`

**Request JSON**
```json
{
  "name": "Cafe New",
  "name_uz": "Cafe Yangi",
  "name_ru": "Кафе Новое",
  "category": 2,
  "contact": "+998907654321",
  "location": {
    "latitude": 41.3100,
    "longitude": 69.2500
  },
  "description": "Yangi kafe",
  "description_uz": "Yangi kafe",
  "description_ru": "Новое кафе"
}
```

**Response (200)**
```json
{
  "id": 10,
  "name": "Cafe New",
  "name_uz": "Cafe Yangi",
  "name_ru": "Кафе Новое",
  "category": 2,
  "contact": "+998907654321",
  "location": {
    "latitude": 41.3100,
    "longitude": 69.2500
  },
  "distance": null,
  "created_at": "2025-08-26T12:00:00Z",
  "updated_at": "2025-08-27T10:00:00Z",
  "image_url": null,
  "description": "Yangi kafe",
  "description_uz": "Yangi kafe",
  "description_ru": "Новое кафе"
}
```

---

# Statistikalar / Статистика

## Aktiv foydalanuvchilar / Активные пользователи
**GET** `/uz/api/statistics/active-users/`  
**GET** `/ru/api/statistics/active-users/`

**Response (200)**
```json
{
  "count": 1,
  "results": [
    {
      "user_id": 1,
      "first_name": "Ali",
      "total_searches": 15
    }
  ]
}
```

---

## Kategoriyalar bo‘yicha qidiruv / Поиск по категориям
**GET** `/uz/api/statistics/by-category/`  
**GET** `/ru/api/statistics/by-category/`

**Response (200)**
```json
{
  "count": 1,
  "results": [
    {
      "category_id": 1,
      "category_name": "Restoran / Ресторан",
      "search_count": 50
    }
  ]
}
```

---

## Kunlik qidiruvlar / Ежедневные запросы
**GET** `/uz/api/statistics/daily-searches/`  
**GET** `/ru/api/statistics/daily-searches/`

**Response (200)**
```json
{
  "count": 1,
  "results": [
    {
      "date": "2025-01-01",
      "search_count": 100
    }
  ]
}
```

---

## Oylik xulosa / Ежемесячный отчет
**GET** `/uz/api/statistics/monthly-summary/`  
**GET** `/ru/api/statistics/monthly-summary/`

**Response (200)**
```json
[
  {
    "month": "2025-01-01",
    "user_registrations": 30,
    "category_searches": 200
  }
]
```

---

# HTTP Status Kodlari / HTTP Status Codes

| HTTP Code | Tavsif (RU)                                        | Tavsif (UZ)                               |
|-----------|----------------------------------------------------|-------------------------------------------|
| **200**   | OK – Успешный GET, PUT или POST запрос             | OK – Muvaffaqiyatli GET, PUT yoki POST so‘rovi |
| **201**   | Created – Ресурс успешно создан                    | Created – Resurs muvaffaqiyatli yaratildi  |
| **204**   | No Content – Успешное удаление                     | No Content – Muvaffaqiyatli o‘chirildi     |
| **400**   | Bad Request – Отсутствуют или неверные параметры   | Bad Request – Parametrlar yo‘q yoki noto‘g‘ri |
| **401**   | Unauthorized – Неверный или отсутствующий токен аутентификации | Unauthorized – Avtorizatsiya tokeni yo‘q yoki noto‘g‘ri |
| **403**   | Forbidden – Недостаточно прав                      | Forbidden – Ruxsat yetarli emas            |
| **404**   | Not Found – Ресурс не найден                       | Not Found – Resurs topilmadi               |
| **409**   | Conflict – Например, дублирующиеся записи           | Conflict – Masalan, dublikat yozuv mavjud  |


---
# Asosiy Ma’lumotlar Maydonlari / Основные поля данных

| Name              | Type      | Tavsif (RU)                                                      | Tavsif (UZ)                                                        |
|-------------------|-----------|------------------------------------------------------------------|--------------------------------------------------------------------|
| **id**            | integer   | Уникальный идентификатор ресурса                                | Resurs uchun noyob identifikator                                   |
| **email**         | varchar   | Email пользователя, используется для логина и связи             | Foydalanuvchi email manzili, login va aloqa uchun ishlatiladi      |
| **first_name**    | varchar   | Имя пользователя                                                | Foydalanuvchi ismi                                                 |
| **last_name**     | varchar   | Фамилия пользователя                                            | Foydalanuvchi familiyasi                                           |
| **password**      | varchar   | Пароль пользователя (хранится в зашифрованном виде)             | Foydalanuvchi paroli (shifrlangan holda saqlanadi)                 |
| **password_confirm** | varchar | Подтверждение пароля                                            | Parolni tasdiqlash                                                 |
| **access**        | varchar   | JWT Access Token                                                | JWT Access Token                                                   |
| **refresh**       | varchar   | JWT Refresh Token                                               | JWT Refresh Token                                                  |
| **role**          | varchar   | Роль пользователя (например: user, admin)                       | Foydalanuvchi roli (masalan: user, admin)                         |
| **is_active**     | boolean   | Активен ли пользователь                                         | Foydalanuvchi aktivligi                                           |
| **age**           | integer   | Возраст пользователя (если доступно)                            | Foydalanuvchi yoshi (agar mavjud bo‘lsa)                          |
| **name**          | varchar   | Название категории или места                                    | Kategoriya yoki joy nomi                                          |
| **name_uz**       | varchar   | Название на узбекском языке                                     | O‘zbek tilidagi nomi                                               |
| **name_ru**       | varchar   | Название на русском языке                                       | Rus tilidagi nomi                                                  |
| **category**      | integer   | ID категории, к которой принадлежит место                       | Joy tegishli bo‘lgan kategoriya ID’si                              |
| **contact**       | varchar   | Контактный номер или данные                                     | Kontakt raqami yoki ma’lumotlari                                  |
| **location**      | object    | Геолокация (широта и долгота)                                   | Joylashuv (latitude va longitude)                                 |
| **latitude**      | float     | Географическая широта                                           | Geografik kenglik                                                  |
| **longitude**     | float     | Географическая долгота                                          | Geografik uzunlik                                                  |
| **description**   | text      | Описание ресурса                                               | Resurs haqida ta’rif                                               |
| **description_uz**| text      | Описание на узбекском                                          | O‘zbek tilidagi ta’rif                                             |
| **description_ru**| text      | Описание на русском                                            | Rus tilidagi ta’rif                                                |
| **image_url**     | varchar   | Ссылка на изображение                                           | Rasm URL manzili                                                   |
| **created_at**    | datetime  | Дата создания                                                  | Yaratilgan sana                                                    |
| **updated_at**    | datetime  | Дата обновления                                                | Yangilangan sana                                                   |
| **distance**      | float     | Расстояние до места (если доступно)                             | Joygacha masofa (agar mavjud bo‘lsa)                               |
| **user_id**       | integer   | ID пользователя (например, в статистике активных пользователей) | Foydalanuvchi ID’si (masalan, aktiv foydalanuvchilar statistikasi) |
| **total_searches**| integer   | Количество поисковых запросов                                   | Qidiruvlar soni                                                    |
| **search_count**  | integer   | Количество запросов по категории или дате                      | Kategoriya yoki sanaga ko‘ra qidiruvlar soni                       |
| **date**          | date      | Дата для статистики (ежедневные поиски)                         | Statistikadagi sana (kunlik qidiruvlar)                            |
| **month**         | date      | Месяц для отчета (ежемесячная статистика)                       | Hisobotdagi oy (oylik statistika)                                 |
| **user_registrations** | integer | Количество регистраций пользователей за месяц                  | Oylik foydalanuvchi ro‘yxatdan o‘tishlari soni                     |
| **category_searches**  | integer | Количество поисков по категориям за месяц                      | Oylik kategoriyalar bo‘yicha qidiruvlar soni                       |


---

# Xulosa / Заключение

## O‘zbekcha:
Ushbu hujjatda **NEAR loyihasi API** uchun asosiy autentifikatsiya, kategoriyalar, joylar va statistika bo‘limlari batafsil yoritildi.  
API **JWT tokenlari** yordamida himoyalangan va foydalanuvchilarni ro‘yxatdan o‘tkazish, login qilish, parolni tiklash kabi imkoniyatlarni taqdim etadi.  
Shuningdek, **kategoriya va joylarni boshqarish (CRUD)** funksiyalari ham mavjud bo‘lib, tizim foydalanuvchilarning qidiruv faoliyatini kuzatish va **statistik hisobotlarni** (kunlik, oylik) shakllantirish imkonini beradi.  

Bu hujjat **dasturchilar** uchun qo‘llanma bo‘lib xizmat qiladi va **NEAR API bilan ishlashda yagona manba** sifatida foydalanilishi mumkin.  

---

## Русский:
В данном документе подробно описаны основные разделы **NEAR проекта API**: аутентификация, категории, места и статистика.  
API защищён с помощью **JWT токенов** и предоставляет возможности регистрации пользователей, входа в систему и восстановления пароля.  
Кроме того, реализованы функции **управления категориями и местами (CRUD)**, а также отслеживание поисковой активности пользователей и формирование **статистических отчетов** (ежедневных и ежемесячных).  

Этот документ служит руководством для **разработчиков** и может использоваться как **основной источник информации** при работе с NEAR API.  

