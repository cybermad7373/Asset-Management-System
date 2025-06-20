class Employee:
    def __init__(self, employee_id=None, name=None, department=None, email=None, password=None, is_admin=False):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def get_employee_id(self):
        return self.employee_id

    def set_employee_id(self, employee_id):
        self.employee_id = employee_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_department(self):
        return self.department

    def set_department(self, department):
        self.department = department

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_is_admin(self):
        return self.is_admin

    def set_is_admin(self, is_admin):
        self.is_admin = is_admin

    def __str__(self):
        return f"Employee ID: {self.employee_id}, Name: {self.name}, Department: {self.department}, Email: {self.email}, Admin: {self.is_admin}"
