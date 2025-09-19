from daos.product_dao import ProductDAO
from models.product import Product

class ProductController:
    def __init__(self):
        self.dao = ProductDAO()

    def list_products(self):
        return self.dao.select_all()

    def add_product(self, name: str, brand: str, price: float):
        p = Product(id=None, name=name, brand=brand, price=price)
        return self.dao.insert(p)

    def update_product(self, id_: int, name: str, brand: str, price: float):
        p = Product(id=id_, name=name, brand=brand, price=price)
        return self.dao.update(p)

    def delete_product(self, id_: int):
        return self.dao.delete(id_)
