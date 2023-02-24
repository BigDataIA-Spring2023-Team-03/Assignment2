import sqlite3

from Authentication import auth as auth


class DbUtil:
    conn = None

    def __init__(self, db_file_name):
        self.conn = sqlite3.connect(db_file_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, *columns):
        query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                                                {', '.join(columns)}
                                            );'''
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            raise Exception("Error during query execution")

    def insert(self, table_name, column_names, list_of_tuples):
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(table_name, ', '.join([i for i in column_names]), ', '.join(['?' for i in range(len(column_names))])), list_of_tuples
        try:
            self.conn.executemany(query)
            self.conn.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            raise Exception("Error during query execution")

    def filter(self, table_name, req_value, **input_values):
        try:
            if not input_values:
                query = f'''SELECT DISTINCT {req_value} from {table_name}'''
                self.cursor.execute(query)
            else:
                query = f'''SELECT DISTINCT {req_value} from {table_name}  WHERE'''
                for i in input_values.keys():
                    query += f' {i} = ? AND'
                if query.endswith('AND'):
                    query = query[:-4]
                self.cursor.execute(query, tuple(input_values.values()))
            l = self.cursor.fetchall()
            return sorted([x[0] for x in l])
        except Exception as e:
            print(f"Error executing query: {e}")
            raise Exception("Error during query execution")

    def check_user_registered(self, table_name, email):
        query = f"SELECT email, password_hash FROM {table_name}  WHERE email = '{email}'"
        try:
            self.cursor.execute(query)
            l = self.cursor.fetchall()
            return len(l) > 0 and len(l) == 1
        except Exception as e:
            print(f"Error executing query: {e}")
            raise Exception("Error during query execution")

    def check_user(self, table_name, email, password):
        query = f"SELECT email, password_hash FROM {table_name}  WHERE email = '{email}'"
        try:
            self.cursor.execute(query)
            l = self.cursor.fetchall()
            return len(l) > 0 and len(l) == 1 and auth.verify_password(password, l[0][1])
        except Exception as e:
            print(f"Error executing query: {e}")
            raise Exception("Error during query execution")
        
    def execute_query(self):
        query = "SELECT * from nexrad_lat_long"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return str(results)
        except Exception as e:
            print(f"Error executing query: {e}")
            raise Exception("Error during query execution")
