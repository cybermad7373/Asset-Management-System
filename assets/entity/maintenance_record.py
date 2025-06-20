class MaintenanceRecord:
    def __init__(self, maintenance_id=None, asset_id=None, maintenance_date=None, description=None, cost=None):
        self.maintenance_id = maintenance_id
        self.asset_id = asset_id
        self.maintenance_date = maintenance_date
        self.description = description
        self.cost = cost

    def get_maintenance_id(self):
        return self.maintenance_id

    def set_maintenance_id(self, maintenance_id):
        self.maintenance_id = maintenance_id

    def get_asset_id(self):
        return self.asset_id

    def set_asset_id(self, asset_id):
        self.asset_id = asset_id

    def get_maintenance_date(self):
        return self.maintenance_date

    def set_maintenance_date(self, maintenance_date):
        self.maintenance_date = maintenance_date

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_cost(self):
        return self.cost

    def set_cost(self, cost):
        self.cost = cost

    def __str__(self):
        return f"Maintenance ID: {self.maintenance_id}, Asset ID: {self.asset_id}, Date: {self.maintenance_date}, Cost: {self.cost}"
