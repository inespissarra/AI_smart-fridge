# sudo systemctl restart mariadb.service
sudo mysql < create_db.sql
sudo mysql CHIP_FRIDGE < populate.sql

# pip install mysql-connector-python