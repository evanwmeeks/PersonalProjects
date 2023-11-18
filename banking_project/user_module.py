from postgres import postgres
"""This is functioning solely as a sandbox for postgres.py implementation for the time being"""

bank = postgres(
                host="localhost",
                database="bank",
                user="evanmeeks",
                password="1234",
                port="5432"
            )
bank.connect()
bank.query('SELECT * FROM users')
