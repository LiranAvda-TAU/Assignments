from EmployeesSystem.logic.ClientHandler import ClientHandler
import os


class ClientHandlerTester:

    def __init__(self):
        self.client_handler = ClientHandler(db_name="EmployeeDBTest.db")

    @staticmethod
    def get_exist_employee_data():
        return {'first_name': 'liran',
                'last_name': 'avda',
                'employee_id': 547,
                'date_of_birth': '20090102'}

    @staticmethod
    def get_new_exist_employee_data():
        return {'first_name': 'simba',
                'last_name': 'lion',
                'employee_id': 19331,
                'date_of_birth': '20090601'}

    @staticmethod
    def get_not_exist_employee_data():
        return {'first_name': 'bar',
                'last_name': 'cohen',
                'employee_id': 12331,
                'date_of_birth': '20090101'}

    @staticmethod
    def get_invalid_employee_data():
        return {'first_name': 'liran',
                'last_name': 'avda',
                'date_of_birth': '20090102'}

    def create_table(self):
        self.client_handler.db_handler.create_table()

    def insert_valid_exist_employees_test(self):
        result = self.client_handler.insert_employees(client_name="foo",
                                                      f_path=os.getcwd()+r"\test_files\foo.csv",
                                                      first_name_field="fname",
                                                      last_name_field="lname",
                                                      employee_id_field="e_id",
                                                      date_of_birth_field="birth")
        if result.success:
            print("insert_valid_exist_employees_test: PASS")
        else:
            print("insert_valid_exist_employees_test: FAIL, error:", result.error)

    def insert_valid_non_exist_employees_test(self):
        result = self.client_handler.insert_employees(client_name="foo",
                                                      f_path=os.getcwd()+r"\test_files\foo_new.csv",
                                                      first_name_field="fname",
                                                      last_name_field="lname",
                                                      employee_id_field="e_id",
                                                      date_of_birth_field="birth")
        if result.success:
            print("insert_valid_non_exist_employees_test: PASS")
        else:
            print("insert_valid_non_exist_employees_test: FAIL, error:", result.error)

    def insert_employees_test_no_header(self):
        result = self.client_handler.insert_employees(client_name="foo",
                                                      f_path=os.getcwd() + r"\test_files\foo_no_header.csv",
                                                      first_name_field="fname",
                                                      last_name_field="lname",
                                                      employee_id_field="e_id",
                                                      date_of_birth_field="birth")
        if not result.success :
            print("insert_employees_test_no_header: PASS")
        else:
            print("insert_employees_test_no_header: FAIL, error:", result.error)

    def insert_employees_test_invalid_file(self):
        result = self.client_handler.insert_employees(client_name="foo",
                                                      f_path=os.getcwd()+r"\test_files\foo.txt",
                                                      first_name_field="fname",
                                                      last_name_field="lname",
                                                      employee_id_field="e_id",
                                                      date_of_birth_field="birth")
        if not result.success and result.error == "CSV files only.":
            print("insert_employees_test_invalid_file: PASS")
        else:
            print("insert_employees_test_invalid_file: FAIL, error:", result.error)

    def insert_employees_test_invalid_field(self):
        result = self.client_handler.insert_employees(client_name="foo",
                                                      f_path=os.getcwd()+r"\test_files\foo.csv",
                                                      first_name_field=None,
                                                      last_name_field="lname",
                                                      employee_id_field="e_id",
                                                      date_of_birth_field="birth")
        if not result.success and result.error == "File should contain 4 explicit columns: first name, last name, " \
                                                  "date of birth, employee id and start with a header.":
            print("insert_employees_test_invalid_field: PASS")
        else:
            print("insert_employees_test_invalid_field: FAIL, error:", result.error)

    def check_employee_eligible_exist_test(self):
        result = self.client_handler.check_employee_eligible(employee_data=self.get_exist_employee_data())
        if result.success:
            print("check_employee_eligible_exist_test: PASS")
        else:
            print("check_employee_eligible_exist_test: FAIL, error:", result.error)

    def check_employee_eligible_new_exist_test(self):
        result = self.client_handler.check_employee_eligible(employee_data=self.get_new_exist_employee_data())
        if result.success:
            print("check_employee_eligible_new_exist_test: PASS")
        else:
            print("check_employee_eligible_new_exist_test: FAIL, error:", result.error)

    def check_employee_eligible_not_exist_test(self):
        result = self.client_handler.check_employee_eligible(employee_data=self.get_not_exist_employee_data())
        if not result.success and result.error == "This employee does not exist_ids in the system.":
            print("check_employee_eligible_not_exist_test: PASS")
        else:
            print("check_employee_eligible_not_exist_test: FAIL, error:", result.error)

    def check_invalid_employee_eligible_test(self):
        result = self.client_handler.check_employee_eligible(employee_data=self.get_invalid_employee_data())
        if not result.success and result.error == "Employee data should contain these four fields: first_name, " \
                                                  "last_name, date_of_birth, employee_id.":
            print("check_invalid_employee_eligible_test: PASS")
        else:
            print("check_invalid_employee_eligible_test: FAIL, error:", result.error)


client_handler_tester = ClientHandlerTester()

print("###Create a table if needed###")
client_handler_tester.create_table()

print("\n###INSERT TESTS###")
client_handler_tester.insert_valid_exist_employees_test()
client_handler_tester.insert_valid_non_exist_employees_test()
client_handler_tester.insert_employees_test_no_header()
client_handler_tester.insert_employees_test_invalid_file()
client_handler_tester.insert_employees_test_invalid_field()

print("\n###CHECK ELIGIBILITY TESTS###")
client_handler_tester.check_employee_eligible_exist_test()
client_handler_tester.check_employee_eligible_new_exist_test()
client_handler_tester.check_employee_eligible_not_exist_test()
client_handler_tester.check_invalid_employee_eligible_test()
