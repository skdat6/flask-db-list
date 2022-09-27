import pytest

from app.main import Item
from app.main import db

def test_new_item():

    item = Item(item='Lapte', category='Dairy', price=10)
    assert item.item == 'Lapte'
    assert item.category == 'Dairy'
    assert item.price == 10




def test_delete():
    item_to_delete = Item.query.get(15)

    with pytest.raises(Exception) as e_info:
        db.session.delete(item_to_delete)
        db.session.commit()
    assert e_info.value.args[0] == "Some error"






