# Nadega Liquids — Vape Shop

## ✅ Твой Firebase уже настроен!

Конфигурация Firebase уже вставлена во все файлы. Осталось только настроить Firestore Database и залить на GitHub → Vercel.

---

## 🚀 Пошаговая инструкция

### ШАГ 1: Настрой Firestore Database (ОБЯЗАТЕЛЬНО!)

1. Перейди на [console.firebase.google.com](https://console.firebase.google.com)
2. Выбери проект **nadegaliquids**
3. В меню слева нажми **Build** → **Firestore Database**
4. Нажми **"Create database"**
5. Выбери **"Start in test mode"** (можно читать/писать всем — для разработки)
6. Выбери регион: **eur3 (europe-west)** или ближайший к тебе
7. Нажми **Enable**

### ШАГ 2: Создай коллекцию "products"

1. В Firestore Database нажми **"Start collection"**
2. ID коллекции: `products`
3. Нажми **Next**
4. Добавь первый документ (товар):
   - Document ID: нажми **Auto-ID**
   - Поля:
     - `name` (string): "Nadega Blue Ice"
     - `category` (string): "Жидкости"
     - `price` (number): 450
     - `description` (string): "Освежающая голубика со льдом"
     - `image` (string): "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400&h=300&fit=crop"
     - `nicotine` (string): "3mg"
     - `volume` (string): "30ml"
     - `createdAt` (timestamp): нажми на поле → выбери Timestamp → Add field
   - Нажми **Save**

5. Добавь ещё пару товаров для теста (или зайди в админку позже и добавь через неё)

### ШАГ 3: Настрой правила безопасности (ВАЖНО!)

1. В Firestore Database перейди во вкладку **"Rules"**
2. Замени всё на:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /products/{product} {
      allow read: if true;
      allow write: if true;
    }
  }
}
```

3. Нажми **"Publish"**

⚠️ Это открытые правила — любой может читать и писать. Для продакшена нужно добавить аутентификацию.

### ШАГ 4: Создай репозиторий на GitHub

1. Зайди на [github.com/new](https://github.com/new)
2. Repository name: `nadega-liquids`
3. **Оставь всё по умолчанию** (Public, без README)
4. Нажми **Create repository**

### ШАГ 5: Загрузи файлы

Открой терминал в папке с распакованным архивом и выполни:

```bash
git init
git add .
git commit -m "Initial commit with Firebase"
git branch -M main
git remote add origin https://github.com/ТВОЙ_НИК/nadega-liquids.git
git push -u origin main
```

Замени `ТВОЙ_НИК` на свой GitHub username.

### ШАГ 6: Деплой на Vercel

1. Зайди на [vercel.com/new](https://vercel.com/new)
2. Найди и выбери репозиторий `nadega-liquids`
3. **Framework Preset:** выбери `Other`
4. Нажми **Deploy**
5. Жди ~30 секунд

### ШАГ 7: Готово! 🎉

Твой сайт доступен по адресу:
```
https://nadega-liquids.vercel.app
```

---

## 🔐 Админ-панель

- **URL:** `https://nadega-liquids.vercel.app/admin`
- **Пароль:** `admin123` (поменяй в `admin.html`!)

В админке можно:
- Добавлять новые товары (сохраняются в Firebase)
- Удалять товары
- Все изменения видны всем пользователям сразу

---

## ⚠️ ВАЖНО: Что сделать перед запуском

### 1. Добавь свой логотип
Замени файл `logo.jpg` в корне проекта на свой логотип.

### 2. Поменяй пароль админки
В файле `admin.html` найди:
```javascript
const ADMIN_PASS = "admin123";
```
Замени `"admin123"` на свой сложный пароль.

### 3. Проверь правила Firestore (перед продакшеном)
Замени открытые правила на защищённые:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /products/{product} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```
И настрой Firebase Authentication в админке.

---

## 📁 Структура проекта

```
nadega-liquids/
├── index.html          # Главная страница
├── liquids.html        # Каталог жидкостей
├── disposables.html    # Каталог одноразок
├── pods.html           # Каталог POD-систем
├── admin.html          # Админ-панель
├── 404.html            # Страница ошибки
├── vercel.json         # Конфигурация Vercel
├── logo.jpg            # Логотип (замени на свой)
└── README.md           # Этот файл
```

---

## 🔧 Если что-то не работает

### Сайт загружается, но товары не отображаются
- Проверь, что Firestore Database создан и коллекция `products` есть
- Проверь правила безопасности (должно быть `allow read: if true;`)
- Открой консоль браузера (F12 → Console) — посмотри ошибки

### Админка не добавляет товары
- Проверь правила Firestore (`allow write: if true;`)
- Проверь консоль браузера на ошибки CORS

### Vercel не деплоит
- Убедись, что файлы запушены в GitHub
- Проверь, что в Vercel выбран правильный репозиторий

---

© 2026 Nadega Liquids
