from EmployeesSystem.logic.Result import Result
import pandas as pd


class FileHandler:

    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    DATE_OF_BIRTH = "date_of_birth"
    EMPLOYEE_ID = "employee_id"
    CLIENT = "client"

    def __init__(self, file_path, client_name):
        self.file_path = file_path
        self.client_name = client_name

    def from_csv_to_df(self, field_names):
        if not self.file_path.endswith(".csv"):
            return Result(False, "CSV files only."), None
        try:
            employees_df = pd.read_csv(self.file_path,
                                       usecols=field_names,
                                       parse_dates=[field_names.date_of_birth])[list(field_names)]
            self.change_columns_names(employees_df)
            # Using DataFrame.insert() to add a column for client name
            employees_df.insert(1, "client", [self.client_name for _ in range(employees_df.shape[0])], True)
            return Result(True, ""), employees_df
        except Exception as e:
            return Result(False, str(e)), None

    def change_columns_names(self, employees_df):
        employees_df.columns.values[0] = self.EMPLOYEE_ID
        employees_df.columns.values[1] = self.FIRST_NAME
        employees_df.columns.values[2] = self.LAST_NAME
        employees_df.columns.values[3] = self.DATE_OF_BIRTH
