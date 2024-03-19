#!/usr/bin/python3

import serial
import mysql.connector

# ser = serial.Serial('/dev/ttyACM0', 9600) # For Raspberry Pi
ser = serial.Serial('/dev/cu.usbmodem142201', 9600)

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

def insert_product(product, quantity, expiration_date, sensor_number):
    # write to database
        cursor = dbConn.cursor()
        if expiration_date == "None":
            query = ("INSERT INTO product (product_name, quantity, sensor) VALUES (%s, %s, %s)")
            cursor.execute(query, (product, quantity, sensor_number))
        else:
            query = ("INSERT INTO product (product_name, quantity, expiration_date, sensor) VALUES (%s, %s, %s, %s)")
            cursor.execute(query, (product, quantity, expiration_date, sensor_number))
        dbConn.commit()
        cursor.close()

def insert_old_product(product):
    cursor = dbConn.cursor()
    query = ("INSERT INTO old_product (product_name) VALUES (%s)")
    cursor.execute(query, (product,))
    dbConn.commit()
    cursor.close()

def delete_old_product(product):
    cursor = dbConn.cursor()
    query = ("DELETE FROM old_product WHERE product_name = %s")
    cursor.execute(query, (product,))
    dbConn.commit()
    cursor.close()

def delete_product(sensor_number):
    cursor = dbConn.cursor()
    query = ("DELETE FROM product WHERE sensor = %s")
    cursor.execute(query, (sensor_number,))
    dbConn.commit()
    cursor.close()

def get_product_information(sensor_number):
    cursor = dbConn.cursor()
    query = ("SELECT product_name, quantity, expiration_date FROM product WHERE sensor = %s")
    cursor.execute(query, (sensor_number,))
    rows = cursor.fetchall()
    cursor.close()
    return (rows[0][0], rows[0][1], rows[0][2])

def is_new_product(product):
    cursor = dbConn.cursor()
    query = ("SELECT * FROM old_product WHERE product_name = %s")
    cursor.execute(query, (product,))
    rows = cursor.fetchall()
    cursor.close()
    return len(rows) != 0

def is_last_product(product):
    cursor = dbConn.cursor()
    query = ("SELECT * FROM product WHERE product_name = %s")
    cursor.execute(query, (product,))
    rows = cursor.fetchall()
    cursor.close()
    return len(rows) == 0

def read_last_product():
    with open('last_product.txt', 'r') as f:
        product = f.readline().strip()
        quantity = f.readline().strip()
        expiration_date = f.readline().strip()
        f.close()
    return (product, quantity, expiration_date)

def write_last_product(product, quantity, expiration_date):
    with open('last_product.txt', 'w') as f:
        f.write(product + '\n')
        f.write(str(quantity) + '\n')
        f.write(str(expiration_date) + '\n')
        f.close()

while 1:
        # read from Arduino
        sensor_number = ser.read().decode("utf-8")
        sensor_state = ser.read().decode("utf-8")
        input = sensor_number + " " + sensor_state
        print ("Read input " + input + " from Arduino")

        if sensor_state == "1":
            product, quantity, expiration_date = read_last_product()

            insert_product(product, quantity, expiration_date, sensor_number)
            if is_new_product(product):
                print("New product", product, "added")
                delete_old_product(product)
        elif sensor_state == "0":
            product_name, quantity, expiration_date = get_product_information(sensor_number)

            print("There's {} of {}".format(quantity, product_name))
            print("Expiration date: {}".format(expiration_date))

            write_last_product(product_name, quantity, expiration_date)

            delete_product(sensor_number)

            if is_last_product(product_name):
                print("Last product", product_name, "removed")
                insert_old_product(product_name)
        

