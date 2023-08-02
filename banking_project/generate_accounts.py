from user_module import User
import pandas as pd
import random

first_names = pd.read_csv("~/Downloads/baby-names.csv")
last_names_df = pd.read_csv("~/Downloads/surnames.csv")

last_names = last_names_df.iloc[:, 0].tolist()

for index, row in first_names.iterrows():

    first_name = row['name']
    last_name = str(random.choice(last_names)).title()
    full_name = first_name + " " + last_name
    gender = row['sex']
    social = random.randint(111111111, 999999999)
    birthday = f"{random.randint(1, 12)}/{random.randint(1, 28)}/{random.randint(1923,2005)}"

    if gender == 'boy':
        gender = 'Male'

    else:
        gender = 'Female'
    User(full_name, social, birthday, gender)