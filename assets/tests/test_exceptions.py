import pytest
from ..dao.asset_management_service_impl import AssetManagementServiceImpl
from ..exception.asset_not_found_exception import AssetNotFoundException
from ..exception.asset_not_maintained_exception import AssetNotMaintainedException

def test_asset_not_found_exception():
    with pytest.raises(AssetNotFoundException) as excinfo:
        raise AssetNotFoundException(123)
    assert "Asset with ID 123 not found" in str(excinfo.value)

def test_asset_not_maintained_exception():
    with pytest.raises(AssetNotMaintainedException) as excinfo:
        raise AssetNotMaintainedException(456)
    assert "Asset with ID 456 has not been maintained in the last 2 years" in str(excinfo.value)