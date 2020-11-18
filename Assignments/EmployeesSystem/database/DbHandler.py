import sqlite3
from sqlite3 import Error
from EmployeesSystem.logic.Result import Result


class DbHandler:

    def __init__(self, db_name):
        self.db_name = db_name

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except Error as e:
            print(e)
        return conn

    def create_table(self):
        conn = self.create_connection()
        if conn:
            try:
                c = conn.cursor()
                c.execute('''
                CREATE TABLE employee(
                    employee_id INTEGER,
                    client TEXT,
                    first_name TEXT, 
                    last_name TEXT,
                    date_of_birth TEXT,
                    PRIMARY KEY (employee_id, client)
                );
                ''')
                c.close()
                conn.commit()
                conn.close()
                print("Table created successfully")
            except Error as e:
                print(e)

    @staticmethod
    def to_sql_with_pd(employees_df, conn):
        try:
            employees_df.to_sql('employee',
                                conn,
                                if_exists='append',
                                index=False)
            return Result(True, "")
        except Error as e:
            return Result(False, str(e))

    @staticmethod
    def delete_by_ids(conn, list_ids, client):
        try:
            c = conn.cursor()
            query = '''DELETE FROM employee WHERE client=? AND employee_id IN ({})'''.format(", ".join("?" * len(list_ids)))
            c.execute(query, [client]+list_ids)
            conn.commit()
            conn.close()
            return Result(True, "")
        except Error as e:
            return Result(False, str(e))

    def insert_with_filter(self, employees_df, conn, exist_ids, client):
        try:
            # first - insert new employees
            is_new_employee = ~employees_df['employee_id'].isin(exist_ids)
            new_employees_df = employees_df[is_new_employee]
            if not new_employees_df.empty:
                print("new employees found")
                result = self.to_sql_with_pd(new_employees_df, conn)
                if not result.success:  # insertion failed
                    conn.close()
                    return result
            # second - delete past employees
            past_employee_ids = [emp_id for emp_id in exist_ids if emp_id not in set(employees_df['employee_id'])]
            if past_employee_ids:
                print("past employees found")
                return self.delete_by_ids(conn, past_employee_ids, client)
            else:
                conn.close()
                return Result(True, "")
        except Error as e:
            conn.close()
            return Result(False, str(e))

    def insert_employees(self, employees_df, client):
        conn = self.create_connection()
        if conn:
            # first - get all ids for this client
            c = conn.cursor()
            c.execute('''SELECT employee_id FROM employee WHERE client=?''',
                      (client,))
            exist_ids = [item[0] for item in c.fetchall()]
            c.close()
            if not exist_ids:
                print("new client")
                return self.to_sql_with_pd(employees_df, conn)
            else:
                print("existing client")
                return self.insert_with_filter(employees_df, conn, exist_ids, client)
        return Result(False, "Connection Failed.")

    def check_employee_eligible(self, employee_data):
        conn = self.create_connection()
        if conn:
            try:
                c = conn.cursor()
                c.execute('''SELECT * FROM employee WHERE employee_id=? AND client=? AND first_name=? AND last_name=?''',
                          (employee_data['employee_id'], employee_data['client'], employee_data['first_name'],
                           employee_data['last_name'],))
                exists = c.fetchall()
                print(exists)
                if not exists:
                    return Result(False, "This employee does not exist_ids in the system.")

                return Result(True, "")
            except Error as e:
                return Result(False, str(e))
        return Result(False, "Connection Failed.")

