from pathlib import Path

from data import get_CMS_data, get_CMS_cov, get_MC_signal



DATA_PATH = Path("/home/agv/Documents/Honours/Project/data/1803.08856/")

file_list = list(DATA_PATH.glob("*_??.csv"))
df = get_CMS_data(file_list)
print(df)

covariance = get_CMS_cov(DATA_PATH / "DPTTH_DMTT_cov.csv")

MC_PATH = Path("/home/agv/Documents/Honours/Project/data_generation/ttbar_2D")
file_list = list(MC_PATH.glob("run_*_LO/MADatNLO.HwU"))
df_list = get_MC_signal(file_list)
print(df_list)
print(len(df_list))

def generate_json(data: pd.DataFrame, MC_signal: List[pd.DataFrame], covariance: List[List[float]]):
    import json

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
