#!/usr/bin/python3

import serial
import mysql.connector

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

# ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
ser = serial.Serial('/dev/cu.usbmodem14101', 9600)

while 1:
        # read from Arduino
        sensor_number = ser.read().decode("utf-8")
        sensor_state = ser.read().decode("utf-8")
        input = sensor_number + " " + sensor_state
        print ("Read input " + input + " from Arduino")

        if sensor_state == "1":
            with open('last_product.txt', 'r') as f:
                product = f.readline()
                quantity = f.readline()
                expiration_date = f.readline()
                f.close()
            # write to database
            cursor = dbConn.cursor()
            if expiration_date == "\n":
                query = ("INSERT INTO product (product_name, quantity, sensor) VALUES (%s, %s, %s)")
                cursor.execute(query, (product, quantity, sensor_number))
            else:
                query = ("INSERT INTO product (product_name, quantity, expiration_date, sensor) VALUES (%s, %s, %s, %s)")
                cursor.execute(query, (product, quantity, expiration_date, sensor_number))
            dbConn.commit()
            cursor.close()
        elif sensor_state == "0":
            cursor = dbConn.cursor()
            query = ("SELECT product_name, quantity, expiration_date FROM product WHERE sensor = %s")
            cursor.execute(query, (sensor_number,))
            rows = cursor.fetchall()
            cursor.close()

            product_name = rows[0][0]
            quantity = rows[0][1]
            expiration_date = rows[0][2]
            print("There's {} of {}".format(quantity, product_name))
            print("Expiration date: {}".format(expiration_date))

            # write to last_product.txt
            with open('last_product.txt', 'w') as f:
                f.write(product_name)
                f.write(str(quantity) + '\n')
                f.write(str(expiration_date) + '\n')
                f.close()

            cursor = dbConn.cursor()
            query = ("DELETE FROM product WHERE sensor = %s")
            cursor.execute(query, (sensor_number,))
            dbConn.commit()
            cursor.close()
        

