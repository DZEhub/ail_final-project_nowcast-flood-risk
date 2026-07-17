# -*- coding=utf-8 -*-
# This file contains unit tests for the data utility functions.

import sys  # Import sys to manipulate the system path
from pathlib import Path  # Import Path for object-oriented filesystem paths
import pandas as pd  # Import pandas for data manipulation
from unittest.mock import patch, MagicMock  # Import mocking utilities

# Add the project's parent directory to the Python path.
# This allows us to import modules from the 'config' directory (e.g., data_utils).
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Import the functions to be tested from your project's data_utils module.
from config.data_utils import prepare_series, split_train_test, fetch_obs_elab


def test_prepare_series(mock_raw_dataframe):
    """
    Tests the prepare_series function.
    It checks if the function correctly renames columns, converts date types, and handles data.
    Args:
        mock_raw_dataframe (pd.DataFrame): A pytest fixture providing a sample raw DataFrame.
    """
    # Call the function under test with the mock data.
    clean_df = prepare_series(mock_raw_dataframe)

    # Assert that the returned object is a pandas DataFrame.
    assert isinstance(clean_df, pd.DataFrame)
    # Assert that the expected columns 'ds' and 'y' are present.
    assert "ds" in clean_df.columns
    assert "y" in clean_df.columns
    # Assert that the 'ds' column has been converted to datetime objects.
    assert pd.api.types.is_datetime64_any_dtype(clean_df["ds"])


def test_split_train_test(mock_clean_dataframe):
    """
    Tests the split_train_test function.
    It verifies that the data is split into training and testing sets correctly based on the given ratio.
    Args:
        mock_clean_dataframe (pd.DataFrame): A pytest fixture providing a sample cleaned DataFrame.
    """
    # Define the training ratio for the split.
    train_ratio = 0.8
    # Call the function under test.
    train_df, test_df, split_date = split_train_test(mock_clean_dataframe, train_ratio=train_ratio)

    # Assert that the function returns three non-null values.
    assert train_df is not None
    assert test_df is not None
    assert split_date is not None
    # Assert that the length of the training set is correct based on the ratio.
    assert len(train_df) == int(len(mock_clean_dataframe) * train_ratio)
    # Assert that the length of the test set is correct.
    assert len(test_df) == len(mock_clean_dataframe) - len(train_df)


@patch('config.data_utils.requests.get')
def test_fetch_obs_elab(mock_requests_get, mock_raw_dataframe):
    """
    Tests the fetch_obs_elab function by mocking the API call.
    It ensures that the function correctly processes a successful API response.
    Args:
        mock_requests_get (MagicMock): The mocked requests.get function.
        mock_raw_dataframe (pd.DataFrame): A fixture to simulate the API response data.
    """
    # Create a mock response object.
    mock_response = MagicMock()
    # Set the status code to 200 (OK).
    mock_response.status_code = 200
    # Configure the mock to return a JSON payload similar to the real API.
    mock_response.json.return_value = {"data": mock_raw_dataframe.to_dict(orient="records")}
    # Assign the mock response to the mocked requests.get call.
    mock_requests_get.return_value = mock_response

    # Call the function that makes the API request.
    result_df = fetch_obs_elab("station_code", "start_date", "end_date", "measure")

    # Assert that the function returns a DataFrame with the expected number of rows.
    assert len(result_df) == len(mock_raw_dataframe)