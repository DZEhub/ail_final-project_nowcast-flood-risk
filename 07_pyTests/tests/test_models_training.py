# -*- coding=utf-8 -*-
# This file contains "smoke tests" for the model training functions.
# A smoke test runs the code to see if it executes without crashing.

import sys  # Import sys to manipulate the system path
from pathlib import Path  # Import Path for object-oriented filesystem paths
from unittest.mock import patch  # Import patch for mocking
import pytest

# Skip this test module cleanly when optional training dependency is unavailable.
mlflow = pytest.importorskip("mlflow", reason="mlflow is required for model training smoke tests")

# Add the project's parent directory to the Python path to import project modules.
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "04_ML_Models"))

# Import the main training functions for each model.
from models.prophet.train_prophet import main_train_prophet
from models.xgboost.train_xgboost import main_train_xgboost
from models.lstm.train_lstm_tensorflow import main_train_lstm

# Import the data splitting utility to create test data.
from config.data_utils import split_train_test


@patch('models.prophet.train_prophet.mlflow')
def test_main_train_prophet_smoke(mock_mlflow, mock_clean_dataframe):
    """
    Smoke test for the Prophet model training function.
    It runs the function with mock data to ensure it completes without errors.
    MLflow is mocked to prevent actual logging during the test.
    """
    # Create small train/test splits from the mock data.
    train_df, test_df, split_date = split_train_test(mock_clean_dataframe)
    # Run the Prophet training function.
    model, forecast, metrics = main_train_prophet(train_df, test_df, "site", "station", "code", "measure", split_date, "title")
    # Assert that the function returns the expected artifacts.
    assert model is not None, "the training function did not return a model."
    assert forecast is not None, "the training function did not return a forecast."
    assert metrics is not None, "the training function did not return metrics."


@patch('models.xgboost.train_xgboost.mlflow')
def test_main_train_xgboost_smoke(mock_mlflow, mock_clean_dataframe):
    """
    Smoke test for the XGBoost model training function.
    Verifies that the training process runs to completion.
    """
    # # Create small train/test splits.
    train_df, test_df, split_date = split_train_test(mock_clean_dataframe)
    # Run the XGBoost training function.
    forecast = main_train_xgboost(train_df, test_df, "site", "station", "code", "measure", split_date, test_df, 42, "title")
    # Assert that a forecast DataFrame is returned.
    assert forecast is not None


@patch('models.lstm.train_lstm_tensorflow.mlflow')
def test_main_train_lstm_smoke(mock_mlflow, mock_clean_dataframe):
    """
    Smoke test for the TensorFlow LSTM model training function.
    Ensures the LSTM training pipeline executes without errors.
    """
    # Create small train/test splits.
    train_df, test_df, split_date = split_train_test(mock_clean_dataframe)
    # Run the LSTM training function.
    forecast = main_train_lstm(train_df, test_df, "site", "station", "code", "measure", split_date, test_df, "title")
    # Assert that a forecast DataFrame is returned.
    assert forecast is not None