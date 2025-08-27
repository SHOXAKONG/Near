# ERD Hujjati – v1 va v2 taqqoslash

Quyida **v2 (yangilangan)** va **v1 (dastlabki)** sxemalar Mermaid.js `erDiagram` ko‘rinishida berilgan. Keyin qisqa izohlar va taqqoslash jadvali keltiriladi.

---

## 1) v1 – Eski ERD (Birinchi variant)
```mermaid
erDiagram
  ROLE ||--o{ USERS : has

  USERS ||--o{ USER_ADDRESS : links
  USER_ADDRESS }o--|| ADDRESS : addresses

  USERS ||--o{ CART : has
  CART  ||--o{ CART_ITEM : contains
  CART_ITEM }o--|| PRODUCTS : product

  USERS ||--o{ WHISHLIST : has
  WHISHLIST }o--|| PRODUCTS : product

  USERS ||--o{ ORDERS : places
  ORDERS ||--|{ ORDERITEMS : includes
  ORDERITEMS }o--|| PRODUCTS : product

  ORDERS ||--o{ PAYMENT : payments

  PRODUCTS }o--|| CATEGORY : category
  PRODUCTS }o--|| SUBCATEGORY : subcategory
  SUBCATEGORY }o--|| CATEGORY : belongs_to

  INVENTORY }o--|| PRODUCTS : product
  INVENTORY }o--|| SELLERS : seller
  SELLERS }o--|| USERS : account

  USERS {
    int id
    string email
    string first_name
    string last_name
    string phone_number
    int role_id
  }

  ADDRESS {
    int id
    string country
    string city
    string street
  }

  USER_ADDRESS {
    int id
    int user_id
    int address_id
    datetime created_at
    datetime updated_at
  }

  CATEGORY {
    int id
    string name
  }

  SUBCATEGORY {
    int id
    string name
    int category_id
  }

  PRODUCTS {
    int id
    string name
    string description
    float price
    float rating
    int category
    int subcategory
    int count
  }

  CART {
    int id
    int user_id
  }

  CART_ITEM {
    int id
    int cart_id
    int product_id
    int quantity
  }

  WHISHLIST {
    int id
    int user_id
    int product_id
    int count
    datetime created_at
  }

  ORDERS {
    int id
    int user_id
    string status
    float total_amount
  }

  ORDERITEMS {
    int id
    int order_id
    int product_id
    int quantity
    float price
  }

  PAYMENT {
    int id
    int order_id
    float amount
    string status
    string method
  }

  SELLERS {
    int id
    int user_id
    string name
  }

```
---

![alt text](drawSQL-image-export-2025-08-26.png)

---


---

**Qisqa izohlar (v1):**

* `CATEGORY` + `SUBCATEGORY` alohida; `PRODUCTS` ikkala ustunga ulanadi.
* `WHISHLIST` jadvali noto‘g‘ri yozilgan (Whishlist) va `count` ustuni mavjud.
* `USER_ADDRESS` alohida link jadvali sifatida ishlatilgan.
* `INVENTORY.seller` → `SELLERS` jadvaliga ulanadi.

---

## 2) v2 – Yangilangan ERD (Ikkinchi variant)


```mermaid
erDiagram
  USERS ||--o{ ADDRESS : has
  USERS ||--o{ CART : has
  CART  ||--o{ CART_ITEM : contains
  CART_ITEM }o--|| PRODUCTS : product

  USERS ||--o{ WISHLIST : has
  WISHLIST }o--|| PRODUCTS : product

  USERS ||--o{ ORDERS : places
  ORDERS ||--|{ ORDER_ITEMS : includes
  ORDER_ITEMS }o--|| PRODUCTS : product

  ORDERS ||--o{ PAYMENT : payments
  ORDERS ||--o{ ORDER_STATUS_HISTORY : status_history
  ORDER_STATUS_HISTORY }o--o{ USERS : actor

  PRODUCTS }o--|| CATEGORY : category
  CATEGORY ||--o{ CATEGORY : parent

  INVENTORY }o--|| PRODUCTS : product
  INVENTORY }o--|| USERS : seller

  ROLE ||--o{ USERS : has

  USERS {
    int id
    string email
    string first_name
    string last_name
    string phone_number
    int role_id
  }

  ROLE {
    int id
    string name
  }

  ADDRESS {
    int id
    string country
    string city
    string street
    int user_id
  }

  CATEGORY {
    int id
    string name
    int parent
    datetime created_at
    datetime updated_at
  }

  PRODUCTS {
    int id
    string name
    string description
    float price
    float rating
    boolean is_active
    int category
  }

  CART {
    int id
    int user_id
    datetime created_at
  }

  CART_ITEM {
    int id
    int cart_id
    int product_id
    int quantity
  }

  WISHLIST {
    int id
    int user_id
    int product_id
    datetime created_at
  }

  ORDERS {
    int id
    int user_id
    string status
    float total_amount
    datetime created_at
  }

  ORDER_ITEMS {
    int id
    int order_id
    int product_id
    int quantity
    float price
  }

  PAYMENT {
    int id
    int order_id
    float amount
    string status
    string method
    datetime created_at
  }

  ORDER_STATUS_HISTORY {
    int id
    int order_id
    string from_status
    string to_status
    datetime at
    int by_user
  }

  INVENTORY {
    int id
    int seller
    int product
    int stock
  }

```
---

![alt text](<drawSQL-image-export-2025-08-26 (1).png>)



**Qisqa izohlar (v2):**

* `CATEGORY` o‘zini-o‘zi `parent` bilan bog‘laydi → istalgan chuqurlikdagi ierarxiya.
* `INVENTORY.seller` — v2 da `USERS`ga ulanadi (seller roli bo‘lishi kerak). Istasangiz alohida `SELLERS` jadvalini qayta kiritish mumkin.
* `WISHLIST` set ko‘rinishida: odatda `(user_id, product_id)` noyob.
* `ORDER_ITEMS.price` — xarid paytidagi **birlik narx** snapshot.

---

## 3) v3 - Eng Optimal ERD (Uchinchi variant)

```mermaid
erDiagram
  USERS ||--o{ ADDRESS : has
  USERS ||--o{ CART : has
  CART  ||--o{ CART_ITEM : contains
  CART_ITEM }o--|| PRODUCTS : product

  PRODUCTS ||--o{ PRODUCT_VARIANTS : variants
  PRODUCTS }o--|| CATEGORY : category
  CATEGORY ||--o{ CATEGORY : parent

  USERS ||--o{ INVENTORY : sells
  INVENTORY }o--|| PRODUCTS : product

  USERS ||--o{ WISHLIST : bookmarks
  WISHLIST }o--|| PRODUCTS : product

  USERS ||--o{ REVIEW : writes
  REVIEW }o--|| PRODUCTS : of

  USERS ||--o{ ORDERS : places
  ORDERS ||--o{ ORDER_ITEMS : includes
  ORDER_ITEMS }o--|| PRODUCTS : product

  ORDERS ||--o{ ORDER_STATUS_HISTORY : status_history
  ORDER_STATUS_HISTORY }o--|| USERS : by

  ORDERS ||--o{ PAYMENT : payments

  USERS {
    bigint id
    varchar email
    varchar first_name
    varchar last_name
    int     age
    varchar phone_number
    varchar password
    enum    role
  }

  ADDRESS {
    bigint id
    varchar country
    varchar city
    varchar street
    varchar street1
    float   latitude
    float   longitude
    varchar home_number
    bigint  user_id
  }

  CATEGORY {
    bigint id
    varchar name
    timestamp created_at
    timestamp updated_at
    bigint parent
  }

  PRODUCTS {
    bigint id
    varchar name
    text    description
    decimal price
    bigint  category
    varchar product_image
    float   rating
    boolean is_active
    timestamp created_at
  }

  PRODUCT_VARIANTS {
    bigint id
    bigint product_id
    varchar color
    varchar size
    enum    gender
    bigint  stock
    boolean is_active
  }

  INVENTORY {
    bigint id
    bigint product_id
    bigint seller_id
    bigint stock
  }

  WISHLIST {
    bigint id
    bigint product_id
    bigint user_id
    timestamp created_at
  }

  REVIEW {
    bigint id
    bigint product_id
    bigint user_id
    float   rating
    text    comments
    boolean is_moderated
    timestamp created_at
  }

  CART {
    bigint id
    bigint user_id
    timestamp created_at
  }

  CART_ITEM {
    bigint id
    bigint cart_id
    bigint product_id
    bigint quantity
  }

  ORDERS {
    bigint id
    bigint user_id
    enum   status
    decimal total_amount
    timestamp created_at
  }

  ORDER_ITEMS {
    bigint id
    bigint order_id
    bigint product_id
    bigint quantity
    decimal price
  }

  ORDER_STATUS_HISTORY {
    bigint id
    bigint order_id
    varchar from_status
    varchar to_status
    timestamp at
    bigint by_user_id
  }

  PAYMENT {
    bigint id
    bigint order_id
    decimal amount
    enum   status
    enum   method
    timestamp created_at
  }
```

---

![alt text](drawSQL-image-export-2025-08-27.png)

---

**Qisqa izohlar (v3):**

- **Product Variants** qo‘shildi: `color/size/gender` darajasida SKU va **variant-level stock**. `(product_id, color, size, gender)` bo‘yicha `UNIQUE` tavsiya etiladi.
- **Review** jadvali: foydalanuvchi bahosi va sharhi, `is_moderated` bilan moderatsiya; `products.rating` ni agregat/cache sifatida yangilab borish mumkin.
- **Order Status History** saqlanadi: holatlar bo‘yicha to‘liq audit (`from_status → to_status`, `at`, `by_user_id`).
- **CATEGORY** bitta jadval, `parent` orqali self-hierarchy (cheksiz chuqurlik).
- **Inventory**: sotuvchi (`USERS` dagi seller roli) bo‘yicha mahsulot qoldig‘i; marketplace uchun mos.
- **Wishlist**: set semantikasi; `(user_id, product_id)` bo‘yicha `UNIQUE`.
- **Snapshot qoidasi**: `ORDER_ITEMS.price` xarid vaqtidagi **birlik narx** sifatida o‘zgarmas saqlanadi.



# ERD versiyalar taqqoslash (v1, v2, v3)

| Yo‘nalish        | v1                       | v2                             | v3                               |
| ---------------- | ------------------------ | ------------------------------ | -------------------------------- |
| Kategoriya       | `CATEGORY`+`SUBCATEGORY` | Bitta `CATEGORY` (self-parent) | v2 bilan bir xil                 |
| Wishlist         | `WHISHLIST` + `count`    | Toza `WHISHLIST` (set)         | v2 bilan bir xil                 |
| Inventory seller | `SELLERS` jadvali        | `USERS` (rol orqali)           | v2 bilan bir xil                 |
| Status tarixi    | Yo‘q                     | `ORDER_STATUS_HISTORY` bor     | saqlangan                        |
| Variants         | Yo‘q                     | Yo‘q                           | **`PRODUCT_VARIANTS` qo‘shildi** |
| Review           | Yo‘q                     | Yo‘q                           | **`REVIEW` qo‘shildi**           |
| Address          | `USER_ADDRESS` link      | `ADDRESS.user_id`              | saqlangan                        |


---

## 5) Biznes qoidalari (SQLsiz, konseptual)

* Savat va buyurtma miqdorlari – musbat.
* Qoldiq – manfiy bo‘lmasin.
* Buyurtma paytida **narx va manzil snapshot** qilinadi (o‘zgarmas yozuv sifatida).
* Bir foydalanuvchiga odatda **bitta faol savat** (ixtiyoriy qoida).

---

