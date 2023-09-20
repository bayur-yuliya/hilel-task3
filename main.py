import csv

import requests
from faker import Faker
from flask import Flask, request

app = Flask(__name__)
fake = Faker()


@app.route('/requrements')
def index():
    try:

        requirements_packages = ''

        with open('requirements.txt', 'r') as file:
            requirements = file.readlines()

            for package in requirements:
                requirements_packages += package + "<br>"

        return requirements_packages

    except FileNotFoundError:
        return "<h2>Немає такого файлу</h2>"


@app.route('/users/generate')
def faker_func():

    query_param = request.args.get('query')

    if query_param is not None:

        try:
            count_users = int(request.args.get('query'))
        except ValueError:
            return "<h2>Помилка, введіть число</h2>"

    else:
        count_users = 100

    fake_data = ""

    for i in range(count_users):
        fake_data += str(i + 1) + ".   " + fake.name() + ' - ' + fake.email() + "<br>"

    return fake_data


@app.route('/mean/')
def mean():
    try:
        height_cm_sum = 0
        weight_kg_sum = 0
        i = 0

        with open('hw.csv', 'r') as file:
            reader = csv.reader(file)

            for line in reader:
                if len(line) > 0:

                    if line[0] == "Index":
                        continue
                    else:
                        height_cm_sum += float(line[1])
                        weight_kg_sum += float(line[2])
                        i += 1

        average_height_cm = round(float(height_cm_sum/i) * 2.54, 2)
        average_weight_kg = round(float(weight_kg_sum/i) / 2.205, 2)

        return f"Середній зріст: {average_height_cm}, середня вага: {average_weight_kg}"

    except FileNotFoundError:
        return "<h2>Не найден файл</h2>"


@app.route('/space/')
def space():
    query = requests.get('http://api.open-notify.org/astros.json')

    if query.json()['number']:
        a = query.json()['number']
    elif query.json()['people']:
        a = len(query.json()['people'])
    else:
        return "<h2>Невказвна кількість космонавтів на орбіті</h2>"

    return f' Kількість космонавтів на орбіті: {a}'


if __name__ == '__main__':
    app.run(debug=True)
