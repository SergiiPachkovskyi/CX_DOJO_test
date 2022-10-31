import datetime
import re
from collections import defaultdict

from django.contrib.auth.models import User
from django.db import IntegrityError
import pandas
from pandas import DataFrame

from .models import Profile


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

    s = s.replace('()', '')
    s = s.replace('[]', '')

    return s.strip()


def read_csv(file_csv: DataFrame):
    file_csv = file_csv[file_csv['username'].notna()]
    file_csv = file_csv[file_csv['password'].notna()]

    users = defaultdict()

    for i in range(file_csv.shape[0]):
        username = file_csv.username.array[i]
        username = remove_brackets(username)
        password = file_csv.password.array[i]

        user_data = {
            'username': username,
            'password': password,
            'first_name': None,
            'last_name': None,
            'avatar': None
        }

        date_joined = file_csv.date_joined.array[i]
        try:
            date_joined = datetime.datetime.fromtimestamp(date_joined)
            user_data.update({'date_joined': date_joined})
        except ValueError:
            pass

        users[username.lower()] = user_data

    return users


def read_xml(users: dict, file_xml: DataFrame):
    for i in range(file_xml.shape[0]):
        if file_xml.id.array[i] is None:
            continue

        first_name = file_xml.first_name.array[i]
        first_name = remove_brackets(first_name)
        last_name = file_xml.last_name.array[i]
        last_name = remove_brackets(last_name)
        avatar = file_xml.avatar.array[i]

        username = f'{"" if first_name == "" else first_name[0] + "."}{"" if last_name == "" else last_name}'
        username = username.lower()

        if users.get(username) is None:
            continue

        users[username]['first_name'] = first_name
        users[username]['last_name'] = last_name
        users[username]['avatar'] = avatar

    return users


def create_users(users: dict):
    for u in users:
        user = users[u]
        if user['first_name'] is None or user['last_name'] is None:
            continue

        new_user = User(
            username=user['username'],
            first_name=user['first_name'],
            last_name=user['last_name'],
        )
        if user.get('date_joined'):
            new_user.date_joined = user['date_joined']
        try:
            new_user.set_password(user['password'])
            new_user.save()

            new_profile = Profile(user=new_user, image_url=user['avatar'])
            new_profile.save()
        except IntegrityError:
            print(f'User {user["username"]} is already exist!')


def load_files(file_csv, file_xml):
    file_csv = pandas.read_csv(file_csv)
    users = read_csv(file_csv)

    file_xml = pandas.read_xml(file_xml, xpath='//user')
    users = read_xml(users, file_xml)

    create_users(users)
