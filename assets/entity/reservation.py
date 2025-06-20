class Reservation:
    def __init__(self, reservation_id=None, asset_id=None, employee_id=None, reservation_date=None,
                 start_date=None, end_date=None, status=None):
        self.reservation_id = reservation_id
        self.asset_id = asset_id
        self.employee_id = employee_id
        self.reservation_date = reservation_date
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def get_reservation_id(self):
        return self.reservation_id

    def set_reservation_id(self, reservation_id):
        self.reservation_id = reservation_id

    def get_asset_id(self):
        return self.asset_id

    def set_asset_id(self, asset_id):
        self.asset_id = asset_id

    def get_employee_id(self):
        return self.employee_id

    def set_employee_id(self, employee_id):
        self.employee_id = employee_id

    def get_reservation_date(self):
        return self.reservation_date

    def set_reservation_date(self, reservation_date):
        self.reservation_date = reservation_date

    def get_start_date(self):
        return self.start_date

    def set_start_date(self, start_date):
        self.start_date = start_date

    def get_end_date(self):
        return self.end_date

    def set_end_date(self, end_date):
        self.end_date = end_date

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return f"Reservation ID: {self.reservation_id}, Asset ID: {self.asset_id}, Employee ID: {self.employee_id}, Status: {self.status}"

