import pytest
import pandas as pd
import numpy as np


def test_check_data_types(mock_clean_dataframe):
    # Check data types using pandas.testing
    expected_dtypes = pd.Series({
        # 'ds' should be datetime with nanosecond/micro precision, which is the pandas default.
        'ds': np.dtype('datetime64[ns]'),
        # 'y' represents water level, which is a int or float.
        'y': np.dtype('int64')
    })
    # Assert that the dtypes of the DataFrame columns match the expected dtypes.
    # We set check_names=False because the name of the dtypes Series itself is not relevant.
    pd.testing.assert_series_equal(mock_clean_dataframe.dtypes, expected_dtypes, check_names=False)
