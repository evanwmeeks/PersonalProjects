import random
import os
import csv
from datetime import datetime
from postgres import postgres

filepath = os.getcwd() + "/data.csv"

class User:
    """
    Represents a user with personal information stored in a .csv database file.

    Attributes:
        id (int): Unique identifier for the user.
        social (str): Social security number of the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        birthday (datetime.datetime): Birthday of the user.
        gender (str): Gender of the user.
        age (int): Age of the user.
    """

    # This code ensures that the .csv database file exists
    header_row = ["ID", "First Name", "Last Name", "Birthday", "Gender", "SSN"]
    if not os.path.exists(filepath):
        with open(filepath, mode="w", newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(header_row)

    def __init__(self, name, social, birthday, gender):
        """
        Initialize a new User object.

        Args:
            name (str): Full name of the user (first name and last name separated by a space).
            social (str): Social security number of the user.
            birthday (str): Birthday of the user in the format "MM/DD/YYYY".
            gender (str): Gender of the user ('M' for male, 'F' for female, etc.).
        """
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
        """
        Check if the social security number already exists in the .csv database file.

        Returns:
            bool: True if the social security number exists, False otherwise.
        """
        with open(filepath, mode='r', newline='') as f:
            csvreader = csv.reader(f)
            next(csvreader)  # Skip the header row
            for row in csvreader:
                if row[5] == self.social:
                    return True
        return False

    def calculate_age(self):
        """
        Calculate the age of the user based on the birthday.

        Returns:
            int: Age of the user.
        """
        today = datetime.now()
        return today.year - self.birthday.year - ((today.month, today.day) <
                                                  (self.birthday.month, self.birthday.day))

    @staticmethod
    def check_id(filepath):
        """
        Generate a random user ID and check if it's already used in the .csv database file.

        Args:
            filepath (str): Path to the .csv database file.

        Returns:
            int: Unique user ID.
        """
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
