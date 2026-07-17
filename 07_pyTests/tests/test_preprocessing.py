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

# ===================================
# Sample DataFrame for testing
# ===================================


# mock_raw_dataframe is a pytest fixture that creates a sample DataFrame for testing purposes. 
# It is defined with a module scope, meaning it will be created once per test module and can be reused across multiple tests.
def test_load_data(mock_raw_dataframe):
    # Test loading data from a CSV file
    # Generate the sample DataFrame
    df = mock_raw_dataframe
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_clean_data(mock_raw_dataframe):
    # Test cleaning data (removing NaN values)
    test_df = mock_raw_dataframe.copy()
    # Call the function under test with the mock data.
    clean_df = prepare_series(test_df)
    assert clean_df.isnull().sum().sum() == 0, "There are still NaN values in the cleaned DataFrame."  # Check that all NaN values are removed
    # assert clean_df['ds'].dtype == 'datetime64[ns]', "'ds' column is not of type datetime64[ns]"  # Ensure "ds" column is datetime64
    assert pd.api.types.is_datetime64_any_dtype(clean_df["ds"]), "'ds' column is not of datetime64 dtype."
    assert clean_df['y'].dtype == 'float64', "'y' column is not of type float"  # Ensure "y" column is float