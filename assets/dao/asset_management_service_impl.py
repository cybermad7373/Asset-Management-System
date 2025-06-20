import mysql.connector
from datetime import datetime, timedelta
from ..entity.asset import Asset
from ..entity.employee import Employee
from ..entity.maintenance_record import MaintenanceRecord
from ..entity.asset_allocation import AssetAllocation
from ..entity.reservation import Reservation
from ..exception.asset_not_found_exception import AssetNotFoundException
from ..exception.asset_not_maintained_exception import AssetNotMaintainedException
from ..util.db_conn_util import DBConnUtil
from ..util.password_util import PasswordUtil

from assets.dao.asset_management_service import AssetManagementService
from assets.entity.asset import Asset
from assets.entity.employee import Employee
from assets.entity.maintenance_record import MaintenanceRecord
from assets.entity.asset_allocation import AssetAllocation
from assets.entity.reservation import Reservation
from assets.exception.asset_not_found_exception import AssetNotFoundException
from assets.exception.asset_not_maintained_exception import AssetNotMaintainedException
from assets.util.db_conn_util import DBConnUtil
from assets.util.password_util import PasswordUtil
from .asset_management_service import AssetManagementService


class AssetManagementServiceImpl(AssetManagementService):
    def __init__(self):
        self.connection = DBConnUtil.get_connection(property_file_name='config.properties')

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def add_asset(self, asset):
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO assets (name, type, serial_number, purchase_date, location, status, owner_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                asset.get_name(),
                asset.get_type(),
                asset.get_serial_number(),
                asset.get_purchase_date(),
                asset.get_location(),
                asset.get_status(),
                asset.get_owner_id()
            )
            cursor.execute(query, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error adding asset: {err}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def update_asset(self, asset):
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE assets 
                SET name = %s, type = %s, serial_number = %s, purchase_date = %s, 
                    location = %s, status = %s, owner_id = %s
                WHERE asset_id = %s
            """
            values = (
                asset.get_name(),
                asset.get_type(),
                asset.get_serial_number(),
                asset.get_purchase_date(),
                asset.get_location(),
                asset.get_status(),
                asset.get_owner_id(),
                asset.get_asset_id()
            )
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error updating asset: {err}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def delete_asset(self, asset_id):
        try:
            cursor = self.connection.cursor()

            # Check if asset exists
            cursor.execute("SELECT 1 FROM assets WHERE asset_id = %s", (asset_id,))
            if not cursor.fetchone():
                raise AssetNotFoundException(asset_id)

            # Delete related records first (maintenance, allocations, reservations)
            cursor.execute("DELETE FROM maintenance_records WHERE asset_id = %s", (asset_id,))
            cursor.execute("DELETE FROM asset_allocations WHERE asset_id = %s", (asset_id,))
            cursor.execute("DELETE FROM reservations WHERE asset_id = %s", (asset_id,))

            # Delete the asset
            cursor.execute("DELETE FROM assets WHERE asset_id = %s", (asset_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error deleting asset: {err}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def allocate_asset(self, asset_id, employee_id, allocation_date):
        try:
            cursor = self.connection.cursor()

            # Check if asset exists
            cursor.execute("SELECT status FROM assets WHERE asset_id = %s", (asset_id,))
            asset = cursor.fetchone()
            if not asset:
                raise AssetNotFoundException(asset_id)

            # Check if asset is available
            if asset[0] != 'in_use':
                print("Asset is not available for allocation")
                return False

            # Check if employee exists
            cursor.execute("SELECT 1 FROM employees WHERE employee_id = %s", (employee_id,))
            if not cursor.fetchone():
                print("Employee not found")
                return False

            # Check if asset is already allocated to someone else
            cursor.execute("""
                SELECT 1 FROM asset_allocations 
                WHERE asset_id = %s AND return_date IS NULL
            """, (asset_id,))
            if cursor.fetchone():
                print("Asset is already allocated to another employee")
                return False

            # Allocate asset
            query = """
                INSERT INTO asset_allocations (asset_id, employee_id, allocation_date)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (asset_id, employee_id, allocation_date))

            # Update asset status
            cursor.execute("""
                UPDATE assets SET status = 'in_use', owner_id = %s 
                WHERE asset_id = %s
            """, (employee_id, asset_id))

            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error allocating asset: {err}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def deallocate_asset(self, asset_id, employee_id, return_date):
        try:
            cursor = self.connection.cursor()

            # Check allocation record
            cursor.execute("""
                SELECT allocation_id FROM asset_allocations 
                WHERE asset_id = %s AND employee_id = %s AND return_date IS NULL
            """, (asset_id, employee_id))
            allocation = cursor.fetchone()

            if not allocation:
                print("No active allocation found for this asset and employee")
                return False

            # Update allocation with return date
            cursor.execute("""
                UPDATE asset_allocations 
                SET return_date = %s 
                WHERE allocation_id = %s
            """, (return_date, allocation[0]))

            # Update asset status (set to available)
            cursor.execute("""
                UPDATE assets 
                SET status = 'in_use', owner_id = NULL 
                WHERE asset_id = %s
            """, (asset_id,))

            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error deallocating asset: {err}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def perform_maintenance(self, asset_id, maintenance_date, description, cost):
        try:
            cursor = self.connection.cursor()

            # Check if asset exists
            cursor.execute("SELECT 1 FROM assets WHERE asset_id = %s", (asset_id,))
            if not cursor.fetchone():
                raise AssetNotFoundException(asset_id)

            # Insert maintenance record
            query = """
                INSERT INTO maintenance_records 
                (asset_id, maintenance_date, description, cost)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (asset_id, maintenance_date, description, cost))

            # Update asset status
            cursor.execute("""
                UPDATE assets 
                SET status = 'under_maintenance' 
                WHERE asset_id = %s
            """, (asset_id,))

            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error performing maintenance: {err}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def reserve_asset(self, asset_id, employee_id, reservation_date, start_date, end_date):
        try:
            cursor = self.connection.cursor()

            # Check if asset exists
            cursor.execute("SELECT status FROM assets WHERE asset_id = %s", (asset_id,))
            asset = cursor.fetchone()
            if not asset:
                raise AssetNotFoundException(asset_id)

            # Check if asset is available
            if asset[0] != 'in_use':
                print("Asset is not available for reservation")
                return False

            # Check if employee exists
            cursor.execute("SELECT 1 FROM employees WHERE employee_id = %s", (employee_id,))
            if not cursor.fetchone():
                print("Employee not found")
                return False

            # Check for conflicting reservations
            cursor.execute("""
                SELECT 1 FROM reservations 
                WHERE asset_id = %s AND status = 'approved' 
                AND ((start_date <= %s AND end_date >= %s) 
                OR (start_date <= %s AND end_date >= %s) 
                OR (start_date >= %s AND end_date <= %s))
            """, (asset_id, start_date, start_date, end_date, end_date, start_date, end_date))

            if cursor.fetchone():
                print("Asset is already reserved for the requested period")
                return False

            # Create reservation
            query = """
                INSERT INTO reservations 
                (asset_id, employee_id, reservation_date, start_date, end_date, status)
                VALUES (%s, %s, %s, %s, %s, 'pending')
            """
            cursor.execute(query, (asset_id, employee_id, reservation_date, start_date, end_date))
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error reserving asset: {err}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def withdraw_reservation(self, reservation_id):
        try:
            cursor = self.connection.cursor()

            # Check if reservation exists
            cursor.execute("""
                SELECT asset_id FROM reservations 
                WHERE reservation_id = %s
            """, (reservation_id,))
            reservation = cursor.fetchone()

            if not reservation:
                print("Reservation not found")
                return False

            # Delete reservation
            cursor.execute("""
                DELETE FROM reservations 
                WHERE reservation_id = %s
            """, (reservation_id,))

            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error withdrawing reservation: {err}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def login(self, email, password):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM employees WHERE email = %s"
            cursor.execute(query, (email,))
            employee_data = cursor.fetchone()

            if not employee_data:
                return None

            # Verify password
            if not PasswordUtil.verify_password(password, employee_data['password']):
                return None

            employee = Employee(
                employee_id=employee_data['employee_id'],
                name=employee_data['name'],
                department=employee_data['department'],
                email=employee_data['email'],
                password=employee_data['password'],
                is_admin=employee_data['is_admin']
            )

            return employee
        except mysql.connector.Error as err:
            print(f"Error during login: {err}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def add_employee(self, employee, current_user):
        if not current_user.get_is_admin():
            print("Only admin can add new employees")
            return False

        try:
            cursor = self.connection.cursor()

            # Hash password
            hashed_password = PasswordUtil.hash_password(employee.get_password())

            query = """
                INSERT INTO employees (name, department, email, password, is_admin)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                employee.get_name(),
                employee.get_department(),
                employee.get_email(),
                hashed_password,
                employee.get_is_admin()
            )
            cursor.execute(query, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error adding employee: {err}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def update_employee(self, employee, current_user):
        # Only allow updating own profile unless admin
        if not current_user.get_is_admin() and current_user.get_employee_id() != employee.get_employee_id():
            print("You can only update your own profile")
            return False

        try:
            cursor = self.connection.cursor()

            # If password is being updated, hash it
            if employee.get_password():
                hashed_password = PasswordUtil.hash_password(employee.get_password())
                query = """
                    UPDATE employees 
                    SET name = %s, department = %s, email = %s, password = %s
                    WHERE employee_id = %s
                """
                values = (
                    employee.get_name(),
                    employee.get_department(),
                    employee.get_email(),
                    hashed_password,
                    employee.get_employee_id()
                )
            else:
                query = """
                    UPDATE employees 
                    SET name = %s, department = %s, email = %s
                    WHERE employee_id = %s
                """
                values = (
                    employee.get_name(),
                    employee.get_department(),
                    employee.get_email(),
                    employee.get_employee_id()
                )

            cursor.execute(query, values)
            self.connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error updating employee: {err}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_asset(self, asset_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM assets WHERE asset_id = %s"
            cursor.execute(query, (asset_id,))
            asset_data = cursor.fetchone()

            if not asset_data:
                raise AssetNotFoundException(asset_id)

            asset = Asset(
                asset_id=asset_data['asset_id'],
                name=asset_data['name'],
                type=asset_data['type'],
                serial_number=asset_data['serial_number'],
                purchase_date=asset_data['purchase_date'],
                location=asset_data['location'],
                status=asset_data['status'],
                owner_id=asset_data['owner_id']
            )

            return asset
        except mysql.connector.Error as err:
            print(f"Error getting asset: {err}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_employee(self, employee_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM employees WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            employee_data = cursor.fetchone()

            if not employee_data:
                return None

            employee = Employee(
                employee_id=employee_data['employee_id'],
                name=employee_data['name'],
                department=employee_data['department'],
                email=employee_data['email'],
                password=employee_data['password'],
                is_admin=employee_data['is_admin']
            )

            return employee
        except mysql.connector.Error as err:
            print(f"Error getting employee: {err}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
