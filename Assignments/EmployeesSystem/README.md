##EmployeesSystem

## Table of contents
1. General info
2. Technologies
3. Setup
4. Structure
5. Logic
6. File Handler
7. Database Handler
8. HTTP API
9. Server
10. Contact


## General info
This project is a simple integration system that can read CSV employees files from different clients and store updated data of the clients that are eligible.

## Technologies
EmployeesSystem is created with:
* Python version: 3.7
* pandas version: 1.0.1
* sqlite3 version: 3.31.1

## Setup
Before running the system, please make sure you have pandas package and sqlite3 package installed.
The class the user may interact with will be the 'ClientHandler' class, under 'logic' folder.
The two methods the user can use under that class are: insert_employees and check_employee_eligible.
insert_employees method will be used to insert employees data for new\existing clients into the DB.
check_employee_eligible method will check if an employee is eligible and registered in the data. This method can also
be accessed through the API.
Examples of both functions are can be seen under logic\tests\ClientHandlerTest.py

## Structure
EmployeesSystem is composed of 4 components: the Logic, the File Handler, the Database Handler and the HTTP API.

## Logic
The logic component is the main component that mediates all functionalities between the HTTP API, the File Handler and the DB Handler. 
Other than the method exposed in the HTTP API, it offers the 'insert_employees' method, that enables inserting employees files of new and existing clients to the system DB. 
The method expects to receive the client's name, the file path and the fields that hold data regarding each employee's first name, last name, birth date and employee id.
To update an existing client's employees, a recurring call to the method with the updated file path should be made.

## File Handler
The file component is responsible for parsing the clients' raw CSV files, and delivering the parsed data in the chosen format (pandas DataFrame) back to the logic component.

## Database Handler
The database component consists of the DB itself, and the Database Handler class, responsible for communication between the Logic component and the DB.

## HTTP API
The HTTP API offers a single method to check whether an employee is eligible. To use the method, a POST request should be sent to the path "/check".
The request body should contain 5 fields: first_name, last_name, date_of_birth, employee_id, client. 

## Server
The service runs locally on port 8080. It was build using python's BaseHttpRequestHandler package.

## Contact
Created by liranavda@gmail.com - feel free to contact me!