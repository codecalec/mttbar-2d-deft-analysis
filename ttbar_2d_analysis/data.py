from typing import List
from pathlib import Path

import numpy as np
import pandas as pd

from deft_hep.helper import convert_hwu_to_numpy

# K-factor from LO to NNLO at 13TeV
LO_XSEC = 4.574e2  # 4.584 +- 0.003 from https://arxiv.org/abs/1405.0301
NNLO_XSEC = (
    831.76  # from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
)
k_factor = NNLO_XSEC / LO_XSEC


def get_CMS_data(path_list: List[Path]) -> pd.DataFrame:

    pt_bounds = [(0, 90), (90, 180), (180, 270), (270, 800)]

    df_total = pd.DataFrame()
    for f, (lower, upper) in zip(path_list, pt_bounds):
        df = pd.read_csv(
            f,
            comment="#",
            header=0,
            names=[
                "m_mid",
                "m_min",
                "m_max",
                "m_value",
                "stat_up",
                "stat_down",
                "sys_up",
                "sys_down",
            ],
            usecols=[0, 1, 2, 3],
        )
        df["pt_min"] = lower
        df["pt_max"] = upper
        df_total = df_total.append(df, ignore_index=True)

    return df_total


def get_CMS_cov(path: Path, num_of_bins: int = 32):
    covar = [[0 for _ in range(num_of_bins)] for _ in range(num_of_bins)]

    with open(path) as f:
        next(f)
        for _ in range(10):
            next(f)

        while line := f.readline():
            x, y, val = iter(line.strip().split(","))
            covar[int(float(x)) - 1][int(float(y)) - 1] = float(val)
    return covar


def get_MC_signal(
    file_list: List[Path], num_of_bins: int = 32
) -> List[pd.DataFrame]:

    hist_list = [convert_hwu_to_numpy(f, num_of_bins) for f in file_list]

    pt_bounds = [0, 90, 180, 270, 800]
    pt_left = [pt_bounds[i//8] for i in range(num_of_bins)]
    pt_right = [pt_bounds[i//8+1] for i in range(num_of_bins)]

    edges, _ = hist_list[0]
    edge_left = [edges[i] for i in range(len(edges) - 1)]
    edge_right = [edges[i + 1] for i in range(len(edges) - 1)]

    df_list = []
    for _, values in hist_list:
        bin_widths = np.fromiter(
            (edge_left[i] - edge_right[i] for i in range(len(edges) - 1)),
            float,
            len(edges) - 1,
        )
        scaled_values = values / bin_widths * k_factor

        df = pd.DataFrame(
            {
                "m_min": edge_left,
                "m_max": edge_right,
                "m_value": scaled_values.tolist(),
                "pt_min": pt_left,
                "pt_max": pt_right,
            }
        )
        df_list.append(df)

    return df_list
