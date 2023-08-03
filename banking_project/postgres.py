import random
import psycopg2
from tabulate import tabulate

class postgres:
    def __init__(self, host, database, user, password, port="5432"):
        """
        Initialize a PostgreSQL database connection.

        Args:
            host (str): Hostname or IP address of the PostgreSQL server.
            database (str): Name of the database to connect to.
            user (str): Username for the database connection.
            password (str): Password for the database connection.
            port (str, optional): Port number for the database connection. Defaults to "5432".
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        """
        Establish a connection to the PostgreSQL server.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("Connection to PostgreSQL successful!")
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def query(self, query):
        """
        Execute a SQL query on the connected PostgreSQL database and print the results in a table format.

        Args:
            query (str): SQL query to be executed.
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            cursor.execute(query)

            results = cursor.fetchall()

            headers = [desc[0] for desc in cursor.description]
            table = tabulate(results, headers=headers, tablefmt="grid")
            print(table)

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")

    def add_table(self, table_name, table_definition):
        """
        Create a new table in the connected PostgreSQL database.

        Args:
            table_name (str): Name of the new table.
            table_definition (str): Definition of the new table's columns and data types.
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_definition});"

            cursor.execute(query)

            self.connection.commit()
            print(f"Table '{table_name}' created successfully!")

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error adding table: {e}")

    def add_columns(self, table_name, column_data):
        """
        Add new columns to a table in the connected PostgreSQL database.

        Args:
            table_name (str): Name of the table to which the columns will be added.
            column_data (list): List of tuples containing column name and data type pairs.
                                Example: [('column1', 'VARCHAR'), ('column2', 'INTEGER'), ...]
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            for column_name, column_type in column_data:
                query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"
                cursor.execute(query)

            self.connection.commit()
            print(f"Columns added successfully to table '{table_name}'.")

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error adding columns: {e}")

    def update_columns(self, table_name, column_name_mapping):
        """
        Update the names and data types of columns in a table in the connected PostgreSQL database.

        Args:
            table_name (str): Name of the table in which the columns will be updated.
            column_name_mapping (dict): Dictionary containing the mapping of old column names to new column names
                                        and new data types.
                                        Example: {'old_column_name1': ('new_column_name1', 'NEW_DATA_TYPE1'),
                                                  'old_column_name2': ('new_column_name2', 'NEW_DATA_TYPE2'),
                                                  ...}

        Returns:
            None: This method has no return value.
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            for old_column_name, (new_column_name, new_data_type) in column_name_mapping.items():
                try:
                    # Rename column name
                    rename_query = f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name};"
                    cursor.execute(rename_query)
                except psycopg2.Error as e:
                    # Suppress the error and continue if column name change fails
                    print(f"Error renaming column '{old_column_name}' to '{new_column_name}': {e}")

                # Update column data type for the renamed column
                update_query = f"ALTER TABLE {table_name} ALTER COLUMN {new_column_name} TYPE {new_data_type};"
                cursor.execute(update_query)

                # Add NOT NULL constraint to the renamed column
                not_null_query = f"ALTER TABLE {table_name} ALTER COLUMN {new_column_name} SET NOT NULL;"
                cursor.execute(not_null_query)

            self.connection.commit()
            print(f"Columns in table '{table_name}' updated successfully.")

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error updating columns: {e}")

    def show_tables(self):
        """
        Show a list of tables in the connected PostgreSQL database.
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"

            cursor.execute(query)

            results = cursor.fetchall()

            if len(results) == 0:
                print("No tables found in the 'public' schema.")
            else:
                print("Tables in the 'public' schema:")
                for row in results:
                    print(row[0])

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error showing tables: {e}")

    def show_table_schema(self, table_name):
        """
        Show the schema of a specific table in the connected PostgreSQL database.

        Args:
            table_name (str): Name of the table to display the schema for.
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            query = f"""
                SELECT column_name, data_type, character_maximum_length, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s;
            """

            cursor.execute(query, (table_name,))

            columns = cursor.fetchall()

            primary_key_query = f"""
                SELECT column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage ku
                  ON tc.constraint_name = ku.constraint_name
                WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY';
            """

            cursor.execute(primary_key_query, (table_name,))
            primary_key = cursor.fetchone()

            rows = []
            for column in columns:
                column_name, data_type, max_length, is_nullable = column
                is_primary_key = "Yes" if primary_key and column_name == primary_key[0] else "No"
                rows.append([column_name, data_type, str(max_length), is_nullable, is_primary_key])

            cursor.close()

            headers = ["Column Name", "Data Type", "Max Length", "OPTIONAL", "Primary Key"]
            table = tabulate(rows, headers=headers, tablefmt="grid")
            print(f"Schema for table '{table_name}':")
            print(table)

        except psycopg2.Error as e:
            print(f"Error showing table schema: {e}")

    def new_customer(self, first_name, last_name, email,
                     date_of_birth, phone_number, phone_type, ssn, gender,
                     street_number, street_name, city, state, zip_code):
        """
        Create a new customer record in the "Users" table.

        Args:
            first_name (str): First name of the customer.
            last_name (str): Last name of the customer.
            email (str): Email address of the customer.
            date_of_birth (str): Date of birth of the customer in the format 'YYYY-MM-DD'.
            phone_number (str): Contact number of the customer.
            phone_type (str): type of phone number: Home, Work or Cell.
            ssn (str): Social Security Number of the customer.
            gender (str): Gender of the customer.
            street_number (str): Street number of the customer's address.
            street_name (str): Street name of the customer's address.
            city (str): City of the customer's address.
            state (str): State of the customer's address.
            zip_code (str): Zip code of the customer's address.

        Returns:
            None: This method has no return value.
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            # Example INSERT query for creating a new record in the "Users" table
            query = """
                INSERT INTO users (user_id,first_name, last_name, 
                email, date_of_birth, phone_number, phone_type, ssn, 
                gender, street_number, street_name, city, state, zip_code)
                VALUES (uuid_generate_v4(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            # Execute the INSERT query with the provided values
            cursor.execute(query, (first_name, last_name, email, date_of_birth, phone_number, phone_type,
                                   ssn, gender, street_number, street_name, city, state, zip_code))

            self.connection.commit()
            print("New customer record created successfully!")

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error creating new customer record: {e}")

    def create_new_checking_account(self, user_id, overdraft_limit=None):
        """
        Create a new checking account in the 'checking_accounts' table.

        Args:
            user_id (str): The user ID of the associated user.
            overdraft_limit (int, optional): The overdraft limit for the checking account. Defaults to None.

        Returns:
            None: This method has no return value.
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            # If the overdraft_limit is not provided, set it to NULL
            overdraft_limit = overdraft_limit if overdraft_limit is not None else 'NULL'

            account_number = random.randint(111111111, 999999999)

            # Create the SQL query
            query = f"""
                INSERT INTO checking_accounts (checking_id, account_number, account_status, overdraft_limit, user_id)
                VALUES (uuid_generate_v4(), %s, 'Active', {overdraft_limit}, %s);
            """

            # Execute the query with the provided values
            cursor.execute(query, (account_number, user_id))

            # Commit the changes to the database
            self.connection.commit()
            print("New checking account created successfully!")

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error creating checking account: {e}")

    def delete_user(self, user_id):
        """
        Delete a user from the 'users' table based on their user ID.

        Args:
            user_id (int): The user ID of the user to be deleted.
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            # Check if the user with the given ID exists in the 'users' table
            check_query = f"SELECT * FROM users WHERE id = %s;"
            cursor.execute(check_query, (user_id,))
            user_data = cursor.fetchone()

            if user_data is None:
                print(f"User with ID {user_id} not found.")
                return

            # Execute the DELETE query
            delete_query = f"DELETE FROM users WHERE id = %s;"
            cursor.execute(delete_query, (user_id,))
            self.connection.commit()

            print(f"User with ID {user_id} deleted successfully.")

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error deleting user: {e}")

    def close_connection(self):
        """
        Close the connection to the PostgreSQL server.
        """
        if self.connection is not None and not self.connection.closed:
            self.connection.close()
            print("Connection closed.")
