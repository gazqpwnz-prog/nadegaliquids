from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static')
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'products.json')

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            "categories": ["Жидкости", "Одноразки", "POD-системы"],
            "products": [
                {"id": 1, "name": "Nadega Blue Ice", "category": "Жидкости", "price": 450, "nicotine": "3mg", "volume": "30ml", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400&h=300&fit=crop", "description": "Освежающая голубика со льдом."},
                {"id": 2, "name": "Nadega Mango Tango", "category": "Жидкости", "price": 520, "nicotine": "6mg", "volume": "60ml", "image": "https://images.unsplash.com/photo-1557800636-894a64c1696f?w=400&h=300&fit=crop", "description": "Сочный манго."},
                {"id": 3, "name": "Nadega Strawberry Cream", "category": "Жидкости", "price": 480, "nicotine": "0mg", "volume": "30ml", "image": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400&h=300&fit=crop", "description": "Клубника со сливками."},
                {"id": 4, "name": "Nadega Cola Chill", "category": "Жидкости", "price": 390, "nicotine": "12mg", "volume": "30ml", "image": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400&h=300&fit=crop", "description": "Кола с льдом."},
                {"id": 5, "name": "Nadega Watermelon Burst", "category": "Жидкости", "price": 550, "nicotine": "3mg", "volume": "60ml", "image": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400&h=300&fit=crop", "description": "Арбузный взрыв."},
                {"id": 6, "name": "Elf Bar 600", "category": "Одноразки", "price": 350, "puffs": "600", "flavor": "Blue Razz", "image": "https://images.unsplash.com/photo-1629198688000-71f23e745b6e?w=400&h=300&fit=crop", "description": "Одноразка 600 затяжек."},
                {"id": 7, "name": "HQD Cuvie Plus", "category": "Одноразки", "price": 420, "puffs": "1200", "flavor": "Peach Ice", "image": "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=400&h=300&fit=crop", "description": "1200 затяжек."},
                {"id": 8, "name": "Lost Mary BM600", "category": "Одноразки", "price": 380, "puffs": "600", "flavor": "Triple Mango", "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=300&fit=crop", "description": "Тройной манго."},
                {"id": 9, "name": "Geek Bar Pulse", "category": "Одноразки", "price": 450, "puffs": "900", "flavor": "Grape Ice", "image": "https://images.unsplash.com/photo-1603569283847-aa295f0d016a?w=400&h=300&fit=crop", "description": "900 затяжек."},
                {"id": 10, "name": "Fume Ultra", "category": "Одноразки", "price": 400, "puffs": "1000", "flavor": "Lush Ice", "image": "https://images.unsplash.com/photo-1615486511484-92e172cc416d?w=400&h=300&fit=crop", "description": "1000 затяжек."},
                {"id": 11, "name": "Voopoo Drag X", "category": "POD-системы", "price": 2800, "battery": "18650", "power": "80W", "image": "https://images.unsplash.com/photo-1599639668312-5363a3b5b9f2?w=400&h=300&fit=crop", "description": "80W POD."},
                {"id": 12, "name": "SMOK Nord 5", "category": "POD-системы", "price": 3200, "battery": "2000mAh", "power": "80W", "image": "https://images.unsplash.com/photo-1585776245991-cf89dd7fcad1?w=400&h=300&fit=crop", "description": "2000mAh."},
                {"id": 13, "name": "Vaporesso XROS 3", "category": "POD-системы", "price": 2400, "battery": "1000mAh", "power": "16W", "image": "https://images.unsplash.com/photo-1586227740560-8cf2732c1531?w=400&h=300&fit=crop", "description": "1000mAh."},
                {"id": 14, "name": "Uwell Caliburn A2", "category": "POD-системы", "price": 2100, "battery": "520mAh", "power": "15W", "image": "https://images.unsplash.com/photo-1606229365485-93a3b8ee0385?w=400&h=300&fit=crop", "description": "520mAh."},
                {"id": 15, "name": "Geekvape Wenax M1", "category": "POD-системы", "price": 1900, "battery": "800mAh", "power": "13W", "image": "https://images.unsplash.com/photo-1569529465841-dfecdab7503b?w=400&h=300&fit=crop", "description": "800mAh."}
            ]
        }

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/liquids')
def liquids():
    return send_from_directory('static', 'liquids.html')

@app.route('/disposables')
def disposables():
    return send_from_directory('static', 'disposables.html')

@app.route('/pods')
def pods():
    return send_from_directory('static', 'pods.html')

@app.route('/admin')
def admin():
    return send_from_directory('static', 'admin.html')

@app.route('/api/products')
def get_products():
    return jsonify(load_data())

@app.route('/api/products', methods=['POST'])
def update_products():
    data = request.get_json()
    save_data(data)
    return jsonify({"status": "ok"})

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
