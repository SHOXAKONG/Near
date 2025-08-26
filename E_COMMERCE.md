# ERD Hujjati – v1 va v2 taqqoslash

Quyida **v2 (yangilangan)** va **v1 (dastlabki)** sxemalar Mermaid.js `erDiagram` ko‘rinishida berilgan. Keyin qisqa izohlar va taqqoslash jadvali keltiriladi.

---

## 1) v2 – Yangilangan ERD (joriy variant)

```mermaid
erDiagram
  USERS ||--o{ ADDRESS : "manzillari"
  USERS ||--o{ CART : "savatlari"
  CART  ||--o{ CART_ITEM : "tovarlar"
  CART_ITEM }o--|| PRODUCTS : "savatda"

  USERS ||--o{ WISHLIST : "xohishlar"
  WISHLIST }o--|| PRODUCTS : "saqlangan"

  USERS ||--o{ ORDERS : "buyurtmalar"
  ORDERS ||--|{ ORDER_ITEMS : "tarkibi"
  ORDER_ITEMS }o--|| PRODUCTS : "sotib olingan"

  ORDERS ||--o{ PAYMENT : "to'lovlar"
  ORDERS ||--o{ ORDER_STATUS_HISTORY : "status tarixi"
  ORDER_STATUS_HISTORY }o--o{ USERS : "by_user (ixtiyoriy)"

  PRODUCTS }o--|| CATEGORY : "kategoriya"
  CATEGORY ||--o{ CATEGORY : "parent (o'z-o'zini bog')"

  INVENTORY }o--|| PRODUCTS : "qoldiq"
  INVENTORY }o--|| USERS : "seller (rol=seller)"

  USERS {
    bigint id PK
    varchar email
    varchar first_name
    varchar last_name
    varchar phone_number
    bigint role_id FK
  }
  ROLE {
    bigint id PK
    varchar name
  }
  ADDRESS {
    bigint id PK
    varchar country
    varchar city
    varchar street
    bigint user_id FK
  }
  CATEGORY {
    bigint id PK
    varchar name
    bigint parent FK
  }
  PRODUCTS {
    bigint id PK
    varchar name
    text description
    decimal price
    numeric rating
    boolean is_active
    bigint category FK
  }
  CART {
    bigint id PK
    bigint user_id FK
    timestamp created_at
  }
  CART_ITEM {
    bigint id PK
    bigint cart_id FK
    bigint product_id FK
    int quantity
  }
  WISHLIST {
    bigint id PK
    bigint user_id FK
    bigint product_id FK
    timestamp created_at
  }
  ORDERS {
    bigint id PK
    bigint user_id FK
    varchar status
    decimal total_amount
  }
  ORDER_ITEMS {
    bigint id PK
    bigint order_id FK
    bigint product_id FK
    int quantity
    decimal price
  }
  PAYMENT {
    bigint id PK
    bigint order_id FK
    decimal amount
    varchar status
    varchar method
  }
  ORDER_STATUS_HISTORY {
    bigint id PK
    bigint order_id FK
    varchar from_status
    varchar to_status
    timestamp at
    bigint by_user FK
  }
  INVENTORY {
    bigint id PK
    bigint seller FK
    bigint product FK
    int stock
  }
  USERS ||--o{ ROLE : "has"  %% ko'rinish uchun ulanma
```
---

![alt text](<drawSQL-image-export-2025-08-26 (1).png>)

---

**Qisqa izohlar (v2):**

* `CATEGORY` o‘zini-o‘zi `parent` bilan bog‘laydi → istalgan chuqurlikdagi ierarxiya.
* `INVENTORY.seller` — v2 da `USERS`ga ulanadi (seller roli bo‘lishi kerak). Istasangiz alohida `SELLERS` jadvalini qayta kiritish mumkin.
* `WISHLIST` set ko‘rinishida: odatda `(user_id, product_id)` noyob.
* `ORDER_ITEMS.price` — xarid paytidagi **birlik narx** snapshot.

---

## 2) v1 – Dastlabki ERD (oldingi variant)

```mermaid
erDiagram
  USERS ||--o{ USER_ADDRESS : "manzil bog'"
  USER_ADDRESS }o--|| ADDRESS : "manzillar"

  ROLE ||--o{ USERS : "foydalanuvchilar"

  CART  ||--o{ CART_ITEM : "tovarlar"
  USERS ||--o{ CART : "savatlari"
  CART_ITEM }o--|| PRODUCTS : "savatda"

  USERS ||--o{ WHISHLIST : "xohishlar (typo)"
  WHISHLIST }o--|| PRODUCTS : "saqlangan"

  USERS ||--o{ ORDERS : "buyurtmalar"
  ORDERS ||--|{ ORDERITEMS : "tarkibi"
  ORDERITEMS }o--|| PRODUCTS : "sotib olingan"

  ORDERS ||--o{ PAYMENT : "to'lovlar"

  PRODUCTS }o--|| CATEGORY : "kategoriya"
  PRODUCTS }o--|| SUBCATEGORY : "subkategoriya"
  SUBCATEGORY }o--|| CATEGORY : "bog'liq"

  INVENTORY }o--|| PRODUCTS : "qoldiq"
  INVENTORY }o--|| SELLERS : "sotuvchi"
  SELLERS }o--|| USERS : "akkaunt"

  USERS {
    bigint id PK
    varchar email
    varchar first_name
    varchar last_name
    varchar phone_number
    bigint role_id FK
  }
  ROLE {
    bigint id PK
    varchar name
  }
  ADDRESS {
    bigint id PK
    varchar country
    varchar city
    varchar street
  }
  USER_ADDRESS {
    bigint id PK
    bigint user_id FK
    bigint address_id FK
    timestamp created_at
    timestamp updated_at
  }
  CATEGORY {
    bigint id PK
    varchar name
  }
  SUBCATEGORY {
    bigint id PK
    varchar name
    bigint category_id FK
  }
  PRODUCTS {
    bigint id PK
    varchar name
    text description
    decimal price
    float rating
    bigint category FK
    bigint subcategory FK
    bigint count  %% redundant
  }
  CART {
    bigint id PK
    bigint user_id FK
  }
  CART_ITEM {
    bigint id PK
    bigint cart_id FK
    bigint product_id FK
    int quantity
  }
  WHISHLIST {
    bigint id PK
    bigint user_id FK
    bigint product_id FK
    bigint count  %% keraksiz
    timestamp created_at
  }
  ORDERS {
    bigint id PK
    bigint user_id FK
    varchar status
    decimal total_amount
  }
  ORDERITEMS {
    bigint id PK
    bigint order_id FK
    bigint product_id FK
    int quantity
    decimal price
  }
  PAYMENT {
    bigint id PK
    bigint order_id FK
    decimal amount
    varchar status
    varchar method
  }
  SELLERS {
    bigint id PK
    bigint user_id FK
    varchar name
  }
```
---

![alt text](drawSQL-image-export-2025-08-26.png)

---



**Qisqa izohlar (v1):**

* `CATEGORY` + `SUBCATEGORY` alohida; `PRODUCTS` ikkala ustunga ulanadi.
* `WHISHLIST` jadvali noto‘g‘ri yozilgan (Whishlist) va `count` ustuni mavjud.
* `USER_ADDRESS` alohida link jadvali sifatida ishlatilgan.
* `INVENTORY.seller` → `SELLERS` jadvaliga ulanadi.

---

## 3) Taqqoslash (v2 vs v1)

| Yo‘nalish           | v1                             | v2                                   | Natija                                                   |
| ------------------- | ------------------------------ | ------------------------------------ | -------------------------------------------------------- |
| Kategoriya modeli   | `CATEGORY` + `SUBCATEGORY`     | Yakka `CATEGORY` (self `parent`)     | Soddaroq, cheksiz chuqurlik, kamroq join                 |
| Mahsulot maydonlari | `count` bor, `subcategory` bor | `count` yo‘q, `is_active` bor        | Qoldiq takrorlanmaydi, ko‘rsatishni boshqarish oson      |
| Wishlist            | Nomi xato, `count` bor         | To‘g‘ri nom, `(user, product)` noyob | Toza set semantikasi                                     |
| Manzillar           | `USER_ADDRESS` link jadvali    | `ADDRESS`da `user_id`                | CRUD va so‘rovlar soddalashadi                           |
| Inventarizatsiya    | `SELLERS`ga ulanadi            | `USERS`ga (seller roli) ulanadi      | Alohida seller profili kerak bo‘lsa, `SELLERS`ni saqlang |
| Status tarixi       | Yo‘q                           | `ORDER_STATUS_HISTORY` qo‘shilgan    | Audit va qo‘llab‑quvvatlash uchun qulay                  |

**Qisqa xulosalar:**

* v2 – tozaroq, kengaytirish oson va saqlash/so‘rovlar kamroq bog‘liqlik talab qiladi.
* Agar marketplace kabi ko‘p sotuvchi bo‘lsa va brend/rekvizitlar kerak bo‘lsa, `SELLERS` jadvalini v2 ga ham qo‘shish tavsiya etiladi.
* Variantlar (size/color) kerak bo‘lsa, alohida `PRODUCT_VARIANTS` va `PRODUCT_IMAGES` jadvallarini qo‘shish maqsadga muvofiq.

---

## 4) Biznes qoidalari (SQLsiz, konseptual)

* Email – yagona bo‘lishi kerak (case‑insensitive).
* Savat va buyurtma miqdorlari – musbat.
* Qoldiq – manfiy bo‘lmasin.
* Buyurtma paytida **narx va manzil snapshot** qilinadi (o‘zgarmas yozuv sifatida).
* Bir foydalanuvchiga odatda **bitta faol savat** (ixtiyoriy qoida).

---

## 5) Keyingi qadamlar

* Sellerni modellashtirish bo‘yicha yakuniy qaror (Users vs Sellers).
* Agar reytinglar kerak bo‘lsa, `PRODUCT_REVIEWS` jadvalli modelga o‘ting va `PRODUCTS.rating`ni cache sifatida ishlating.
* Rasm boshqaruvi uchun `PRODUCT_IMAGES` (primary/ordering bilan) joriy eting.
