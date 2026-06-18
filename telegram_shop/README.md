# 🛒 MARKET USS — Telegram Mini App Shop

Полноценный магазин в Telegram с каталогом, корзиной, избранным и админ-панелью.

## 📁 Структура проекта

```
telegram_shop/
├── app.py              # Flask бэкенд (API)
├── bot.py              # Telegram бот
├── static/
│   ├── index.html      # Главная страница Mini App
│   ├── style.css       # Стили
│   └── app.js          # Логика фронтенда
├── data/
│   ├── products.json   # База товаров
│   └── orders.json     # Заказы
└── requirements.txt    # Зависимости
```

## 🚀 Быстрый старт

### 1. Создайте бота в Telegram
1. Напишите [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot`
3. Скопируйте **API токен**

### 2. Настройте проект

```bash
# Установите зависимости
pip install -r requirements.txt

# Отредактируйте конфигурацию в app.py и bot.py:
# - BOT_TOKEN = "ваш_токен"
# - ADMIN_IDS = [ваш_telegram_id]
# - WEB_APP_URL = "https://ваш-домен.com"
```

### 3. Запустите бэкенд
```bash
python app.py
```

### 4. Запустите бота
```bash
python bot.py
```

### 5. Настройте Mini App в BotFather
1. Отправьте `/mybots` → выберите бота
2. Нажмите **Menu Button** → **Configure menu button**
3. Выберите **Web App**
4. Введите URL вашего сайта

## 🛠️ Управление товарами

### Через админ-панель в Mini App:
1. Откройте Mini App
2. Нажмите **Профиль** → откроется админ-панель
3. Заполните форму и нажмите **Добавить товар**
4. Для удаления — нажмите **Удалить** напротив товара

### Через API (curl/Postman):
```bash
# Добавить товар
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -H "X-Telegram-Init-Data: ваш_init_data" \
  -d '{
    "name": "Новый товар",
    "description": "Описание",
    "price": 1000,
    "image": "https://example.com/img.jpg",
    "category": "Устройства",
    "stock": 10
  }'

# Удалить товар
curl -X DELETE http://localhost:5000/api/products/1 \
  -H "X-Telegram-Init-Data: ваш_init_data"
```

## 🌐 Деплой

### Бесплатные варианты:
- **Backend**: [Render](https://render.com), [Railway](https://railway.app), [PythonAnywhere](https://pythonanywhere.com)
- **Frontend**: GitHub Pages, Vercel, Netlify
- **Бот**: Запускайте на том же сервере что и бэкенд

### Важно:
- Для Telegram Mini App нужен **HTTPS**
- Укажите домен в настройках бота через @BotFather

## 🔒 Безопасность

- Проверка `initData` от Telegram (подпись HMAC)
- Только админы могут добавлять/удалять товары
- Заказы отправляются админам в Telegram

## 📱 Скриншоты

Каталог товаров | Корзина | Админ-панель
---|---|---
Красивый grid | Удобный drawer | Простое управление

## 📝 Лицензия

MIT License
