import pytest
from datetime import datetime, timedelta
from ..dao.asset_management_service_impl import AssetManagementServiceImpl
from ..entity.asset import Asset
from ..entity.employee import Employee
from ..exception.asset_not_found_exception import AssetNotFoundException

@pytest.fixture
def service():
    return AssetManagementServiceImpl()

@pytest.fixture
def sample_asset():
    return Asset(
        name="Test Laptop",
        type="laptop",
        serial_number="TEST123",
        purchase_date="2023-01-01",
        location="Office",
        status="in_use",
        owner_id=None
    )

@pytest.fixture
def sample_employee():
    return Employee(
        name="Test User",
        department="IT",
        email="test@example.com",
        password="password123",
        is_admin=False
    )

def test_add_asset(service, sample_asset):
    # Test adding a new asset
    assert service.add_asset(sample_asset) == True

    # Verify the asset was added
    cursor = service.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM assets WHERE serial_number = 'TEST123'")
    asset = cursor.fetchone()
    assert asset is not None
    assert asset['name'] == "Test Laptop"

    # Clean up
    cursor.execute("DELETE FROM assets WHERE serial_number = 'TEST123'")
    service.connection.commit()
    cursor.close()

def test_update_asset(service, sample_asset):
    # First add the asset
    service.add_asset(sample_asset)

    # Get the asset ID
    cursor = service.connection.cursor(dictionary=True)
    cursor.execute("SELECT asset_id FROM assets WHERE serial_number = 'TEST123'")
    asset_id = cursor.fetchone()['asset_id']

    # Update the asset
    updated_asset = Asset(
        asset_id=asset_id,
        name="Updated Laptop",
        type="laptop",
        serial_number="TEST123",
        purchase_date="2023-01-01",
        location="Warehouse",
        status="in_use",
        owner_id=None
    )
    assert service.update_asset(updated_asset) == True

    # Verify the update
    cursor.execute("SELECT * FROM assets WHERE asset_id = %s", (asset_id,))
    asset = cursor.fetchone()
    assert asset['name'] == "Updated Laptop"
    assert asset['location'] == "Warehouse"

    # Clean up
    cursor.execute("DELETE FROM assets WHERE asset_id = %s", (asset_id,))
    service.connection.commit()
    cursor.close()

def test_delete_asset(service, sample_asset):
    # First add the asset
    service.add_asset(sample_asset)

    # Get the asset ID
    cursor = service.connection.cursor(dictionary=True)
    cursor.execute("SELECT asset_id FROM assets WHERE serial_number = 'TEST123'")
    asset_id = cursor.fetchone()['asset_id']

    # Delete the asset
    assert service.delete_asset(asset_id) == True

    # Verify deletion
    cursor.execute("SELECT 1 FROM assets WHERE asset_id = %s", (asset_id,))
    assert cursor.fetchone() is None
    cursor.close()

def test_asset_not_found_exception(service):
    # Try to get a non-existent asset
    with pytest.raises(AssetNotFoundException):
        service.get_asset(99999)

def test_allocate_asset(service, sample_asset, sample_employee):
    # Add test assets and employee
    service.add_asset(sample_asset)
    service.add_employee(sample_employee, sample_employee)  # Using same employee as admin

    # Get IDs
    cursor = service.connection.cursor(dictionary=True)
    cursor.execute("SELECT asset_id FROM assets WHERE serial_number = 'TEST123'")
    asset_id = cursor.fetchone()['asset_id']

    cursor.execute("SELECT employee_id FROM employees WHERE email = 'test@example.com'")
    employee_id = cursor.fetchone()['employee_id']

    # Allocate asset
    assert service.allocate_asset(asset_id, employee_id, "2023-01-01") == True

    # Verify allocation
    cursor.execute("""
        SELECT 1 FROM asset_allocations 
        WHERE asset_id = %s AND employee_id = %s AND return_date IS NULL
    """, (asset_id, employee_id))
    assert cursor.fetchone() is not None

    # Clean up
    cursor.execute("DELETE FROM asset_allocations WHERE asset_id = %s", (asset_id,))
    cursor.execute("UPDATE assets SET owner_id = NULL WHERE asset_id = %s", (asset_id,))
    cursor.execute("DELETE FROM assets WHERE asset_id = %s", (asset_id,))
    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    service.connection.commit()
    cursor.close()