"""File for handling operations and values that are weather-related."""

import numpy as np

# https://climateknowledgeportal.worldbank.org/country/romania/climate-data-historical
"""Mean temperature for Romania in 2021, according to the source."""
TEMP_MEAN_2021 = 10.35

"""Mean temperature of each month for Romania in 2021."""
MONTH_TEMP_MEAN_2021 = np.array([-1.71, 0.21, 4.7, 10.37, 15.39, 19.17, 20.95, 20.91, 16.09, 10.65, 5.13, -0.25])

"""I am using the means from above to estimate the variance of the average temperature."""
VARIANCE = 1 / 12 * np.sum(np.square(np.subtract(MONTH_TEMP_MEAN_2021, TEMP_MEAN_2021)))

"""With the obtained variance I get the standard deviation."""
STANDARD_DEVIATION = np.sqrt(VARIANCE)


def get_temp():
    """
    Get a random temperature from the normal distribution having the mean and standard deviation calculated above.
    The value is rounded and then converted to an integer.
    """
    return int(round(np.random.normal(TEMP_MEAN_2021, STANDARD_DEVIATION)))


def get_rain():
    """Get a random value from the (0, 2) interval from a uniform distribution. The result is rounded to 1 digit."""
    return round(np.random.uniform(0, 2), 1)


def get_wind():
    """
    Get a random value from the (0, 50) interval from a uniform distribution.
    The result is rounded and then converted to an integer.
    """
    return int(round(np.random.uniform(0, 50)))
