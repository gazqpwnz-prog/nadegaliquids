// ======== ИНИЦИАЛИЗАЦИЯ TELEGRAM WEB APP ========
const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

// Цвета из темы Telegram
const theme = tg.themeParams;
document.documentElement.style.setProperty('--tg-bg', theme.bg_color || '#ffffff');
document.documentElement.style.setProperty('--tg-text', theme.text_color || '#000000');
document.documentElement.style.setProperty('--tg-button', theme.button_color || '#2481cc');
document.documentElement.style.setProperty('--tg-button-text', theme.button_text_color || '#ffffff');

// ======== ДАННЫЕ ========
let products = [];
let cart = JSON.parse(localStorage.getItem('cart') || '[]');
let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
let currentCategory = 'all';
let currentProduct = null;
let isAdmin = false;

const API_URL = ''; // Оставьте пустым для того же домена

// ======== ЗАГРУЗКА ТОВАРОВ ========
async function loadProducts() {
    try {
        const res = await fetch(`${API_URL}/api/products`);
        products = await res.json();
        renderCatalog();
        if (isAdmin) renderAdminList();
    } catch (e) {
        console.error('Ошибка загрузки:', e);
        // Демо-данные если сервер недоступен
        products = getDemoProducts();
        renderCatalog();
    }
}

function getDemoProducts() {
    return [
        {
            id: 1,
            name: "VAPORESSO COREX 2.0",
            description: "Картриджи для XROS Series 0.8Ω Mesh Pod. 4 шт в упаковке.",
            price: 1,
            old_price: null,
            image: "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400",
            category: "Расходники",
            stock: 50
        },
        {
            id: 2,
            name: "VILTER PRO BRUSKO",
            description: "Refillable POD System. 1600 mAh, 420 mAh, 2 mL. Aspire.",
            price: 900,
            old_price: null,
            image: "https://images.unsplash.com/photo-1563298723-dcfebaa392e3?w=400",
            category: "Устройства",
            stock: 20
        },
        {
            id: 3,
            name: "BRYZGI Жидкости",
            description: "Набор премиум жидкостей. Разные вкусы.",
            price: 400,
            old_price: null,
            image: "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400",
            category: "Жидкости",
            stock: 100
        },
        {
            id: 4,
            name: "VAPORESSO XROS 5 MINI",
            description: "Новый POD-комплект. Компактный и мощный.",
            price: 1800,
            old_price: 2000,
            image: "https://images.unsplash.com/photo-1563298723-dcfebaa392e3?w=400",
            category: "Устройства",
            stock: 15
        }
    ];
}

// ======== РЕНДЕР КАТАЛОГА ========
function renderCatalog() {
    const catalog = document.getElementById('catalog');
    const search = document.getElementById('search-input').value.toLowerCase();

    let filtered = products;

    if (currentCategory !== 'all') {
        filtered = filtered.filter(p => p.category === currentCategory);
    }

    if (search) {
        filtered = filtered.filter(p => 
            p.name.toLowerCase().includes(search) || 
            p.description.toLowerCase().includes(search)
        );
    }

    if (filtered.length === 0) {
        catalog.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <span>📭</span>
                <p>Товары не найдены</p>
            </div>
        `;
        return;
    }

    catalog.innerHTML = filtered.map((p, i) => `
        <div class="product-card" onclick="openProduct(${p.id})" style="animation-delay: ${i * 0.05}s">
            <img class="product-image" src="${p.image}" alt="${p.name}" 
                 onerror="this.src='https://via.placeholder.com/300'">
            <button class="product-fav" onclick="event.stopPropagation(); toggleFav(${p.id})">
                ${favorites.includes(p.id) ? '❤️' : '🤍'}
            </button>
            <div class="product-info">
                <div>
                    <span class="product-price">${p.price} ₽</span>
                    ${p.old_price ? `<span class="product-old-price">${p.old_price} ₽</span>` : ''}
                </div>
                <div class="product-name">${p.name}</div>
            </div>
        </div>
    `).join('');
}

// ======== ФИЛЬТРЫ ========
function filterCategory(cat) {
    currentCategory = cat;
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    renderCatalog();
}

function searchProducts() {
    renderCatalog();
}

// ======== МОДАЛКА ТОВАРА ========
function openProduct(id) {
    const p = products.find(x => x.id === id);
    if (!p) return;
    currentProduct = p;

    document.getElementById('modal-img').src = p.image;
    document.getElementById('modal-title').textContent = p.name;
    document.getElementById('modal-desc').textContent = p.description;
    document.getElementById('modal-price').textContent = p.price + ' ₽';
    document.getElementById('modal-old-price').textContent = p.old_price ? p.old_price + ' ₽' : '';

    document.getElementById('product-modal').classList.add('active');
}

function closeModal() {
    document.getElementById('product-modal').classList.remove('active');
    currentProduct = null;
}

// ======== КОРЗИНА ========
function addToCartFromModal() {
    if (!currentProduct) return;
    addToCart(currentProduct);
    closeModal();
}

function addToCart(product) {
    const existing = cart.find(item => item.id === product.id);
    if (existing) {
        existing.qty++;
    } else {
        cart.push({ ...product, qty: 1 });
    }
    saveCart();
    updateCartCount();
    tg.showPopup({ title: 'Добавлено', message: `${product.name} в корзине` });
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    saveCart();
    renderCart();
    updateCartCount();
}

function changeQty(id, delta) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.qty += delta;
        if (item.qty <= 0) {
            removeFromCart(id);
            return;
        }
        saveCart();
        renderCart();
        updateCartCount();
    }
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function updateCartCount() {
    const count = cart.reduce((sum, item) => sum + item.qty, 0);
    document.getElementById('cart-count').textContent = count;
}

function openCart() {
    renderCart();
    document.getElementById('cart-drawer').classList.add('active');
}

function closeCart() {
    document.getElementById('cart-drawer').classList.remove('active');
}

function renderCart() {
    const container = document.getElementById('cart-items');
    if (cart.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <span>🛒</span>
                <p>Корзина пуста</p>
            </div>
        `;
        document.getElementById('cart-total').textContent = '0 ₽';
        return;
    }

    container.innerHTML = cart.map(item => `
        <div class="cart-item">
            <img src="${item.image}" alt="${item.name}" onerror="this.src='https://via.placeholder.com/70'">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">${item.price * item.qty} ₽</div>
                <div class="cart-item-qty">
                    <button onclick="changeQty(${item.id}, -1)">−</button>
                    <span>${item.qty}</span>
                    <button onclick="changeQty(${item.id}, 1)">+</button>
                </div>
            </div>
            <button onclick="removeFromCart(${item.id})" style="background:none;border:none;font-size:20px;color:#999;cursor:pointer;">🗑️</button>
        </div>
    `).join('');

    const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
    document.getElementById('cart-total').textContent = total + ' ₽';
}

// ======== ОФОРМЛЕНИЕ ЗАКАЗА ========
async function checkout() {
    if (cart.length === 0) {
        tg.showAlert('Корзина пуста!');
        return;
    }

    const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
    const items = cart.map(i => ({ id: i.id, name: i.name, qty: i.qty, price: i.price }));

    try {
        const headers = { 'Content-Type': 'application/json' };
        if (tg.initData) headers['X-Telegram-Init-Data'] = tg.initData;

        const res = await fetch(`${API_URL}/api/orders`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ items, total })
        });

        if (res.ok) {
            tg.showPopup({
                title: 'Заказ оформлен!',
                message: `Сумма: ${total} ₽\nМы свяжемся с вами для подтверждения.`,
                buttons: [{ id: 'ok', type: 'ok', text: 'Отлично' }]
            });
            cart = [];
            saveCart();
            updateCartCount();
            closeCart();
        } else {
            throw new Error('Server error');
        }
    } catch (e) {
        // Fallback: отправка данных боту
        tg.sendData(JSON.stringify({ action: 'order', items, total }));
        tg.close();
    }
}

// ======== ИЗБРАННОЕ ========
function toggleFav(id) {
    const idx = favorites.indexOf(id);
    if (idx > -1) {
        favorites.splice(idx, 1);
    } else {
        favorites.push(id);
    }
    localStorage.setItem('favorites', JSON.stringify(favorites));
    renderCatalog();
}

function showFavorites() {
    const favProducts = products.filter(p => favorites.includes(p.id));
    const catalog = document.getElementById('catalog');

    if (favProducts.length === 0) {
        catalog.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <span>❤️</span>
                <p>Нет избранных товаров</p>
            </div>
        `;
        return;
    }

    catalog.innerHTML = favProducts.map((p, i) => `
        <div class="product-card" onclick="openProduct(${p.id})" style="animation-delay: ${i * 0.05}s">
            <img class="product-image" src="${p.image}" alt="${p.name}" 
                 onerror="this.src='https://via.placeholder.com/300'">
            <button class="product-fav" onclick="event.stopPropagation(); toggleFav(${p.id})">❤️</button>
            <div class="product-info">
                <div>
                    <span class="product-price">${p.price} ₽</span>
                    ${p.old_price ? `<span class="product-old-price">${p.old_price} ₽</span>` : ''}
                </div>
                <div class="product-name">${p.name}</div>
            </div>
        </div>
    `).join('');
}

// ======== НАВИГАЦИЯ ========
function showPage(page) {
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    event.target.closest('.nav-btn').classList.add('active');

    document.getElementById('admin-panel').style.display = 'none';
    document.querySelector('.catalog').style.display = 'grid';
    document.querySelector('.filters').style.display = 'flex';
    document.querySelector('.search-bar').style.display = 'flex';

    if (page === 'home') {
        renderCatalog();
    } else if (page === 'favorites') {
        showFavorites();
    }
}

// ======== АДМИН-ПАНЕЛЬ ========
function toggleAdmin() {
    // Проверка: только определённые пользователи
    const user = tg.initDataUnsafe?.user;
    // Для демо: любой может открыть. В продакшене проверяйте ID!
    isAdmin = !isAdmin;

    if (isAdmin) {
        document.querySelector('.catalog').style.display = 'none';
        document.querySelector('.filters').style.display = 'none';
        document.querySelector('.search-bar').style.display = 'none';
        document.getElementById('admin-panel').style.display = 'block';
        renderAdminList();
    } else {
        showPage('home');
        document.querySelector('.nav-btn').classList.add('active');
    }
}

function renderAdminList() {
    const container = document.getElementById('admin-products');
    container.innerHTML = products.map(p => `
        <div class="admin-product">
            <img src="${p.image}" onerror="this.src='https://via.placeholder.com/60'">
            <div class="admin-product-info">
                <h4>${p.name}</h4>
                <span>${p.price} ₽ | ${p.category} | Остаток: ${p.stock}</span>
            </div>
            <button onclick="deleteProduct(${p.id})">Удалить</button>
        </div>
    `).join('');
}

async function addProduct() {
    const product = {
        name: document.getElementById('admin-name').value,
        description: document.getElementById('admin-desc').value,
        price: document.getElementById('admin-price').value,
        old_price: document.getElementById('admin-old-price').value || null,
        image: document.getElementById('admin-image').value,
        category: document.getElementById('admin-category').value,
        stock: document.getElementById('admin-stock').value
    };

    if (!product.name || !product.price) {
        tg.showAlert('Заполните название и цену!');
        return;
    }

    try {
        const headers = { 'Content-Type': 'application/json' };
        if (tg.initData) headers['X-Telegram-Init-Data'] = tg.initData;

        const res = await fetch(`${API_URL}/api/products`, {
            method: 'POST',
            headers,
            body: JSON.stringify(product)
        });

        if (res.ok) {
            tg.showPopup({ title: 'Готово', message: 'Товар добавлен!' });
            // Очистка формы
            document.querySelectorAll('.admin-form input').forEach(i => i.value = '');
            loadProducts();
        } else {
            throw new Error('Unauthorized');
        }
    } catch (e) {
        // Демо-режим: добавляем локально
        const newId = Math.max(...products.map(p => p.id), 0) + 1;
        products.push({ ...product, id: newId, visible: true, price: Number(product.price), stock: Number(product.stock) });
        renderCatalog();
        renderAdminList();
        tg.showPopup({ title: 'Готово (демо)', message: 'Товар добавлен локально. Для сохранения на сервере настройте бэкенд.' });
    }
}

async function deleteProduct(id) {
    if (!confirm('Удалить товар?')) return;

    try {
        const headers = {};
        if (tg.initData) headers['X-Telegram-Init-Data'] = tg.initData;

        const res = await fetch(`${API_URL}/api/products/${id}`, {
            method: 'DELETE',
            headers
        });

        if (res.ok) {
            loadProducts();
        } else {
            throw new Error('Unauthorized');
        }
    } catch (e) {
        products = products.filter(p => p.id !== id);
        renderCatalog();
        renderAdminList();
        tg.showPopup({ title: 'Готово (демо)', message: 'Товар удалён локально.' });
    }
}

// ======== ЗАКРЫТИЕ ПРИЛОЖЕНИЯ ========
function closeApp() {
    tg.close();
}

// ======== ИНИЦИАЛИЗАЦИЯ ========
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    updateCartCount();

    // Настройка кнопки "Назад" Telegram
    tg.BackButton.onClick(() => {
        closeCart();
        closeModal();
    });
});
