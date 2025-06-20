class AssetNotMaintainedException(Exception):
    def __init__(self, asset_id):
        self.asset_id = asset_id
        self.message = f"Asset with ID {asset_id} has not been maintained in the last 2 years"
        super().__init__(self.message)
