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
from config.data_utils import prepare_series, split_train_test, fetch_obs_elab, create_features


def test_prepare_series(mock_raw_dataframe):
    """
    Tests the prepare_series function.
    It checks if the function correctly renames columns, converts date types, and handles data.
    Args:
        mock_raw_dataframe (pd.DataFrame): A pytest fixture providing a sample raw DataFrame.
    """
    raw_df = mock_raw_dataframe.copy()
    # Call the function under test with the mock data.
    clean_df = prepare_series(raw_df)
    
    # Assert that the returned object is a pandas DataFrame.
    assert isinstance(clean_df, pd.DataFrame), "The output of prepare_series is not a pandas DataFrame."
    assert not clean_df.empty, "The output of prepare_series is an empty DataFrame."
    # Assert that the expected columns 'ds' and 'y' are present.
    assert "ds" in clean_df.columns, f"'ds' column is missing in the cleaned DataFrame: {clean_df.columns}"
    assert "y" in clean_df.columns, f"'y' column is missing in the cleaned DataFrame: {clean_df.columns}"
    # Assert that the 'ds' column has been converted to datetime objects.
    assert pd.api.types.is_datetime64_any_dtype(clean_df["ds"]), "'ds' column is not of datetime64 dtype."


def test_split_train_test(mock_clean_dataframe):
    """
    Tests the split_train_test function.
    It verifies that the data is split into training and testing sets correctly based on the given ratio.
    Args:
        mock_clean_dataframe (pd.DataFrame): A pytest fixture providing a sample cleaned DataFrame.
    """
    clean_df = mock_clean_dataframe.copy()
    # Use the cleaned dataframe directly from the fixture
    feature_df = create_features(clean_df)
    # Define the training ratio for the split.
    train_ratio = 0.8
    # Call the function under test.
    train_df, test_df, split_date = split_train_test(feature_df, train_ratio=train_ratio)

    # Assert that the function returns three non-null values.
    assert train_df is not None, "train_df is None"
    assert test_df is not None, "test_df is None"
    assert split_date is not None, "split_date is None"
    
    assert len(train_df) + len(test_df) == len(feature_df), "Total length of train and test sets does not match the original DataFrame length."  # Check that the total length matches the original DataFrame
    assert train_df.shape[0] == len(train_df), "Number of samples in train_df does not match its length."  # Check that the number of samples in train_df matches its length
    assert test_df.shape[0] == len(test_df), "Number of samples in test_df does not match its length."  # Check that the number of samples in test_df matches its length
    assert not train_df.empty, "train_df is empty."  # Check that train_df is not empty
    assert not test_df.empty, "test_df is empty."  # Check that test_df is not empty
    
    # Assert that the length of the training set is correct based on the ratio.
    assert len(train_df) == int(len(feature_df) * train_ratio), "absolute difference between train length and expected length based on ratio does not match the original DataFrame length."
    # Assert that the length of the test set is correct.
    assert len(test_df) == len(feature_df) - len(train_df), "absolute difference between train and test lengths does not match the original DataFrame length."


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


def test_create_features(mock_clean_dataframe):
    """
    Tests the create_features function.
    It checks if the function correctly generates new features from the cleaned DataFrame.
    Args:
        mock_clean_dataframe (pd.DataFrame): A pytest fixture providing a sample cleaned DataFrame.
    """
    # Test feature engineering (creating a new feature)
    test_df = mock_clean_dataframe.copy()
    # Call the function under test with the mock data.
    feature_df = create_features(test_df)
    # Assert that the returned object is a pandas DataFrame.
    assert isinstance(feature_df, pd.DataFrame), "The output of create_features is not a pandas DataFrame."
    assert not feature_df.empty, "The output of create_features is an empty DataFrame."
    # Assert that new feature columns are present in the DataFrame.
    expected_feature_columns = ["hour", "dayofweek", "quarter", "month", "year", "dayofyear", "dayofmonth", "weekofyear"]  # Replace with actual expected feature names
    for col in expected_feature_columns:
        assert col in feature_df.columns, f"Expected feature column '{col}' is missing in the DataFrame."
        assert pd.api.types.is_numeric_dtype(feature_df[col]), f"Feature column '{col}' is not of numeric dtype."
        # assert feature_df[col].dtype == float, f"Feature column '{col}' is not of type float."
        
        
