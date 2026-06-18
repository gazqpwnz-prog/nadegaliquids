
import os
import json
import hashlib
import hmac
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ======== КОНФИГУРАЦИЯ ========
# ЗАМЕНИТЕ НА СВОЙ ТОКЕН ОТ @BotFather
BOT_TOKEN = "8906080480:AAFQB5dZcbVlubxT9pPxLxz5XmlF1kP4jT0"
ADMIN_IDS = [6602618961]  # Добавьте сюда Telegram ID админов

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')

# ======== УТИЛИТЫ ========
def load_json(filepath, default=None):
    if default is None:
        default = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def init_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(PRODUCTS_FILE):
        save_json(PRODUCTS_FILE, [])
    if not os.path.exists(ORDERS_FILE):
        save_json(ORDERS_FILE, [])

init_data()

# ======== ПРОВЕРКА INIT DATA (безопасность Telegram) ========
def validate_init_data(init_data_str):
    """Проверяет подпись initData от Telegram WebApp"""
    try:
        parsed = dict(x.split('=') for x in init_data_str.split('&'))
        received_hash = parsed.pop('hash')
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        return computed_hash == received_hash
    except Exception:
        return False

def get_user_from_init_data(init_data_str):
    """Извлекает данные пользователя из initData"""
    try:
        parsed = dict(x.split('=') for x in init_data_str.split('&'))
        user = json.loads(parsed.get('user', '{}'))
        return user
    except Exception:
        return {}

# ======== API: ТОВАРЫ ========
@app.route('/api/products', methods=['GET'])
def get_products():
    """Получить список всех товаров"""
    products = load_json(PRODUCTS_FILE)
    # Фильтруем скрытые товары для обычных пользователей
    return jsonify([p for p in products if p.get('visible', True)])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Получить один товар"""
    products = load_json(PRODUCTS_FILE)
    for p in products:
        if p['id'] == product_id and p.get('visible', True):
            return jsonify(p)
    return jsonify({"error": "Товар не найден"}), 404

@app.route('/api/products', methods=['POST'])
def add_product():
    """Добавить товар (требует авторизации админа)"""
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    if not validate_init_data(init_data):
        return jsonify({"error": "Unauthorized"}), 401

    user = get_user_from_init_data(init_data)
    if user.get('id') not in ADMIN_IDS:
        return jsonify({"error": "Forbidden"}), 403

    data = request.json
    products = load_json(PRODUCTS_FILE)

    new_id = max([p['id'] for p in products], default=0) + 1
    product = {
        "id": new_id,
        "name": data.get('name', ''),
        "description": data.get('description', ''),
        "price": float(data.get('price', 0)),
        "old_price": float(data.get('old_price', 0)) if data.get('old_price') else None,
        "image": data.get('image', ''),
        "category": data.get('category', ''),
        "stock": int(data.get('stock', 0)),
        "visible": True,
        "created_at": datetime.now().isoformat()
    }
    products.append(product)
    save_json(PRODUCTS_FILE, products)
    return jsonify(product), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Обновить товар"""
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    if not validate_init_data(init_data):
        return jsonify({"error": "Unauthorized"}), 401

    user = get_user_from_init_data(init_data)
    if user.get('id') not in ADMIN_IDS:
        return jsonify({"error": "Forbidden"}), 403

    data = request.json
    products = load_json(PRODUCTS_FILE)

    for p in products:
        if p['id'] == product_id:
            p.update({k: v for k, v in data.items() if k != 'id'})
            save_json(PRODUCTS_FILE, products)
            return jsonify(p)
    return jsonify({"error": "Товар не найден"}), 404

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Удалить товар (мягкое удаление — скрываем)"""
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    if not validate_init_data(init_data):
        return jsonify({"error": "Unauthorized"}), 401

    user = get_user_from_init_data(init_data)
    if user.get('id') not in ADMIN_IDS:
        return jsonify({"error": "Forbidden"}), 403

    products = load_json(PRODUCTS_FILE)
    for p in products:
        if p['id'] == product_id:
            p['visible'] = False
            save_json(PRODUCTS_FILE, products)
            return jsonify({"success": True})
    return jsonify({"error": "Товар не найден"}), 404

# ======== API: ЗАКАЗЫ ========
@app.route('/api/orders', methods=['POST'])
def create_order():
    """Создать заказ"""
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user = get_user_from_init_data(init_data) if init_data else {}

    data = request.json
    orders = load_json(ORDERS_FILE)

    new_id = max([o['id'] for o in orders], default=0) + 1
    order = {
        "id": new_id,
        "user_id": user.get('id'),
        "username": user.get('username'),
        "items": data.get('items', []),
        "total": data.get('total', 0),
        "status": "new",
        "created_at": datetime.now().isoformat()
    }
    orders.append(order)
    save_json(ORDERS_FILE, orders)
    return jsonify(order), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Получить заказы (админ)"""
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    if not validate_init_data(init_data):
        return jsonify({"error": "Unauthorized"}), 401

    user = get_user_from_init_data(init_data)
    if user.get('id') not in ADMIN_IDS:
        return jsonify({"error": "Forbidden"}), 403

    orders = load_json(ORDERS_FILE)
    return jsonify(orders)

# ======== СТАТИЧЕСКИЕ ФАЙЛЫ ========
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

# ======== ЗАПУСК ========
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
