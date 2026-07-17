# -*- coding=utf-8 -*-
# This file defines shared fixtures for all tests.
# Fixtures are reusable objects for tests, like mock data.

import pytest  # Import the pytest framework
import pandas as pd  # Import pandas for data manipulation
from datetime import datetime  # Import datetime for date handling


@pytest.fixture(scope="session")
def mock_raw_dataframe():
    """
    Creates a mock raw DataFrame fixture.
    This simulates the data structure returned by the fetch_obs_elab API call.
    The 'scope="session"' means this fixture is created only once per test session.
    """
    # Define the data for the mock DataFrame
    data = {
        "date_obs": pd.to_datetime(["2023-01-01 10:00:00", "2023-01-01 11:00:00", "2023-01-01 12:00:00"]),
        "resultat_obs": [10.5, 11.0, 10.8]
    }
    # Create and return the pandas DataFrame
    return pd.DataFrame(data)


@pytest.fixture(scope="session")
def mock_clean_dataframe():
    """
    Creates a mock cleaned DataFrame fixture.
    This simulates the data structure after the prepare_series function has been applied.
    It's used to test functions that expect cleaned data, like splitting or model training.
    """
    # Define the data for the mock DataFrame with 'ds' and 'y' columns
    data = {
        "ds": pd.to_datetime(["2023-01-01 10:00:00", "2023-01-01 11:00:00", "2023-01-01 12:00:00", "2023-01-01 13:00:00", "2023-01-01 14:00:00"]),
        "y": [10.5, 11.0, 10.8, 11.2, 11.5]
    }
    # Create and return the pandas DataFrame
    return pd.DataFrame(data)