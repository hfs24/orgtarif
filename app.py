from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'product.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, '_database'):
        g._database.close()





@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('add.html', products=products)

@app.route('/save-product', methods=['POST'])
def save_product():
    if request.method == 'POST':
        productName = request.form['productName']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        discount1 = float(request.form.get('discount1', 0.0))
        discount2 = float(request.form.get('discount2', 0.0))
        tva = float(request.form.get('tva', 0.0))

        price1 = float(price-(price * (discount1 / 100)))
        price2 = float(price1-(price1 * (discount2 / 100)))
        tvatotal = float(price2 * (tva / 100))

        finprice = float((price2 + tvatotal))
        totalprice = float(finprice * quantity)


        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO products (productName,price, discount1, discount2, tva ,quantity,finprice,totalprice) VALUES (?, ?, ?, ?, ?, ?,?,?)",
                       (productName, price, discount1, discount2, tva ,quantity,finprice,totalprice))
        db.commit()

    return redirect(url_for('index'))



@app.route('/OrganisationTarifaire')
def product_list():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('OrganisationTarifaire.html', products=products)



if __name__ == '__main__':
    app.run(debug=True)
