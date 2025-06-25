from assets.util.db_conn_util import DBConnUtil
from assets.util.password_util import PasswordUtil

def insert_sample_data():
    connection = DBConnUtil.get_connection(property_file_name='config.properties')
    cursor = connection.cursor(dictionary=True)

    try:
        # Clear existing non-admin data (optional)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM reservations")
        cursor.execute("DELETE FROM asset_allocations")
        cursor.execute("DELETE FROM maintenance_records")
        cursor.execute("DELETE FROM assets WHERE owner_id IS NOT NULL")
        cursor.execute("DELETE FROM employees WHERE is_admin = FALSE")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        # Insert only regular employees
        employees = [
          # ('Admin User', 'IT', 'admin@company.com', PasswordUtil.hash_password('secret'), True),  --> already inserted
            ('Ruthra', 'AIML', 'ruthra@company.com', PasswordUtil.hash_password('password123'), False),
            ('Varshan', 'HR', 'varshan@company.com', PasswordUtil.hash_password('password123'), False)
        ]
        cursor.executemany("""
            INSERT INTO employees (name, department, email, password, is_admin)
            VALUES (%s, %s, %s, %s, %s)
        """, employees)

        # Get the inserted employee IDs
        cursor.execute("SELECT employee_id, email FROM employees WHERE is_admin = FALSE")
        employee_ids = {row['email']: row['employee_id'] for row in cursor.fetchall()}

        # Insert assets assigned to regular employees
        assets = [
            ('MacBook Pro 16"', 'Laptop', 'MPB20230001', '2023-01-15', 'Office', 'in_use', employee_ids['john.doe@company.com']),
            ('Canon EOS R5', 'Camera', 'CER20230002', '2023-02-20', 'Studio', 'in_use', employee_ids['jane.smith@company.com']),
            ('Dell XPS 15', 'Laptop', 'DXP20220001', '2022-11-10', 'Warehouse', 'decommissioned', None)
        ]
        cursor.executemany("""
            INSERT INTO assets (name, type, serial_number, purchase_date, location, status, owner_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, assets)

        # Get the inserted asset IDs
        cursor.execute("SELECT asset_id, serial_number FROM assets")
        asset_ids = {row['serial_number']: row['asset_id'] for row in cursor.fetchall()}

        # Insert maintenance records for employee assets
        cursor.execute("""
            INSERT INTO maintenance_records (asset_id, maintenance_date, description, cost)
            VALUES (%s, %s, %s, %s)
        """, (asset_ids['MPB20230001'], '2023-05-15', 'Battery replacement', 89.99))

        # Insert asset allocations
        allocations = [
            (asset_ids['MPB20230001'], employee_ids['john.doe@company.com'], '2023-04-01', None),
            (asset_ids['CER20230002'], employee_ids['jane.smith@company.com'], '2023-04-15', None)
        ]
        cursor.executemany("""
            INSERT INTO asset_allocations (asset_id, employee_id, allocation_date, return_date)
            VALUES (%s, %s, %s, %s)
        """, allocations)

        # Insert reservations between employees
        cursor.execute("""
            INSERT INTO reservations (asset_id, employee_id, reservation_date, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (asset_ids['MPB20230001'], employee_ids['jane.smith@company.com'], '2023-05-01', '2023-06-01', '2023-06-15', 'pending'))

        connection.commit()
        print("✅ Sample employee data inserted successfully!")

    except Exception as e:
        connection.rollback()
        print(f"❌ Error inserting sample data: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    insert_sample_data()