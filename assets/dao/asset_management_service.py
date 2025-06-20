from abc import ABC, abstractmethod


class AssetManagementService(ABC):
    @abstractmethod
    def add_asset(self, asset):
        pass

    @abstractmethod
    def update_asset(self, asset):
        pass

    @abstractmethod
    def delete_asset(self, asset_id):
        pass

    @abstractmethod
    def allocate_asset(self, asset_id, employee_id, allocation_date):
        pass

    @abstractmethod
    def deallocate_asset(self, asset_id, employee_id, return_date):
        pass

    @abstractmethod
    def perform_maintenance(self, asset_id, maintenance_date, description, cost):
        pass

    @abstractmethod
    def reserve_asset(self, asset_id, employee_id, reservation_date, start_date, end_date):
        pass

    @abstractmethod
    def withdraw_reservation(self, reservation_id):
        pass

    @abstractmethod
    def login(self, email, password):
        pass

    @abstractmethod
    def add_employee(self, employee, current_user):
        pass

    @abstractmethod
    def update_employee(self, employee, current_user):
        pass

    @abstractmethod
    def get_asset(self, asset_id):
        pass

    @abstractmethod
    def get_employee(self, employee_id):
        pass
