# create_test_data.py

import csv
from faker import Faker
import random

fake = Faker()

# Liste der drei Buchstaben Abkürzungen europäischer Länder
european_countries = ['AUT', 'BEL', 'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'HUN', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 'MLT', 'NLD', 'POL', 'PRT', 'ROU', 'SVK', 'SVN', 'ESP', 'SWE']

def generate_test_data():
    test_data = []
    for _ in range(25):
        first_name = fake.first_name()
        last_name = fake.last_name()
        nation = random.choice(european_countries)
        birthdate = fake.date_of_birth().strftime('%Y-%m-%d')
        start_number = fake.unique.random_int(min=1, max=50)

        test_data.append({
            'First Name': first_name,
            'Last Name': last_name,
            'Nation': nation,
            'Birthdate': birthdate,
            'Start Number': start_number
        })

    return test_data

def write_test_data_to_csv():
    test_data = generate_test_data()

    with open('test_data.csv', 'w', newline='') as csv_file:
        fieldnames = ['First Name', 'Last Name', 'Nation', 'Birthdate', 'Start Number']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in test_data:
            writer.writerow(row)

if __name__ == "__main__":
    write_test_data_to_csv()
