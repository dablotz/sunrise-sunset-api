Feature: sunrise api

  Scenario: Specifying a valid latitude and longitude in a request returns a successful response
    Given a valid latitude and longitude
    When I send the request
    Then sunrise and sunset times are included in the response
    And the date in the response was the date in the request
    And the day length accurately represents the amount of time between sunrise and sunset

  Scenario: Specifying a valid latitude, longitude, and date in a request returns the sunrise and sunset information
  for a given date
    Given a valid latitude, longitude, and date
    When I send the request
    Then sunrise and sunset times are included in the response
    And the date in the response was the date in the request
    And the day length accurately represents the amount of time between sunrise and sunset

  Scenario: Requesting an unformatted response returns unformatted data in the response
    Given a request that specifies unformatted data in the response
    When I send the request
    Then the dates and times in the response are unformatted

  Scenario: Sending an invalid or empty date returns a response with a status of INVALID_DATE
    Given a request with an invalid date
    When I send the request
    Then the status is shown as INVALID_DATE