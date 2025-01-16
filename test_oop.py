"""
Протестируйте классы из модуля homework/models.py
"""

import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()

@pytest.fixture
def product_sq():
    return Product("notebook", 50, "This is a notebook", 10)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity - 1)
        assert product.check_quantity(product.quantity)
        assert not product.check_quantity(product.quantity + 1)


    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        quantity = product.quantity
        product.buy(2)
        assert product.quantity == quantity - 2

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(product.quantity + 1)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_product_add(self, cart, product):
        # TODO напишите проверки на метод buy
        cart.add_product(product, 4)
        assert cart.products[product] == 4

    def test_product_not_enough(self, cart, product_sq):
        # TODO напишите проверки на метод buy
        with pytest.raises(ValueError):
            cart.add_product(product_sq, 11)

    def test_remove_item(self, cart, product):
        cart.add_product(product, 4)
        cart.remove_product(product, 3)
        assert cart.products[product] == 1

    def test_add_twice(self, cart, product):
        cart.add_product(product,1)
        cart.add_product(product,1)
        assert cart.products[product] == 2

    def test_clear_empty_cart(self, cart):
        cart.clear()
        assert not cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 3)
        cart.clear()
        assert not cart.products

    def test_remove_one_product(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product)
        assert not cart.products

    def test_remove_bigger_qty(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 6)
        assert not cart.products

    def test_remove_same_qty(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 5)
        assert not cart.products

    def test_remove_one_product_from_cart_of_two(self, cart, product, product_sq):
        cart.add_product(product, 5)
        cart.add_product(product_sq, 1)
        cart.remove_product(product)
        assert product not in cart.products
        assert product_sq in cart.products

    def test_remove_two_products(self, cart, product, product_sq):
        cart.add_product(product, 5)
        cart.add_product(product_sq, 1)

        cart.remove_product(product)
        assert product_sq in cart.products

        cart.remove_product(product_sq)
        assert not cart.products

    def test_price_count(self, cart, product, product_sq):
        cart.add_product(product_sq, 5)
        cart.add_product(product, 4)
        assert cart.get_total_price() == 5 * product_sq.price + 4 * product.price

    def test_buy_cart(self, cart, product):
        old_quantity = product.quantity
        cart.add_product(product, 10)
        cart.buy()
        assert product.quantity == old_quantity - 10

    def test_not_buying(self, cart, product_sq):
        with pytest.raises(ValueError):
            cart.add_product(product_sq, 12)
            cart.buy()

    def test_buy_2pr_cart(self, cart, product, product_sq):
        cart.add_product(product, 10)
        with pytest.raises(ValueError):
            cart.add_product(product_sq, 12)
            cart.buy()