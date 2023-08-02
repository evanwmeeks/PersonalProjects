import psycopg2
from tabulate import tabulate
class postgres:
    def __init__(self, host, database, user, password, port="5432"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        try:
            # Establish a connection to the PostgreSQL server
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
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            # Create a cursor to interact with the database
            cursor = self.connection.cursor()

            # Execute the query
            cursor.execute(query)

            # Fetch the results (if any)
            results = cursor.fetchall()

            # Process the results (print in this example)
            for row in results:
                print(row)

            # Close the cursor
            cursor.close()
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")

    def add_table(self, table_name, table_definition):
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            # Create a cursor to interact with the database
            cursor = self.connection.cursor()

            # Example CREATE TABLE query
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_definition});"

            # Execute the CREATE TABLE query
            cursor.execute(query)

            # Commit the changes to the database
            self.connection.commit()
            print(f"Table '{table_name}' created successfully!")

            # Close the cursor
            cursor.close()
        except psycopg2.Error as e:
            print(f"Error adding table: {e}")

    def show_tables(self):
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            # Create a cursor to interact with the database
            cursor = self.connection.cursor()

            # Query to fetch table names from information_schema.tables
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"

            # Execute the query
            cursor.execute(query)

            # Fetch the results (if any)
            results = cursor.fetchall()

            # Process the results (print in this example)
            if len(results) == 0:
                print("No tables found in the 'public' schema.")
            else:
                print("Tables in the 'public' schema:")
                for row in results:
                    print(row[0])

            # Close the cursor
            cursor.close()
        except psycopg2.Error as e:
            print(f"Error showing tables: {e}")

    def show_table_schema(self, table_name):
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            # Create a cursor to interact with the database
            cursor = self.connection.cursor()

            # Query to fetch table schema from information_schema.columns
            query = f"""
                SELECT column_name, data_type, character_maximum_length, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s;
            """

            # Execute the query with the table name
            cursor.execute(query, (table_name,))

            # Fetch the results (if any)
            columns = cursor.fetchall()

            # Query to fetch primary key information
            primary_key_query = f"""
                SELECT column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage ku
                  ON tc.constraint_name = ku.constraint_name
                WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY';
            """

            # Execute the primary key query with the table name
            cursor.execute(primary_key_query, (table_name,))
            primary_key = cursor.fetchone()

            # Process the results and create a list of rows for tabulate
            rows = []
            for column in columns:
                column_name, data_type, max_length, is_nullable = column
                is_primary_key = "Yes" if primary_key and column_name == primary_key[0] else "No"
                rows.append([column_name, data_type, str(max_length), is_nullable, is_primary_key])

            # Close the cursor
            cursor.close()

            # Format the results as a table using tabulate
            headers = ["Column Name", "Data Type", "Max Length", "NOT NULL", "Primary Key"]
            table = tabulate(rows, headers=headers, tablefmt="grid")
            print(f"Schema for table '{table_name}':")
            print(table)

        except psycopg2.Error as e:
            print(f"Error showing table schema: {e}")

    def drop_table(self, table_name):
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            # Create a cursor to interact with the database
            cursor = self.connection.cursor()

            # Example DROP TABLE query
            query = f"DROP TABLE IF EXISTS {table_name};"

            # Execute the DROP TABLE query
            cursor.execute(query)

            # Commit the changes to the database
            self.connection.commit()
            print(f"Table '{table_name}' dropped successfully!")

            # Close the cursor
            cursor.close()
        except psycopg2.Error as e:
            print(f"Error dropping table: {e}")

    def new_records(self, table_name, data):
        try:
            if self.connection is None or self.connection.closed:
                print("Connection not established. Call connect() first.")
                return

            # Create a cursor to interact with the database
            cursor = self.connection.cursor()

            # Example INSERT query
            query = f"INSERT INTO {table_name} VALUES %s;"

            # Execute the INSERT query with the data provided
            cursor.execute(query, (data,))

            # Commit the changes to the database
            self.connection.commit()
            print("Data inserted successfully!")

            # Close the cursor
            cursor.close()
        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")

    def close_connection(self):
        if self.connection is not None and not self.connection.closed:
            self.connection.close()
            print("Connection closed.")
