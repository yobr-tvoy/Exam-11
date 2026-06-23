import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATA_FILE = 'restaurants.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    restaurants = load_data()
    return render_template('index.html', restaurants=restaurants)

@app.route('/add', methods=['POST'])
def add_restaurant():
    name = request.form.get('name')
    cuisine = request.form.get('cuisine')
    rating = request.form.get('rating')
    address = request.form.get('address')

    if name and cuisine and rating and address:
        restaurants = load_data()
        restaurants.append({
            'name': name,
            'cuisine': cuisine,
            'rating': float(rating) if rating else 0.0,
            'address': address
        })
        save_data(restaurants)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_restaurant(index):
    restaurants = load_data()
    if 0 <= index < len(restaurants):
        restaurants.pop(index)
        save_data(restaurants)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
