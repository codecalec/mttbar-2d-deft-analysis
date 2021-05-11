import sys
import getopt
from pathlib import Path
from typing import List

from data import get_CMS_data, get_CMS_cov, get_MC_signal
from config import generate_json

import pandas as pd


def create_config_files():
    DATA_PATH = Path("/home/agv/Documents/Honours/Project/data/1803.08856/")

    file_list = list(DATA_PATH.glob("*_??.csv"))
    df = get_CMS_data(file_list)

    covariance = get_CMS_cov(DATA_PATH / "DPTTH_DMTT_cov.csv")

    MC_PATH = Path("/home/agv/Documents/Honours/Project/data_generation/ttbar_2D")
    file_list = list(MC_PATH.glob("run_*_LO/MADatNLO.HwU"))
    df_list = get_MC_signal(file_list)

    generate_json(df, df_list, covariance, "ttbar_2D.json")


def run_analysis():
    pass


try:
    opts, args = getopt.getopt(sys.argv[1:], "c", ["--config"])
    for opt, args in opts:
        if opt in ("-c", "config"):
            create_config_files()
            print("Generated config files")

    if len(opts) == 0:
        run_analysis()

except getopt.GetoptError as err:
    print(err)
    sys.exit(2)
