from postgres import postgres

bank = postgres(
                host="localhost",
                database="bank",
                user="evanmeeks",
                password="1234",
                port="5432"
            )
bank.connect()
bank.query('SELECT * FROM users')