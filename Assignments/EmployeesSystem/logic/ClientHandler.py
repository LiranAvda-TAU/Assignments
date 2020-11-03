from EmployeesSystem.database.DbHandler import DbHandler
from EmployeesSystem.logic.Result import Result
from EmployeesSystem.logic.FieldName import FieldName
from EmployeesSystem.FileHandler import FileHandler


class ClientHandler:

    def __init__(self, db_name=r'database\EmployeeDB.db'):
        self.db_handler = DbHandler(db_name)

    def insert_employees(self, client_name, f_path, first_name_field, last_name_field, employee_id_field,
                         date_of_birth_field):
        field_names = FieldName(employee_id=employee_id_field,
                                first_name=first_name_field,
                                last_name=last_name_field,
                                date_of_birth=date_of_birth_field)
        if None in field_names:
            return Result(False,
                          "File should contain 4 explicit columns: first name, last name, date of birth, employee id "
                          "and start with a header.")
        file_handler = FileHandler(f_path, client_name)
        result, employees_df = file_handler.from_csv_to_df(field_names)
        if not result.success:
            return result
        return self.db_handler.insert_employees(employees_df, client_name)

    def check_employee_eligible(self, employee_data):
        if self.is_data_valid(employee_data):
            return self.db_handler.check_employee_eligible(employee_data)
        error = "Employee data should contain these four fields: first_name, last_name, date_of_birth, " \
                "employee_id."
        return Result(False, error)

    @staticmethod
    def is_data_valid(employee_data):
        return all(field in employee_data for field in (FileHandler.FIRST_NAME,
                                                        FileHandler.LAST_NAME,
                                                        FileHandler.DATE_OF_BIRTH,
                                                        FileHandler.EMPLOYEE_ID))

