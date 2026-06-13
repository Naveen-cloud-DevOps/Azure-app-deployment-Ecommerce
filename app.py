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
    },
     "mobiles": {
        "name": "Mobile Phones",
        "price": "$199.99",
        "image": "https://www.gorefurbo.com/cdn/shop/collections/Refurbished_Mobile_Phones_1.jpg?v=1695978895",
        "description": "All types of latest smartphones available with best offers."
    },

    "snacks": {
        "name": "Organic Snack Bars",
        "price": "$19.99",
        "image": "https://t3.ftcdn.net/jpg/02/52/38/80/360_F_252388016_KjPnB9vglSCuUJAumCDNbmMzGdzPAucK.jpg",
        "description": "Healthy snack bars made with natural ingredients."
    },

    "grocery": {
        "name": "Grocery Items",
        "price": "$99.99",
        "image": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiYDATNoFKploew5OMW3etFJIExLq2dOxtNJFVvAiA0rNNB3VLKpAjAwV7SEzg4sIz45Sf_hCc-7MRS4PQM8erBcvLQDel9s2tLmh6s4Lyj7qoHf-rx7oP6F5yhgvPcZHbr09e5sglYptI/w1200-h630-p-k-no-nu/ekiranahome-banner1.jpg",
        "description": "Fresh grocery products delivered at your doorstep."
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
