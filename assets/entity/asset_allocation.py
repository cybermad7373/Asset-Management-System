class AssetAllocation:
    def __init__(self, allocation_id=None, asset_id=None, employee_id=None, allocation_date=None, return_date=None):
        self.allocation_id = allocation_id
        self.asset_id = asset_id
        self.employee_id = employee_id
        self.allocation_date = allocation_date
        self.return_date = return_date

    def get_allocation_id(self):
        return self.allocation_id

    def set_allocation_id(self, allocation_id):
        self.allocation_id = allocation_id

    def get_asset_id(self):
        return self.asset_id

    def set_asset_id(self, asset_id):
        self.asset_id = asset_id

    def get_employee_id(self):
        return self.employee_id

    def set_employee_id(self, employee_id):
        self.employee_id = employee_id

    def get_allocation_date(self):
        return self.allocation_date

    def set_allocation_date(self, allocation_date):
        self.allocation_date = allocation_date

    def get_return_date(self):
        return self.return_date

    def set_return_date(self, return_date):
        self.return_date = return_date

    def __str__(self):
        return (f"Allocation ID: {self.allocation_id}, Asset ID: {self.asset_id}, Employee ID: {self.employee_id},"
                f" Allocation Date: {self.allocation_date}, Return Date: {self.return_date}")
