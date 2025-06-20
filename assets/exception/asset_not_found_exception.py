class AssetNotFoundException(Exception):
    def __init__(self, asset_id):
        self.asset_id = asset_id
        self.message = f"Asset with ID {asset_id} not found"
        super().__init__(self.message)
