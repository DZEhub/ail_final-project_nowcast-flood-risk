# -*- coding=utf-8 -*-
# This file defines shared fixtures for all tests.
# Fixtures are reusable objects for tests, like mock data.

import pytest  # Import the pytest framework
from pathlib import Path  # Import Path for object-oriented filesystem paths
import pandas as pd  # Import pandas for data manipulation
from datetime import datetime  # Import datetime for date handling
import numpy as np  # Import numpy for array handling


@pytest.fixture(scope="session")
def mock_raw_dataframe():
    """
    Creates a mock raw DataFrame fixture.
    This simulates the data structure returned by the fetch_obs_elab API call.
    The 'scope="session"' means this fixture is created only once per test session.
    """
    # set the path to the CSV file containing the original data raw to test: mock DataFrame
    raw_data_file = Path(__file__).resolve().parent / "test_raw_obs_elab_A2350200.csv"
    print(raw_data_file)
    
    # Create and return the pandas DataFrame, parsing the date column
    return pd.read_csv(raw_data_file) #, sep=";", parse_dates=["date_obs_elab"])


@pytest.fixture(scope="session")
def mock_clean_dataframe():
    """
    Creates a mock cleaned DataFrame fixture.
    This simulates the data structure after the prepare_series function has been applied.
    It's used to test functions that expect cleaned data, like splitting or model training.
    """
    # set the path to the CSV file containing the data cleaned to test: mock DataFrame with 'ds' and 'y' columns
    clean_data_file = Path(__file__).resolve().parent / "test_clean_obs_elab_A2350200.csv"
    print(clean_data_file)
    
    clean_df = pd.read_csv(clean_data_file)
    clean_df['ds'] = pd.to_datetime(clean_df['ds'], errors='coerce')
    # clean_df['y'] = pd.to_numeric(clean_df['y'], errors='coerce')

    # Create and return the pandas DataFrame
    return clean_df


"""
==================================================================
Model Testing in the Mock ML Project
==================================================================
"""


# Sample DataFrame as a fixture
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'feature': [1, 2, 3, 4],
        'target': [2, 4, 6, 8]
    })


def sample_data_cleaned():
    return pd.DataFrame({
        'ds': [1, 2, 3, 4],
        'y': [2, 4, 6, 8]
    })


@pytest.fixture
def sample_train_data():
    X = np.array([[1], [2], [3], [4]])
    y = np.array([2, 4, 6, 8])
    return X, y


@pytest.fixture
def sample_test_data():
    X_test = np.array([[5], [6]])
    y_test = np.array([10, 12])
    return X_test, y_test


@pytest.fixture
def edge_case_data():
    empty_data = (np.array([]), np.array([]))
    mismatched_data = (np.array([[1], [2], [3]]), np.array([2, 4]))
    nan_data = (np.array([[1], [2], [np.nan]]), np.array([2, 4, 6]))
    return empty_data, mismatched_data, nan_data
