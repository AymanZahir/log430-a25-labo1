import pytest
from daos.product_dao import ProductDAO
from models.product import Product

@pytest.fixture(scope="module")
def dao():
    d = ProductDAO()
    try:
        d.delete_all()
    except Exception:
        pass

    d.insert(Product(None, "iPhone 15",   "Apple",   999.99))
    d.insert(Product(None, "Galaxy S24",  "Samsung", 899.50))
    d.insert(Product(None, "Pixel 9",     "Google",  799.00))
    yield d

    try:
        d.delete_all()
    except Exception:
        pass

def test_product_select(dao):
    lst = dao.select_all()
    assert len(lst) >= 3
    first = lst[0]
    assert hasattr(first, "id") and hasattr(first, "name") and hasattr(first, "brand") and hasattr(first, "price")
    assert isinstance(first.price, float)

def test_product_insert(dao):
    pid = dao.insert(Product(None, "ThinkPad X1", "Lenovo", 1899.00))
    assert pid is not None and pid > 0
    ids = [p.id for p in dao.select_all()]
    assert pid in ids

def test_product_update(dao):
    p = dao.select_all()[0]
    new_name = p.name + " Pro"
    new_brand = p.brand
    new_price = p.price + 50.0
    ok = dao.update(Product(p.id, new_name, new_brand, new_price))
    assert ok is True

    reloaded = [x for x in dao.select_all() if x.id == p.id][0]
    assert reloaded.name == new_name
    assert abs(reloaded.price - new_price) < 1e-6

def test_product_delete(dao):
    pid = dao.insert(Product(None, "Temp Item", "TempBrand", 1.23))
    assert pid is not None
    ok = dao.delete(pid)
    assert ok is True
    ids = [p.id for p in dao.select_all()]
    assert pid not in ids
