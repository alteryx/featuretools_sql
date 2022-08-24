CREATE DATABASE db;
USE db;
CREATE TABLE PRODUCTS(PRODUCT_ID INT, PRODUCT_NAME VARCHAR(20), PRIMARY KEY (PRODUCT_ID));
CREATE TABLE TRANSACTIONS(TRANSACTION_ID INT, PRODUCT_ID INT, PRIMARY KEY (TRANSACTION_ID), FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCTS(PRODUCT_ID));
INSERT INTO PRODUCTS(PRODUCT_ID, PRODUCT_NAME) VALUES (1, 'Car');
INSERT INTO PRODUCTS(PRODUCT_ID, PRODUCT_NAME) VALUES (2, 'Truck');
INSERT INTO PRODUCTS(PRODUCT_ID, PRODUCT_NAME) VALUES (3, 'Plane');
INSERT INTO TRANSACTIONS(TRANSACTION_ID, PRODUCT_ID) VALUES (0, 1);
INSERT INTO TRANSACTIONS(TRANSACTION_ID, PRODUCT_ID) VALUES (1, 1);
INSERT INTO TRANSACTIONS(TRANSACTION_ID, PRODUCT_ID) VALUES (3, 1);
INSERT INTO TRANSACTIONS(TRANSACTION_ID, PRODUCT_ID) VALUES (4, 2);
INSERT INTO TRANSACTIONS(TRANSACTION_ID, PRODUCT_ID) VALUES (2, 3);
INSERT INTO TRANSACTIONS(TRANSACTION_ID, PRODUCT_ID) VALUES (5, 3);
CREATE TABLE NORELATIONSTABLE(ELEM_ID INT, PRIMARY KEY (ELEM_ID));
INSERT INTO NORELATIONSTABLE(ELEM_ID) VALUES (1);
