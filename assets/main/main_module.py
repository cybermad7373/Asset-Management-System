from datetime import datetime
from ..dao.asset_management_service_impl import AssetManagementServiceImpl
from ..entity.asset import Asset
from ..entity.employee import Employee
from ..exception.asset_not_found_exception import AssetNotFoundException
from ..exception.asset_not_maintained_exception import AssetNotMaintainedException


class MainModule:
    def __init__(self):
        self.service = AssetManagementServiceImpl()
        self.current_user = None

    def login_menu(self):
        while True:
            print("\n==== Digital Asset Management System ====")
            print("1. Login")
            print("2. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                email = input("Enter email: ")
                password = input("Enter password: ")
                self.current_user = self.service.login(email, password)

                if self.current_user:
                    print(f"\nWelcome, {self.current_user.get_name()}!")
                    if self.current_user.get_is_admin():
                        self.admin_menu()
                    else:
                        self.user_menu()
                else:
                    print("Invalid email or password")
            elif choice == "2":
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def admin_menu(self):
        while True:
            print("\n==== Admin Menu ====")
            print("1. Asset Management")
            print("2. Employee Management")
            print("3. Reports")
            print("4. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.asset_management_menu()
            elif choice == "2":
                self.employee_management_menu()
            elif choice == "3":
                self.reports_menu()
            elif choice == "4":
                self.current_user = None
                break
            else:
                print("Invalid choice. Please try again.")

    def user_menu(self):
        while True:
            print("\n==== User Menu ====")
            print("1. View My Assets")
            print("2. Request Asset")
            print("3. Return Asset")
            print("4. Request Maintenance")
            print("5. Update My Profile")
            print("6. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_my_assets()
            elif choice == "2":
                self.request_asset()
            elif choice == "3":
                self.return_asset()
            elif choice == "4":
                self.request_maintenance()
            elif choice == "5":
                self.update_my_profile()
            elif choice == "6":
                self.current_user = None
                break
            else:
                print("Invalid choice. Please try again.")

    def asset_management_menu(self):
        while True:
            print("\n==== Asset Management ====")
            print("1. Add Asset")
            print("2. Update Asset")
            print("3. Delete Asset")
            print("4. View All Assets")
            print("5. Allocate Asset")
            print("6. Deallocate Asset")
            print("7. Perform Maintenance")
            print("8. Back to Admin Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_asset()
            elif choice == "2":
                self.update_asset()
            elif choice == "3":
                self.delete_asset()
            elif choice == "4":
                self.view_all_assets()
            elif choice == "5":
                self.allocate_asset()
            elif choice == "6":
                self.deallocate_asset()
            elif choice == "7":
                self.perform_maintenance()
            elif choice == "8":
                break
            else:
                print("Invalid choice. Please try again.")

    def employee_management_menu(self):
        while True:
            print("\n==== Employee Management ====")
            print("1. Add Employee")
            print("2. Update Employee")
            print("3. View All Employees")
            print("4. Back to Admin Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_employee()
            elif choice == "2":
                self.update_employee()
            elif choice == "3":
                self.view_all_employees()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def reports_menu(self):
        while True:
            print("\n==== Reports ====")
            print("1. Asset Status Report")
            print("2. Maintenance History")
            print("3. Allocation History")
            print("4. Back to Admin Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.asset_status_report()
            elif choice == "2":
                self.maintenance_history()
            elif choice == "3":
                self.allocation_history()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def add_asset(self):
        print("\n==== Add New Asset ====")
        try:
            name = input("Enter asset name: ")
            asset_type = input("Enter asset type (e.g., laptop, vehicle, equipment): ")
            serial_number = input("Enter serial number: ")
            purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
            location = input("Enter current location: ")
            status = input("Enter status (in_use, decommissioned, under_maintenance): ")
            owner_id = input("Enter owner ID (leave empty if none): ")

            asset = Asset(
                name=name,
                type=asset_type,
                serial_number=serial_number,
                purchase_date=purchase_date,
                location=location,
                status=status,
                owner_id=int(owner_id) if owner_id else None
            )

            if self.service.add_asset(asset):
                print("Asset added successfully!")
            else:
                print("Failed to add asset")
        except Exception as e:
            print(f"Error: {e}")

    def update_asset(self):
        print("\n==== Update Asset ====")
        try:
            asset_id = int(input("Enter asset ID to update: "))
            asset = self.service.get_asset(asset_id)

            if not asset:
                print("Asset not found")
                return

            print(f"\nCurrent Asset Details:")
            print(f"Name: {asset.get_name()}")
            print(f"Type: {asset.get_type()}")
            print(f"Serial Number: {asset.get_serial_number()}")
            print(f"Purchase Date: {asset.get_purchase_date()}")
            print(f"Location: {asset.get_location()}")
            print(f"Status: {asset.get_status()}")
            print(f"Owner ID: {asset.get_owner_id()}")

            print("\nEnter new details (leave blank to keep current value):")
            name = input(f"Name [{asset.get_name()}]: ") or asset.get_name()
            asset_type = input(f"Type [{asset.get_type()}]: ") or asset.get_type()
            serial_number = input(f"Serial Number [{asset.get_serial_number()}]: ") or asset.get_serial_number()
            purchase_date = input(f"Purchase Date [{asset.get_purchase_date()}]: ") or asset.get_purchase_date()
            location = input(f"Location [{asset.get_location()}]: ") or asset.get_location()
            status = input(f"Status [{asset.get_status()}]: ") or asset.get_status()
            owner_id = input(f"Owner ID [{asset.get_owner_id()}]: ") or asset.get_owner_id()

            updated_asset = Asset(
                asset_id=asset_id,
                name=name,
                type=asset_type,
                serial_number=serial_number,
                purchase_date=purchase_date,
                location=location,
                status=status,
                owner_id=int(owner_id) if owner_id else None
            )

            if self.service.update_asset(updated_asset):
                print("Asset updated successfully!")
            else:
                print("Failed to update asset")
        except Exception as e:
            print(f"Error: {e}")

    def delete_asset(self):
        print("\n==== Delete Asset ====")
        try:
            asset_id = int(input("Enter asset ID to delete: "))

            if self.service.delete_asset(asset_id):
                print("Asset deleted successfully!")
            else:
                print("Failed to delete asset")
        except AssetNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def view_all_assets(self):
        print("\n==== All Assets ====")
        try:
            cursor = self.service.connection.cursor(dictionary=True)
            query = "SELECT * FROM assets"
            cursor.execute(query)
            assets = cursor.fetchall()

            if not assets:
                print("No assets found")
                return

            print("\n{:<10} {:<20} {:<15} {:<15} {:<15} {:<15} {:<20} {:<10}".format(
                "ID", "Name", "Type", "Serial", "Purchase Date", "Location", "Status", "Owner ID"
            ))
            print("-" * 120)

            for asset in assets:
                print("{:<10} {:<20} {:<15} {:<15} {:<15} {:<15} {:<20} {:<10}".format(
                    asset['asset_id'],
                    asset['name'],
                    asset['type'],
                    asset['serial_number'],
                    str(asset['purchase_date']),
                    asset['location'],
                    asset['status'],
                    asset['owner_id'] if asset['owner_id'] else "None"
                ))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def allocate_asset(self):
        print("\n==== Allocate Asset ====")
        try:
            asset_id = int(input("Enter asset ID to allocate: "))
            employee_id = int(input("Enter employee ID to allocate to: "))
            allocation_date = input("Enter allocation date (YYYY-MM-DD): ")

            if self.service.allocate_asset(asset_id, employee_id, allocation_date):
                print("Asset allocated successfully!")
            else:
                print("Failed to allocate asset")
        except AssetNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def deallocate_asset(self):
        print("\n==== Deallocate Asset ====")
        try:
            asset_id = int(input("Enter asset ID to deallocate: "))
            employee_id = int(input("Enter employee ID to deallocate from: "))
            return_date = input("Enter return date (YYYY-MM-DD): ")

            if self.service.deallocate_asset(asset_id, employee_id, return_date):
                print("Asset deallocated successfully!")
            else:
                print("Failed to deallocate asset")
        except Exception as e:
            print(f"Error: {e}")

    def perform_maintenance(self):
        print("\n==== Perform Maintenance ====")
        try:
            asset_id = int(input("Enter asset ID for maintenance: "))
            maintenance_date = input("Enter maintenance date (YYYY-MM-DD): ")
            description = input("Enter maintenance description: ")
            cost = float(input("Enter maintenance cost: "))

            if self.service.perform_maintenance(asset_id, maintenance_date, description, cost):
                print("Maintenance recorded successfully!")
            else:
                print("Failed to record maintenance")
        except AssetNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def add_employee(self):
        print("\n==== Add New Employee ====")
        try:
            name = input("Enter employee name: ")
            department = input("Enter department: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            is_admin = input("Is this an admin account? (y/n): ").lower() == 'y'

            employee = Employee(
                name=name,
                department=department,
                email=email,
                password=password,
                is_admin=is_admin
            )

            if self.service.add_employee(employee, self.current_user):
                print("Employee added successfully!")
            else:
                print("Failed to add employee")
        except Exception as e:
            print(f"Error: {e}")

    def update_employee(self):
        print("\n==== Update Employee ====")
        try:
            employee_id = int(input("Enter employee ID to update: "))
            employee = self.service.get_employee(employee_id)

            if not employee:
                print("Employee not found")
                return

            print(f"\nCurrent Employee Details:")
            print(f"Name: {employee.get_name()}")
            print(f"Department: {employee.get_department()}")
            print(f"Email: {employee.get_email()}")
            print(f"Admin: {'Yes' if employee.get_is_admin() else 'No'}")

            print("\nEnter new details (leave blank to keep current value):")
            name = input(f"Name [{employee.get_name()}]: ") or employee.get_name()
            department = input(f"Department [{employee.get_department()}]: ") or employee.get_department()
            email = input(f"Email [{employee.get_email()}]: ") or employee.get_email()
            password = input("New password (leave blank to keep current): ")

            updated_employee = Employee(
                employee_id=employee_id,
                name=name,
                department=department,
                email=email,
                password=password if password else None,
                is_admin=employee.get_is_admin()
            )

            if self.service.update_employee(updated_employee, self.current_user):
                print("Employee updated successfully!")
            else:
                print("Failed to update employee")
        except Exception as e:
            print(f"Error: {e}")

    def view_all_employees(self):
        print("\n==== All Employees ====")
        try:
            cursor = self.service.connection.cursor(dictionary=True)
            query = "SELECT * FROM employees"
            cursor.execute(query)
            employees = cursor.fetchall()

            if not employees:
                print("No employees found")
                return

            print("\n{:<10} {:<20} {:<20} {:<25} {:<10}".format(
                "ID", "Name", "Department", "Email", "Admin"
            ))
            print("-" * 85)

            for emp in employees:
                print("{:<10} {:<20} {:<20} {:<25} {:<10}".format(
                    emp['employee_id'],
                    emp['name'],
                    emp['department'],
                    emp['email'],
                    "Yes" if emp['is_admin'] else "No"
                ))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def view_my_assets(self):
        print("\n==== My Assets ====")
        try:
            cursor = self.service.connection.cursor(dictionary=True)
            query = """
                SELECT a.* FROM assets a
                JOIN asset_allocations aa ON a.asset_id = aa.asset_id
                WHERE aa.employee_id = %s AND aa.return_date IS NULL
            """
            cursor.execute(query, (self.current_user.get_employee_id(),))
            assets = cursor.fetchall()

            if not assets:
                print("You don't have any allocated assets")
                return

            print("\n{:<10} {:<20} {:<15} {:<15} {:<15} {:<15} {:<20}".format(
                "ID", "Name", "Type", "Serial", "Purchase Date", "Location", "Status"
            ))
            print("-" * 105)

            for asset in assets:
                print("{:<10} {:<20} {:<15} {:<15} {:<15} {:<15} {:<20}".format(
                    asset['asset_id'],
                    asset['name'],
                    asset['type'],
                    asset['serial_number'],
                    str(asset['purchase_date']),
                    asset['location'],
                    asset['status']
                ))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def request_asset(self):
        print("\n==== Request Asset ====")
        try:
            self.view_all_assets()
            asset_id = int(input("\nEnter asset ID to request: "))
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            reservation_date = datetime.now().strftime("%Y-%m-%d")

            if self.service.reserve_asset(
                    asset_id,
                    self.current_user.get_employee_id(),
                    reservation_date,
                    start_date,
                    end_date
            ):
                print("Asset request submitted successfully!")
            else:
                print("Failed to submit asset request")
        except AssetNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def return_asset(self):
        print("\n==== Return Asset ====")
        try:
            self.view_my_assets()
            asset_id = int(input("\nEnter asset ID to return: "))
            return_date = datetime.now().strftime("%Y-%m-%d")

            if self.service.deallocate_asset(
                    asset_id,
                    self.current_user.get_employee_id(),
                    return_date
            ):
                print("Asset returned successfully!")
            else:
                print("Failed to return asset")
        except Exception as e:
            print(f"Error: {e}")

    def request_maintenance(self):
        print("\n==== Request Maintenance ====")
        try:
            self.view_my_assets()
            asset_id = int(input("\nEnter asset ID for maintenance: "))
            description = input("Enter maintenance description: ")
            maintenance_date = datetime.now().strftime("%Y-%m-%d")
            cost = 0.0  # Will be updated by admin

            if self.service.perform_maintenance(asset_id, maintenance_date, description, cost):
                print("Maintenance request submitted successfully!")
            else:
                print("Failed to submit maintenance request")
        except AssetNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def update_my_profile(self):
        print("\n==== Update My Profile ====")
        try:
            employee = self.current_user

            print(f"\nCurrent Profile Details:")
            print(f"Name: {employee.get_name()}")
            print(f"Department: {employee.get_department()}")
            print(f"Email: {employee.get_email()}")

            print("\nEnter new details (leave blank to keep current value):")
            name = input(f"Name [{employee.get_name()}]: ") or employee.get_name()
            department = input(f"Department [{employee.get_department()}]: ") or employee.get_department()
            email = input(f"Email [{employee.get_email()}]: ") or employee.get_email()
            password = input("New password (leave blank to keep current): ")

            updated_employee = Employee(
                employee_id=employee.get_employee_id(),
                name=name,
                department=department,
                email=email,
                password=password if password else None,
                is_admin=employee.get_is_admin()
            )

            if self.service.update_employee(updated_employee, self.current_user):
                print("Profile updated successfully!")
                # Update current user in session
                self.current_user = self.service.get_employee(employee.get_employee_id())
            else:
                print("Failed to update profile")
        except Exception as e:
            print(f"Error: {e}")

    def asset_status_report(self):
        print("\n==== Asset Status Report ====")
        try:
            cursor = self.service.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    a.asset_id,
                    a.name,
                    a.type,
                    a.status,
                    e.name AS owner_name,
                    e.department AS owner_department
                FROM assets a
                LEFT JOIN employees e ON a.owner_id = e.employee_id
                ORDER BY a.status, a.type
            """
            cursor.execute(query)
            assets = cursor.fetchall()

            if not assets:
                print("No assets found")
                return

            print("\n{:<10} {:<20} {:<15} {:<20} {:<20} {:<20}".format(
                "ID", "Name", "Type", "Status", "Owner", "Department"
            ))
            print("-" * 105)

            for asset in assets:
                print("{:<10} {:<20} {:<15} {:<20} {:<20} {:<20}".format(
                    asset['asset_id'],
                    asset['name'],
                    asset['type'],
                    asset['status'],
                    asset['owner_name'] if asset['owner_name'] else "None",
                    asset['owner_department'] if asset['owner_department'] else "None"
                ))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def maintenance_history(self):
        print("\n==== Maintenance History ====")
        try:
            cursor = self.service.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    m.maintenance_id,
                    a.name AS asset_name,
                    m.maintenance_date,
                    m.description,
                    m.cost
                FROM maintenance_records m
                JOIN assets a ON m.asset_id = a.asset_id
                ORDER BY m.maintenance_date DESC
            """
            cursor.execute(query)
            records = cursor.fetchall()

            if not records:
                print("No maintenance records found")
                return

            print("\n{:<10} {:<20} {:<15} {:<30} {:<10}".format(
                "ID", "Asset", "Date", "Description", "Cost"
            ))
            print("-" * 85)

            for record in records:
                print("{:<10} {:<20} {:<15} {:<30} {:<10.2f}".format(
                    record['maintenance_id'],
                    record['asset_name'],
                    str(record['maintenance_date']),
                    record['description'][:27] + "..." if len(record['description']) > 30 else record['description'],
                    record['cost']
                ))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def allocation_history(self):
        print("\n==== Allocation History ====")
        try:
            cursor = self.service.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    aa.allocation_id,
                    a.name AS asset_name,
                    e.name AS employee_name,
                    aa.allocation_date,
                    aa.return_date
                FROM asset_allocations aa
                JOIN assets a ON aa.asset_id = a.asset_id
                JOIN employees e ON aa.employee_id = e.employee_id
                ORDER BY aa.allocation_date DESC
            """
            cursor.execute(query)
            allocations = cursor.fetchall()

            if not allocations:
                print("No allocation records found")
                return

            print("\n{:<10} {:<20} {:<20} {:<15} {:<15}".format(
                "ID", "Asset", "Employee", "Allocation Date", "Return Date"
            ))
            print("-" * 80)

            for alloc in allocations:
                print("{:<10} {:<20} {:<20} {:<15} {:<15}".format(
                    alloc['allocation_id'],
                    alloc['asset_name'],
                    alloc['employee_name'],
                    str(alloc['allocation_date']),
                    str(alloc['return_date']) if alloc['return_date'] else "Active"
                ))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

def main():
    app = MainModule()
    app.login_menu()

if __name__ == "__main__":
    main()