import unittest

import nose
import random
import string
import redis

from pyla import enteries
from pyla import fields


class QueueEntry(enteries.Entry):
    country = fields.BaseField(index=True)
    category = fields.BaseField(index=True)
    language = fields.BaseField(index=True)
    id = fields.BaseField(primary=True)

def random_key(size):
    """ Generates a random key
    """
    return ''.join(random.choice(string.letters) for _ in range(size))

class TestPyla(unittest.TestCase):

    def setUp(self):
        r = redis.Redis()
        r.flushall()


    def teardown(self):
        r = redis.Redis()
        r.flushall()

    def test_or_filter(self):

        COUNT = 1000
        
        countries = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        languages = ['en', 'ar', 'fr']
        categories = ['cars', 'items', 'property', 'jobs']
        for _ in range(COUNT):
            e = QueueEntry()
            e.country = random.choice(countries)
            e.category = random.choice(categories)
            e.language = random.choice(languages)
            e.id = random_key(32)
            e.save()

        for name, params in (('country', countries), ('language', languages), ('category', categories)):

            nose.tools.assert_equals(
                len(QueueEntry.objects.filter(**dict(((name, params),)))),
                1000
            )
