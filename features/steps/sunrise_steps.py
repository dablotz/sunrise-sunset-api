from behave import *
from datetime import datetime, timedelta
import requests


# A valid latitude/longitude pair (google maps pin for Boston)
VALID_COORDINATES = {"lat": 42.360081, "lng": -71.058884}
SUNRISE_URL = "https://api.sunrise-sunset.org/json"


@given('a valid latitude and longitude')
def step_impl(context):
    # Creating the dictionary of parameters to pass to the API
    context.data = {"lat": VALID_COORDINATES.get("lat"),
                    "lng": VALID_COORDINATES.get("lng")}


@given('a valid latitude, longitude, and date')
def step_impl(context):
    # Creating the dictionary of parameters to pass to the API
    # Sending 'yesterday' as the date
    context.data = {"lat": VALID_COORDINATES.get("lat"),
                    "lng": VALID_COORDINATES.get("lng"),
                    "date": datetime.today().date() - timedelta(days=1)}


@given('a request that specifies unformatted data in the response')
def step_impl(context):
    # Creating the dictionary of parameters to pass to the API
    # Setting unformatted to 0 (default is 1) to get unformatted data in the response
    context.data = {"lat": VALID_COORDINATES.get("lat"),
                    "lng": VALID_COORDINATES.get("lng"),
                    "formatted": 0}


@given('a request with an invalid date')
def step_impl(context):
    # Creating the dictionary of parameters to pass to the API
    # Sending 1 as the date
    context.data = {"lat": VALID_COORDINATES.get("lat"),
                    "lng": VALID_COORDINATES.get("lng"),
                    "date": 1}


@when('I send the request')
def step_impl(context):
    context.response = requests.get(SUNRISE_URL, params=context.data).json()

    # Forcing the formatted flag to 0 for an unformatted response
    # I found the unformatted times easier to work with
    # so I added this second request
    context.data["formatted"] = 0
    context.unformatted_response = requests.get(SUNRISE_URL, params=context.data).json()


@then('sunrise and sunset times are included in the response')
def step_impl(context):
    response = context.response
    assert("sunrise" in response["results"])
    assert(response["results"]["sunrise"] is not None)
    assert("sunset" in response["results"])
    assert(response["results"]["sunset"] is not None)


@then('the dates and times in the response are unformatted')
def step_impl(context):
    response = context.response

    for item in response["results"]:
        if item != "day_length":
            # Attempt to convert the timestamps in the response to datetime objects
            try:
                datetime.fromisoformat(response["results"][item])
            except ValueError:
                assert()
        else:
            assert(isinstance(response["results"]["day_length"], int))


@then('the status is shown as INVALID_DATE')
def step_impl(context):
    response = context.response
    assert(response["status"] == "INVALID_DATE")


@then('the date in the response was the date in the request')
def step_impl(context):
    # Using the unformatted response because the date is not included in a formatted response.
    unformatted_response = context.unformatted_response

    # Getting the date from the request - either a specified day or today (the API's default)
    if "date" not in context.data:
        comp_date = datetime.today().date()
    else:
        comp_date = context.data.get("date")

    resp_date = datetime.fromisoformat(unformatted_response["results"]["sunrise"]).date()

    assert(comp_date == resp_date)


@then('the day length accurately represents the amount of time between sunrise and sunset')
def step_impl(context):
    # Using the unformatted numbers for ease
    sunrise = datetime.fromisoformat(context.unformatted_response["results"]["sunrise"])
    sunset = datetime.fromisoformat(context.unformatted_response["results"]["sunset"])
    day_length = timedelta(seconds=context.unformatted_response["results"]["day_length"])

    assert(sunrise + day_length == sunset)
