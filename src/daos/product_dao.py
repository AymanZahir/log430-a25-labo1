"""
Product DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv, find_dotenv
from models.product import Product

class ProductDAO:
    def __init__(self):
        load_dotenv(find_dotenv())
        host = os.getenv("MYSQL_HOST")
        db   = os.getenv("MYSQL_DB_NAME")
        usr  = os.getenv("DB_USERNAME")
        pwd  = os.getenv("DB_PASSWORD")
        self.conn = mysql.connector.connect(host=host, database=db, user=usr, password=pwd)
        self.cursor = self.conn.cursor()

    def select_all(self):
        self.cursor.execute("SELECT id, name, brand, price FROM products ORDER BY id ASC")
        rows = self.cursor.fetchall()
        return [Product(*row) for row in rows]

    def insert(self, product: Product):
        self.cursor.execute(
            "INSERT INTO products (name, brand, price) VALUES (%s, %s, %s)",
            (product.name, product.brand, product.price)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, product: Product):
        try:
            sql = """
                UPDATE products
                   SET name=%s,
                       brand=%s,
                       price=%s
                 WHERE id=%s
            """
            self.cursor.execute(sql, (product.name, product.brand, product.price, product.id))
            self.conn.commit()
            return self.cursor.rowcount == 1
        except Error:
            self.conn.rollback()
            return False

    def delete(self, product_id: int):
        try:
            self.cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
            self.conn.commit()
            return self.cursor.rowcount == 1
        except Error:
            self.conn.rollback()
            return False

    # optionnel (utile en tests)
    def delete_all(self):
        try:
            self.cursor.execute("TRUNCATE TABLE products")
            self.conn.commit()
            return True
        except Error:
            self.conn.rollback()
            return False

    def close(self):
        try:
            if getattr(self, "cursor", None):
                self.cursor.close()
            if getattr(self, "conn", None):
                self.conn.close()
        except Exception:
            pass