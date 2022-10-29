import re
from collections import defaultdict

import pandas
from django.contrib.auth.models import User
from django.db import IntegrityError


def remove_brackets(s: str | None):
    if s is None:
        return ''

    brackets = re.findall(r"\([^()]+\)", s)
    while brackets:
        for b in brackets:
            s = s.replace(b, '')
        brackets = re.findall(r"\([^()]+\)", s)

    square_brackets = re.findall(r"\[[^\[\]]+\]", s)
    while square_brackets:
        for b in square_brackets:
            s = s.replace(b, '')
        square_brackets = re.findall(r"\[[^\[\]]+\]", s)

    return s.strip()


def create_users(users: dict):
    for u in users:
        user = users[u]
        if user['first_name'] is None or user['last_name'] is None:
            continue

        new_user = User(username=u, **user)
        try:
            new_user.set_password(user['password'])
            new_user.save()
        except IntegrityError:
            print(f'User {u} is already exist!')


def load_files(file_xml, file_csv):
    file_csv = pandas.read_csv(file_csv)

    file_csv = file_csv[file_csv['username'].notna()]
    file_csv = file_csv[file_csv['password'].notna()]

    users = defaultdict()

    for i in range(file_csv.shape[0]):
        username = file_csv.username.array[i]
        username = remove_brackets(username)
        password = file_csv.password.array[i]
        # date_joined = file_csv.date_joined.array[i]

        users[username] = {
            'password': password,
            'first_name': None,
            'last_name': None
        }

    file_xml = pandas.read_xml(file_xml, xpath='//user')

    for i in range(file_xml.shape[0]):
        if file_xml.id.array[i] is None:
            continue

        first_name = file_xml.first_name.array[i]
        first_name = remove_brackets(first_name)
        last_name = file_xml.last_name.array[i]
        last_name = remove_brackets(last_name)

        username = f'{"" if first_name == "" else first_name[0]}.{"" if last_name == "" else last_name}'

        if users.get(username) is None:
            continue

        users[username]['first_name'] = first_name
        users[username]['last_name'] = last_name

    create_users(users)

