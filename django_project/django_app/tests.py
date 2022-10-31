from collections import defaultdict
import datetime

import pandas
from django.test import TestCase
from numpy import NaN

from .utils import remove_brackets, read_csv, read_xml


class DataCollectionTest(TestCase):
    def test_remove_brackets(self):
        self.assertEqual(remove_brackets('test ()'), 'test')
        self.assertEqual(remove_brackets('test []'), 'test')
        self.assertEqual(remove_brackets('test ([]) [()]'), 'test')
        self.assertEqual(remove_brackets('test (asd)'), 'test')
        self.assertEqual(remove_brackets('test [asd]'), 'test')
        self.assertEqual(remove_brackets('test (asd) [asd] ([asd] (asd))'), 'test')

    def test_read_csv(self):
        df = pandas.DataFrame.from_dict({
            'username': ['M.Steam', 'V.Markus', NaN],
            'password': ['ASDf43f#$dsD', NaN, 'DSA4FSFF54w%$#df'],
            'date_joined': [1638700932, 1464014817, NaN],
        })
        self.assertEqual(
            read_csv(df),
            defaultdict(None, {
                'm.steam': {
                    'username': 'M.Steam',
                    'password': 'ASDf43f#$dsD',
                    'first_name': None,
                    'last_name': None,
                    'avatar': None,
                    'date_joined': datetime.datetime(2021, 12, 5, 12, 42, 12)
                }
            }))

    def test_read_xml(self):
        users = defaultdict()
        users.update({
            'm.steam': {
                'username': 'M.Steam',
                'password': 'ASDf43f#$dsD',
                'first_name': None,
                'last_name': None,
                'avatar': None,
                'date_joined': datetime.datetime(2021, 12, 5, 12, 42, 12)
            }
        })

        df = pandas.DataFrame.from_dict({
            'id': ['1', '2', '3'],
            'first_name': ['Max', 'Anton', None],
            'last_name': ['St(dsa53d)eam', None, None],
            'avatar': [
                'https://pbs.twimg.com/media/BcINeMVCIAABeWd.jpg',
                'https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/35af6a41332353.57a1ce913e889.jpg',
                'https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/15345c41332353.57a1ce9141249.jpg'
            ],
        })
        self.assertEqual(
            read_xml(users, df),
            defaultdict(None, {
                'm.steam': {
                    'username': 'M.Steam',
                    'password': 'ASDf43f#$dsD',
                    'first_name': 'Max',
                    'last_name': 'Steam',
                    'avatar': 'https://pbs.twimg.com/media/BcINeMVCIAABeWd.jpg',
                    'date_joined': datetime.datetime(2021, 12, 5, 12, 42, 12)
                }
            }))
