import random
import os
import csv
from datetime import datetime
from postgres import postgres
filepath = os.getcwd() + "/data.csv"

class User:
    # This code ensures that the .csv database file exists
    header_row = ["ID", "First Name", "Last Name", "Birthday", "Gender", "SSN"]
    if not os.path.exists(filepath):
        with open(filepath, mode="w", newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(header_row)

    def __init__(self, name, social, birthday, gender):
        self.id = self.check_id(filepath)
        self.social = str(social)
        self.first_name = name.split()[0]
        self.last_name = name.split()[1]
        self.birthday = datetime.strptime(birthday, '%m/%d/%Y')
        self.gender = gender
        self.age = self.calculate_age()

        # Checks to see if the provided SSN exists, denies creation if so.

        with open(filepath, mode='a', newline='') as f:
            if not self.social_exists():
                csvwriter = csv.writer(f)
                csvwriter.writerow([self.id, self.first_name, self.last_name,
                                    self.birthday.strftime('%m/%d/%Y'), self.gender, self.social])
            else:
                print('User already exists!')
                exit()

    def social_exists(self):
        with open(filepath, mode='r', newline='') as f:
            csvreader = csv.reader(f)
            next(csvreader)  # Skip the header row
            for row in csvreader:
                if row[5] == self.social:
                    return True
        return False

    def calculate_age(self):
        today = datetime.now()
        return today.year - self.birthday.year - ((today.month, today.day) <
                                                  (self.birthday.month, self.birthday.day))

    # Checks that the random ID isn't already used
    @staticmethod
    def check_id(filepath):
        while True:
            user_id = random.randint(100000000, 999999999)
            with open(filepath, mode='r', newline='') as f:
                csvreader = csv.reader(f)
                next(csvreader)  # Skip the header row
                for row in csvreader:
                    if row[0] == str(user_id):  # Convert ID to string for comparison
                        break
                else:
                    return user_id  # Return the ID if it's not found in the CSV file


bank = postgres(
        host="localhost",
        database="bank",
        user="evanmeeks",
        password="1234",
        port="5432"
    )
bank.connect()
bank.show_table_schema("users")
