# -*- coding=utf-8 -*-
import pandas as pd
import numpy as np
import requests
import sys
from pathlib import Path

# Absolute path of this script's folder: .../Dev/python_apps/data_collection
CURRENT_DIR = Path(__file__).resolve().parent.parent
# Add folder to import search path once
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

# 4) Import from files inside CONFIG_DIR
from config.sites import API_BASE_URL

# Define the column names for the datetime and target variable in the raw dataset
DATETIME_COLUMN_NAME = "date_obs_elab"
TARGET_COLUMN_NAME = "resultat_obs_elab"


def fetch_obs_elab(code_station: str, start_date: str, end_date: str, measure: str) -> pd.DataFrame:
    """Fetch elaborated hydrometric observations from Hub'Eau and return a DataFrame."""
    endpoint = f"{API_BASE_URL}/obs_elab"
    params = {
        "code_entite": code_station,
        "date_debut_obs_elab": start_date,
        "date_fin_obs_elab": end_date,
        "size": 20000,
        "format": "json",
        "grandeur_hydro_elab": measure,
    }
    
    try:
        response = requests.get(endpoint, params=params, timeout=45)
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:
        print(f"API error: {exc}")
        return pd.DataFrame()

    rows = payload.get("data", []) if isinstance(payload, dict) else []
    df = pd.DataFrame(rows)
    return df


def split_train_test(series: pd.DataFrame, train_ratio: float = 0.8, split_by_ratio=True, SPLIT_DATE="2024-01-01"):
    """Split time series into chronological train and test sets."""
    if len(series) < 20:
        return None, None, SPLIT_DATE
    
    if split_by_ratio:
        train_size = max(int(len(series) * train_ratio), 10)
        train_size = min(train_size, len(series) - 5)
        train_df = series.iloc[:train_size].copy()
        test_df = series.iloc[train_size:].copy()
        SPLIT_DATE = train_df.index[-1] if 'ds' not in train_df.columns else train_df['ds'].iloc[-1]
        return train_df, test_df, str(SPLIT_DATE)[:10]
    else:
        # If the index is not datetime but 'ds' exists
        if 'ds' in series.columns:
            mask_selection = series['ds'] < SPLIT_DATE
        else:
            mask_selection = series.index < SPLIT_DATE
        train_df = series[mask_selection].copy()
        test_df = series[~mask_selection].copy()
        ratio = len(train_df) / len(series) if len(series) > 0 else 0
        return train_df, test_df, ratio


def prepare_series(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare a clean daily time series with Prophet-compatible columns ds and y."""
    required_cols = {DATETIME_COLUMN_NAME, TARGET_COLUMN_NAME}
    if df.empty or not required_cols.issubset(df.columns):
        return pd.DataFrame()
    
    series = df[[DATETIME_COLUMN_NAME, TARGET_COLUMN_NAME]].copy()
    series = series.rename(columns={DATETIME_COLUMN_NAME: "ds", TARGET_COLUMN_NAME: "y"})
    
    series["ds"] = pd.to_datetime(series["ds"], errors="coerce")
    series["y"] = pd.to_numeric(series["y"], errors="coerce")
    series.dropna(subset=["ds", "y"], inplace=True)
    series.sort_values("ds", inplace=True)
    series.drop_duplicates(subset="ds", keep="last", inplace=True)
    series.reset_index(drop=True, inplace=True)
    return series


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create time series features based on time series index."""
    df = df.copy()
    if isinstance(df.index, pd.DatetimeIndex):
        df['hour'] = df.index.hour
        df['dayofweek'] = df.index.dayofweek
        df['quarter'] = df.index.quarter
        df['month'] = df.index.month
        df['year'] = df.index.year
        df['dayofyear'] = df.index.dayofyear
        df['dayofmonth'] = df.index.day
        df['weekofyear'] = df.index.isocalendar().week
    elif 'ds' in df.columns:
        df['hour'] = df["ds"].dt.hour
        df['dayofweek'] = df["ds"].dt.dayofweek
        df['quarter'] = df["ds"].dt.quarter
        df['month'] = df["ds"].dt.month
        df['year'] = df["ds"].dt.year
        df['dayofyear'] = df["ds"].dt.dayofyear
        df['dayofmonth'] = df["ds"].dt.day
        df['weekofyear'] = df["ds"].dt.isocalendar().week
    return df