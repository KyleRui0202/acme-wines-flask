"""
    acmewines.utils.pouplate
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This is a module for creating data for test
"""

from random import getrandbits
from faker import Faker

from acmewines.models import Order
from acmewines.configs.validation import birthday_format

def seed_test_data(orders=20):
    """Create and save fake test data (orders) into database"""

    created_data = {'orders': 0}

    fake = Faker()
    for i in range(orders):
        id = fake.random_int(min=1, max=2147483647)
        name = fake.name()
        email = fake.email()
        state = fake.state_abbr()
        zipcode = fake.zipcode()
        if getrandbits(1):
            zipcode = fake.zipcode_plus4()
        birthday = fake.date(birthday_format)
        order = Order(id, name=name, email=email, state=state,
            zipcode=zipcode, birthday=birthday)
        order.save()
        created_data['orders'] += 1

    return created_data
