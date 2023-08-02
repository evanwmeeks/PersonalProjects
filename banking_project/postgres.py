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

    def execute_query(self, query):
        """
        Execute a SQL query on the connected PostgreSQL database.

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

            for row in results:
                print(row)

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

    def add_column(self, table_name, column_name, column_type):
        """
        Add a new column to a table in the connected PostgreSQL database.

        Args:
            table_name (str): Name of the table to which the column will be added.
            column_name (str): Name of the new column.
            column_type (str): Data type of the new column (e.g., VARCHAR, INTEGER, BOOLEAN, etc.).
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"

            cursor.execute(query)

            self.connection.commit()
            print(f"Column '{column_name}' added successfully to table '{table_name}'.")

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error adding column: {e}")

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

            headers = ["Column Name", "Data Type", "Max Length", "NOT NULL", "Primary Key"]
            table = tabulate(rows, headers=headers, tablefmt="grid")
            print(f"Schema for table '{table_name}':")
            print(table)

        except psycopg2.Error as e:
            print(f"Error showing table schema: {e}")

    def drop_table(self, table_name):
        """
        Drop a table from the connected PostgreSQL database.

        Args:
            table_name (str): Name of the table to be dropped.
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            query = f"DROP TABLE IF EXISTS {table_name};"

            cursor.execute(query)

            self.connection.commit()
            print(f"Table '{table_name}' dropped successfully!")

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error dropping table: {e}")

    def drop_column(self, table_name, column_name):
        """
        Drop a column from a table in the connected PostgreSQL database.

        Args:
            table_name (str): Name of the table from which the column will be dropped.
            column_name (str): Name of the column to be dropped.
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            query = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"

            cursor.execute(query)

            self.connection.commit()
            print(f"Column '{column_name}' dropped successfully from table '{table_name}'.")

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error dropping column: {e}")

    def new_records(self, table_name, data):
        """
        Insert new records into a table in the connected PostgreSQL database.

        Args:
            table_name (str): Name of the table to insert data into.
            data (tuple): Data to be inserted into the table.
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            query = f"INSERT INTO {table_name} VALUES %s;"

            cursor.execute(query, (data,))

            self.connection.commit()
            print("Data inserted successfully!")

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")

    def delete_record(self, table_name, condition):
        """
        Delete record from a table in the connected PostgreSQL database based on a specified condition.

        Args:
            table_name (str): Name of the table from which records will be deleted.
            condition (str): Condition to identify record to be deleted (e.g., "id = 1" or "name = 'John'").
        """
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            cursor = self.connection.cursor()

            query = f"DELETE FROM {table_name} WHERE {condition};"

            cursor.execute(query)

            self.connection.commit()
            print(f"Rows deleted successfully from table '{table_name}'.")

            cursor.close()
        except psycopg2.Error as e:
            print(f"Error deleting rows: {e}")

    def close_connection(self):
        """
        Close the connection to the PostgreSQL server.
        """
        if self.connection is not None and not self.connection.closed:
            self.connection.close()
            print("Connection closed.")
