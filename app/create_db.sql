DROP DATABASE IF EXISTS CHIP_FRIDGE;
CREATE DATABASE IF NOT EXISTS CHIP_FRIDGE;
USE CHIP_FRIDGE;

CREATE TABLE product (
    sensor INT NOT NULL UNIQUE,
    quantity INT NOT NULL,
    expiration_date DATE,
    product_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (sensor)
);

CREATE TABLE old_product (
    product_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (product_name)
);