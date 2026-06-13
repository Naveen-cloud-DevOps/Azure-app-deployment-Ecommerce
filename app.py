```python
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Database Connection
def get_db():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database=os.environ.get("MYSQL_DATABASE")
    )

# Auto Create Table
def init_db():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(100) NOT NULL,
        customer_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        address TEXT NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    db.commit()
    cursor.close()
    db.close()


PRODUCTS = {
    "beauty": {
        "name": "Beauty Product",
        "price": "$29.99",
        "image": "https://franchiseindia.s3.ap-south-1.amazonaws.com/uploads/news/wi/5a2b878420b31.jpg",
        "description": "Achieve glowing skin with our Radiant Skin Cream."
    },
    "mobiles": {
        "name": "Mobiles",
        "price": "$199.99",
        "image": "https://www.gorefurbo.com/cdn/shop/collections/Refurbished_Mobile_Phones_1.jpg?v=1695978895",
        "description": "Latest mobile phones available."
    },
    "snacks": {
        "name": "Organic Snack Bars",
        "price": "$19.99",
        "image": "https://t3.ftcdn.net/jpg/02/52/38/80/360_F_252388016_KjPnB9vglSCuUJAumCDNbmMzGdzPAucK.jpg",
        "description": "Healthy organic snack bars."
    },
    "grocery": {
        "name": "Grocery",
        "price": "$99.99",
        "image": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiYDATNoFKploew5OMW3etFJIExLq2dOxtNJFVvAiA0rNNB3VLKpAjAwV7SEzg4sIz45Sf_hCc-7MRS4PQM8erBcvLQDel9s2tLmh6s4Lyj7qoHf-rx7oP6F5yhgvPcZHbr09e5sglYptI/w1200-h630-p-k-no-nu/ekiranahome-banner1.jpg",
        "description": "Best grocery products."
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
        product = request.form['product']
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO orders
            (product_name, customer_name, email, address)
            VALUES (%s, %s, %s, %s)
            """,
            (product, name, email, address)
        )

        db.commit()

        cursor.close()
        db.close()

        return redirect(url_for('success', product=product))

    except Exception as e:
        return f"ERROR: {str(e)}"


@app.route('/success')
def success():
    product = request.args.get('product')
    product_data = PRODUCTS.get(product)

    return render_template(
        'success.html',
        product_data=product_data
    )


if __name__ == '__main__':
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
```
