from flask import Flask
from flask import render_template, request, redirect, url_for
from flask import jsonify
import mysql.connector

app = Flask(__name__)

# SGBD configs
DB_HOST="localhost"
DB_USER="root"
DB_DATABASE="CHIP_FRIDGE"
DB_PORT = 3306
DB_PASSWORD=""
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

dbConn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)

@app.route('/')
def home():
    dbConn = None
    cursor = None
    try:
        dbConn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        cursor = dbConn.cursor()

        query = ("SELECT product_name, quantity FROM product;")

        cursor.execute(query)
        print("query executed")
        
        global fridge_data
        fridge_data = {
            "items": [],
            "quantities": []
        }

        for (product_name, quantity) in cursor:
            print("There's {} of {}".format(quantity, product_name))
            fridge_data['items'] += [str(product_name)]
            fridge_data['quantities'] += [quantity]

        shopping_list, notification = fetch_data()
        return render_template('home.html', shopping_list=shopping_list, notification=notification)
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        dbConn.close()

# Route to provide data
@app.route('/data')
def fetch_data():
    shopping_list = {'Milk': 3, 'Bread':7, 'Eggs':2, 'Bananas': 7}
    notification = {
        'title': 'Notification',
        'content': 'Yogurt is about to expire'
    }

    return shopping_list, notification

@app.route('/fetch_fridge_data')
def fetch_fridge_data():
    return jsonify(fridge_data)

if __name__ == '__main__':
    app.run(debug=True)