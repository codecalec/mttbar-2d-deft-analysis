from pathlib import Path
from typing import List

import pandas as pd


def generate_json(
    data: pd.DataFrame,
    MC_signal: List[pd.DataFrame],
    covariance: List[List[float]],
    filename: Path,
):
    import json

    ctg_list = [-2.0, 0.0001, 2.0, -1.0, 1.0]

    output_dict = {
        "config": {
            "run_name": "CMS-TOP-ctg",
            "data": {"observable": "$m_{t\\bar{t}}$"},
            "model": {
                "input": "numpy",
                "inclusive_k_factor": 1,
                "c_i_benchmark": 2,
                "max_coeff_power": 1,
                "cross_terms": False,
            },
            "fit": {"n_burnin": 500, "n_total": 3000, "n_walkers": 32},
        }
    }

    test_output_dict = {
        "config": {
            "run_name": "CMS-TOP-ctg",
            "data": {"observable": "$m_{t\\bar{t}}$"},
            "model": {
                "input": "numpy",
                "inclusive_k_factor": 1,
                "c_i_benchmark": 2,
                "max_coeff_power": 1,
                "cross_terms": False,
            },
            "fit": {"n_burnin": 500, "n_total": 3000, "n_walkers": 32},
        }
    }

    MC_signal_model = MC_signal[:3]
    MC_signal_test = MC_signal[3:]
    ctg_list_model = ctg_list[:3]
    ctg_list_test = ctg_list[3:]

    # Data Section
    output_dict["config"]["data"]["bins"] = data["m_min"].tolist()
    output_dict["config"]["data"]["central_values"] = data["value"].tolist()
    test_output_dict["config"]["data"]["bins"] = data["m_min"].tolist()
    test_output_dict["config"]["data"]["central_values"] = data["value"].tolist()

    output_dict["config"]["data"]["covariance_matrix"] = covariance
    test_output_dict["config"]["data"]["covariance_matrix"] = covariance

    # Model Section
    samples = [[1, ctg] for ctg in ctg_list_model]
    samples_test = [[1, ctg] for ctg in ctg_list_test]

    output_dict["config"]["model"]["samples"] = samples
    test_output_dict["config"]["model"]["samples"] = samples_test

    predictions = [df["value"].tolist() for df in MC_signal_model]
    predictions_test = [df["value"].tolist() for df in MC_signal_test]

    output_dict["config"]["model"]["predictions"] = predictions
    test_output_dict["config"]["model"]["predictions"] = predictions_test

    output_dict["config"]["model"]["prior_limits"] = {"c_{tG}": [-2.0, 2.0]}
    test_output_dict["config"]["model"]["prior_limits"] = {"c_{tG}": [-2.0, 2.0]}

    with open(filename, "w") as f:
        json.dump(output_dict, f, indent=4)

    with open(f"test_{filename}", "w") as test_f:
        json.dump(test_output_dict, test_f, indent=4)
