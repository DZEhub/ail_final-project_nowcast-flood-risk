# -*- coding=utf-8 -*-
# Import necessary system and path manipulation modules
import sys
from pathlib import Path
import os
import time
from datetime import datetime, date

print("__file__:", str(Path(__file__)))
print("level 0:", str(Path(__file__).resolve()))
print("level 1:", str(Path(__file__).resolve().parent))
print("level 2:", str(Path(__file__).resolve().parent.parent))
print("level 3:", str(Path(__file__).resolve().parent.parent.parent))
print("level 4:", str(Path(__file__).resolve().parent.parent.parent.parent))
print("level 5:", str(Path(__file__).resolve().parent.parent.parent.parent.parent))

# Add parent directory to path to allow importing config modules
# This ensures that we can import from the 'config' and 'models' directories correctly
# sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Import utilities for fetching data from the API, cleaning the time series, and splitting the data
from config.data_utils import fetch_obs_elab, prepare_series, split_train_test, SITES
# Import utilities for argument parsing, MLflow configuration, and plotting
from config.model_utils import parse_args, setup_mlflow, plot_all_models_comparison

# Get current directory of this script file
PROJECT_DIR = Path(__file__).resolve().parent
print("cwd:", PROJECT_DIR)