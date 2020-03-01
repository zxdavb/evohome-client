"""Test evohomeclient2"""
import requests_mock

from . import EvohomeClient

URL_ROOT = "https://tccna.honeywell.com/WebAPI/emea/api/v1/"

INSTALLATION_DATA = """[{
    "locationInfo": {
        "locationId": "locationId"
    },
    "gateways": [
        {
            "gatewayInfo": {
                "location": "location",
                "gatewayId": "gatewayId"
            },
            "temperatureControlSystems": [
                {
                    "systemId": "sysId",
                     "zones": []
                }
            ]
        }
    ]
}]"""

INSTALLATION_DATA_MULTIPLE = """[{
    "locationInfo": {
        "locationId": "locationId"
    },
    "gateways": [
        {
            "gatewayInfo": {
                "location": "location",
                "gatewayId": "gatewayId"
            },
            "temperatureControlSystems": [
                {
                    "systemId": "sysId",
                    "zones": []
                }
            ]
        },
        {
            "gatewayInfo": {
                "location": "location",
                "gatewayId": "gatewayId"
            },
            "temperatureControlSystems": [
                {
                    "systemId": "sysId",
                    "zones": []
                }
            ]
        }
    ]
}]"""

LOCATION_DATA = """{
    "locationInfo": {
        "locationId": "locationId"
    },
    "gateways": [
        {
                "gatewayId": "gatewayId",
            "gatewayInfo": {
                "location": "location"
            },
            "temperatureControlSystems": [
                {
                    "systemId": "sysId",
                    "zones": [],
                    "systemModeStatus": "active",
                    "activeFaults": []
                }
            ]
        }
    ]
}"""

LOCATION_DATA_MULTIPLE = """{
    "locationInfo": {
        "locationId": "locationId"
    },
    "gateways": [
        {
                "gatewayId": "gatewayId",
            "gatewayInfo": {
                "location": "location"
            },
            "temperatureControlSystems": [
                {
                    "systemId": "sysId",
                    "zones": [],
                    "systemModeStatus": "active",
                    "activeFaults": []
                }
            ]
        },
        {
                "gatewayId": "gatewayId",
            "gatewayInfo": {
                "location": "location"
            },
            "temperatureControlSystems": [
                {
                    "systemId": "sysId",
                    "zones": [],
                    "systemModeStatus": "active",
                    "activeFaults": []
                }
            ]
        }
    ]
}"""

AUTH_RESPONSE = """
  {
    "access_token": "1234",
    "expires_in": 30,
    "refresh_token": "refresh"
  }
"""

USER_RESPONSE = """
  {
    "name": "name",
    "userId": "userId"
  }
"""

GATEWAY_RESPONSE = """
{}
"""


@requests_mock.Mocker()
def test_user_account(mock):
    """test that user account is successful"""
    mock.post(
        "https://tccna.honeywell.com/Auth/OAuth/Token",
        status_code=200,
        text=AUTH_RESPONSE,
    )
    mock.get(
        URL_ROOT + "userAccount", status_code=200, text=USER_RESPONSE,
    )
    mock.get(
        URL_ROOT + "location/installationInfo"
        "?userId=userId&includeTemperatureControlSystems=True",
        status_code=200,
        text=INSTALLATION_DATA,
    )
    mock.get(
        URL_ROOT + "location/locationId/status"
        "?includeTemperatureControlSystems=True",
        status_code=200,
        text=LOCATION_DATA,
    )

    # try:
    client = EvohomeClient("username", "password")
    print(client)
    info = client.user_account()
    assert info["name"] == "name"
    assert info["userId"] == "userId"


@requests_mock.Mocker()
def test_temperatures(mock):
    """test that user account is successful"""
    mock.post(
        "https://tccna.honeywell.com/Auth/OAuth/Token",
        status_code=200,
        text=AUTH_RESPONSE,
    )
    mock.get(
        URL_ROOT + "userAccount", status_code=200, text=USER_RESPONSE,
    )
    mock.get(
        URL_ROOT + "location/installationInfo"
        "?userId=userId&includeTemperatureControlSystems=True",
        status_code=200,
        text=INSTALLATION_DATA,
    )
    mock.get(
        URL_ROOT + "location/locationId/status"
        "?includeTemperatureControlSystems=True",
        status_code=200,
        text=LOCATION_DATA,
    )

    # try:
    client = EvohomeClient("username", "password")
    print(client)
    list(client.temperatures())


@requests_mock.Mocker()
def test_gateway(mock):
    """test that user account is successful"""
    mock.post(
        "https://tccna.honeywell.com/Auth/OAuth/Token",
        status_code=200,
        text=AUTH_RESPONSE,
    )
    mock.get(
        URL_ROOT + "userAccount", status_code=200, text=USER_RESPONSE,
    )
    mock.get(
        URL_ROOT + "location/installationInfo"
        "?userId=userId&includeTemperatureControlSystems=True",
        status_code=200,
        text=INSTALLATION_DATA,
    )
    mock.get(
        URL_ROOT + "location/locationId/status"
        "?includeTemperatureControlSystems=True",
        status_code=200,
        text=LOCATION_DATA,
    )
    mock.get(
        URL_ROOT + "gateway", status_code=200, text=GATEWAY_RESPONSE,
    )

    # try:
    client = EvohomeClient("username", "password")
    client.gateway()


@requests_mock.Mocker()
def test_single_settings(mock):
    """Test can change different statuses"""
    mock.post(
        "https://tccna.honeywell.com/Auth/OAuth/Token",
        status_code=200,
        text=AUTH_RESPONSE,
    )
    mock.get(
        URL_ROOT + "userAccount", status_code=200, text=USER_RESPONSE,
    )
    mock.get(
        URL_ROOT + "location/installationInfo"
        "?userId=userId&includeTemperatureControlSystems=True",
        status_code=200,
        text=INSTALLATION_DATA,
    )
    mock.get(
        URL_ROOT + "location/locationId/status"
        "?includeTemperatureControlSystems=True",
        status_code=200,
        text=LOCATION_DATA,
    )
    mock.put(
        URL_ROOT + "temperatureControlSystem/sysId/mode", status_code=200, text="",
    )
    client = EvohomeClient("username", "password", debug=True)

    client.set_status_away()
    client.set_status_eco()
    client.set_status_custom()
    client.set_status_dayoff()
    client.set_status_heatingoff()
    client.set_status_reset()
    client.set_status_normal()


@requests_mock.Mocker()
def test_multi_zone_failure(mock):
    """Confirm that exception is thrown for multiple locations"""
    mock.post(
        "https://tccna.honeywell.com/Auth/OAuth/Token",
        status_code=200,
        text=AUTH_RESPONSE,
    )
    mock.get(
        URL_ROOT + "userAccount", status_code=200, text=USER_RESPONSE,
    )
    mock.get(
        URL_ROOT + "location/installationInfo"
        "?userId=userId&includeTemperatureControlSystems=True",
        status_code=200,
        text=INSTALLATION_DATA_MULTIPLE,
    )
    mock.get(
        URL_ROOT + "location/locationId/status"
        "?includeTemperatureControlSystems=True",
        status_code=200,
        text=LOCATION_DATA_MULTIPLE,
    )
    mock.put(
        URL_ROOT + "temperatureControlSystem/sysId/mode", status_code=200, text="",
    )
    client = EvohomeClient("username", "password", debug=True)

    try:
        client.set_status_away()
        assert False  # shouldn't get here
    except:
        assert True
