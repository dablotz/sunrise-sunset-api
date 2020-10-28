from behave import *
from datetime import datetime, timedelta
import requests


# A valid latitude/longitude pair (top of Prescott Park in Medford, Oregon)
VALID_COORDINATES = {"lat": 42.3511625, "lng": -122.785302}
SUNRISE_URL = "https://api.sunrise-sunset.org/json"


@given('a valid latitude and longitude')
def step_impl(context):
    # Creating the dictionary of parameters to pass to the API
    context.data = {"lat": VALID_COORDINATES.get("latitude"),
                    "lng": VALID_COORDINATES.get("longitude")}


@given('a valid latitude, longitude, and date')
def step_impl(context):
    # Creating the dictionary of parameters to pass to the API
    # Sending 'yesterday' as the date
    context.data = {"lat": VALID_COORDINATES.get("latitude"),
                    "lng": VALID_COORDINATES.get("longitude"),
                    "date": datetime.today() - timedelta(days=1)}


@given('a request that specifies unformatted data in the response')
def step_impl(context):
    # Creating the dictionary of parameters to pass to the API
    # Setting unformatted to 0 (default is 1) to get unformatted data in the response
    context.data = {"lat": VALID_COORDINATES.get("latitude"),
                    "lng": VALID_COORDINATES.get("longitude"),
                    "formatted": 0}


@given('a request with an invalid date')
def step_impl(context):
    # Creating the dictionary of parameters to pass to the API
    # Sending 1 as the date
    context.data = {"lat": VALID_COORDINATES.get("latitude"),
                    "lng": VALID_COORDINATES.get("longitude"),
                    "date": 1}


@when('I send the request')
def step_impl(context):
    context.response = requests.get(SUNRISE_URL, params=context.data)
    context.formatted_response = requests.get(SUNRISE_URL, params=VALID_COORDINATES)


@then('sunrise and sunset times are included in the response')
def step_impl(context):
    response = context.response.json()
    assert("sunrise" in response["results"])
    assert(response["results"]["sunrise"] is not None)
    assert("sunset" in response["results"])
    assert(response["results"]["sunset"] is not None)


@then('the dates and times in the response are unformatted')
def step_impl(context):
    response = context.response.json()
    formatted_response = context.formatted_response.json()

    for k, v in response["results"]:
        if k != "day_length":
            # simply asserting that the strings are not identical
            assert(v != formatted_response["results"][k])


@then('the status is shown as INVALID_DATE')
def step_impl(context):
    response = context.response.json()
    assert(response["status"] == "INVALID_DATE")


@then('the date in the response was the date in the request')
def step_impl(context):
    response = context.response.json()
    formatted_response = context.formatted_response.json()

    comp_date = context.data.get("date", datetime.today())

