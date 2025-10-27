import json, math
from typing import Dict
from ..common.io import load_bundle as _load_pkg_bundle

def load_score2_bundle(filename: str = "score2_coeff_bundle_v1.json"):
    return _load_pkg_bundle("risk_calculators.score2.bundles", filename)

def score2_risk(
    age: int,
    sex: str,              # "male" | "female"
    smoker: bool,
    sbp: float,            # mmHg
    tchol: float,          # mmol/L
    hdl: float,            # mmol/L
    bundle: Dict,
    region="low"          # based on country of residence
) -> float:
    """
    Returns 10-year CVD risk in percent, using the merged SCORE2 coeff bundle.
    - Pulls betas + region_params from bundle["by_region"][region][sex].
    """
    if not 40 <= age <= 69:
        raise ValueError(f"SCORE2 is only validated for ages 40–69 (got {age})")

    sex = sex.lower()
    region = region.lower()
    try:
        entry = bundle["by_region"][region][sex]
    except KeyError as e:
        raise ValueError(f"Unknown region/sex: region={region!r}, sex={sex!r}") from e

    beta = entry["betas"]                # beta coefficients
    a, b = entry["region_params"]        # regional recalibration params

    # scaling
    cage   = (age - 60) / 5
    csbp   = (sbp - 120) / 20
    ctchol = (tchol - 6) / 1
    chdl   = (hdl  - 1.3) / 0.5
    smoke  = 1 if smoker else 0
    diab   = 0   # SCORE2 (non-diabetes population)

    # linear predictor
    LP = (
        beta["cage"]*cage +
        beta["smoke"]*smoke +
        beta["csbp"]*csbp +
        beta["ctchol"]*ctchol +
        beta["chdl"]*chdl +
        beta["cage*smoke"]*(cage*smoke) +
        beta["cage*csbp"]*(cage*csbp) +
        beta["cage*ctchol"]*(cage*ctchol) +
        beta["cage*chdl"]*(cage*chdl) +
        beta["diab"]*diab +                 # 0 for SCORE2
        beta["cage*diab"]*(cage*diab)      # 0 for SCORE2
    )

    # sex-specific baseline survival
    if sex == "male":
        S0_10y = 0.9605
    elif sex == "female":
        S0_10y = 0.9776
    else:
        raise ValueError("sex must be 'male' or 'female'")

    # base risk and regional recalibration
    p_base = 1.0 - (S0_10y ** (math.exp(LP)))
    p_base = min(max(p_base, 1e-15), 1 - 1e-15) # avoid log(0) issues

    x = math.log(-math.log(1.0 - p_base))
    x_adj = a + b * x
    p_reg = 1.0 - math.exp(-math.exp(x_adj))

    return float(p_reg * 100.0)

