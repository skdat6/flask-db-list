from app.main import Item


def test_new_item():

    item = Item(item='Lapte', category='Dairy', price=10)
    assert item.item == 'Lapte'
    assert item.category == 'Dairy'
    assert item.price == 10

