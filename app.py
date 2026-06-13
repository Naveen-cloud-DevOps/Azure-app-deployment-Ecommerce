```python
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

PRODUCTS = {
    "beauty": {
        "name": "Beauty Product",
        "price": "$29.99",
        "image": "https://franchiseindia.s3.ap-south-1.amazonaws.com/uploads/news/wi/5a2b878420b31.jpg",
        "description": "Achieve glowing skin with our Radiant Skin Cream."
    }
}

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

@app.route('/checkout')
def checkout():
    product = request.args.get('product')
    product_data = PRODUCTS.get(product)

    return render_template(
        'checkout.html',
        product=product,
        product_data=product_data
    )

@app.route('/submit-order', methods=['POST'])
def submit_order():
    try:
        db = get_db()
        cursor = db.cursor()

        product = request.form.get('product')
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')

        cursor.execute("""
            INSERT INTO orders
            (product_name, customer_name, email, address)
            VALUES (%s, %s, %s, %s)
        """, (product, name, email, address))

        db.commit()

        cursor.close()
        db.close()

        return redirect(url_for('success', product=product))

    except Exception as e:
        return f"MySQL Error: {str(e)}"

@app.route('/success')
def success():
    product = request.args.get('product')
    product_data = PRODUCTS.get(product)

    return render_template(
        'success.html',
        product_data=product_data
    )

@app.route('/health')
def health():
    return "Application Running Successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```
