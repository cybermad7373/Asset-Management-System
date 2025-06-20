class Asset:

    def __init__(self, asset_id=None, name=None, type=None, serial_number=None, purchase_date=None,
                 location=None, status=None, owner_id=None):
        self.asset_id = asset_id
        self.name = name
        self.type = type
        self.serial_number = serial_number
        self.purchase_date = purchase_date
        self.location = location
        self.status = status
        self.owner_id = owner_id

    def get_asset_id(self):
        return self.asset_id

    def set_asset_id(self, asset_id):
        self.asset_id = asset_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_serial_number(self):
        return self.serial_number

    def set_serial_number(self, serial_number):
        self.serial_number = serial_number

    def get_purchase_date(self):
        return self.purchase_date

    def set_purchase_date(self, purchase_date):
        self.purchase_date = purchase_date

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_owner_id(self):
        return self.owner_id

    def set_owner_id(self, owner_id):
        self.owner_id = owner_id

    def __str__(self):
        return f"Asset ID: {self.asset_id}, Name: {self.name}, Type: {self.type}, Serial: {self.serial_number}, Status: {self.status}"
