import json, math
from typing import Dict, Literal, Optional
from ..common.io import load_bundle as _load_pkg_bundle

def load_caide_bundle(filename: str = "caide_coeff_bundle_v1.json"):
    return _load_pkg_bundle("risk_calculators.caide.bundles", filename)

Sex = Literal["female", "male"]
APOE = Literal["non_e4", "e4"]

def caide(
    age: int,
    sex: Sex,                        # "female" | "male"
    education_years: int,            # years of formal education
    sbp_mmHg: float,                 # systolic BP (mmHg)
    bmi: float,                      # kg/m^2
    total_chol_mmol_L: float,        # mmol/L
    physically_active: bool,         # True if ≥2x/week, else False
    apoe_status: Optional[APOE] = None,            # "non_e4" | "e4" (required if model="apoe")
    model: Literal["basic", "apoe"] = "basic",
    bundle: Dict = None
) -> float:
    """
    Returns 20-year CAIDE dementia risk (%) using the points + logistic-on-points model
    
    """

    model_key = "model_1_basic" if model == "basic" else "model_2_apoe"
    if model_key not in bundle:
        raise KeyError(f"Model {model!r} not found in bundle.")
    m = bundle[model_key]

    def var(name: str) -> Dict:
        for v in m["variables"]:
            if v["name"] == name:
                return v
        raise KeyError(name)

    def categorical_points(name: str, code: str) -> float:
        v = var(name)
        cats = {c["code"]: float(c.get("points", 0.0)) for c in v["categories"]}
        if code not in cats:
            raise ValueError(f"Unknown category {code!r} for {name}. Allowed: {list(cats)}")
        return cats[code]

    def binary_points(name: str, is_true: bool) -> float:
        if not is_true:
            return 0.0
        v = var(name)
        return float(v.get("points_if_true", 0.0))

    # categorical mapping
    # age
    def age_points(a: int) -> float:
        v = var("age")
        chosen = None
        for c in v["categories"]:
            code = c["code"]
            pts = float(c.get("points", 0.0))
            if code.startswith("<"):
                cutoff = int(code[1:])
                if a < cutoff:
                    chosen = pts
            elif code.startswith(">"):
                cutoff = int(code[1:])
                if a > cutoff:
                    chosen = pts
            else:
                rng = code.replace("–", "-")
                lo, hi = [int(x) for x in rng.split("-")]
                if lo <= a <= hi:
                    chosen = pts
        return chosen

    # education_years
    def edu_points(years: int) -> float:
        v = var("education_years")
        chosen = None
        for c in v["categories"]:
            lab = (c.get("label") or c.get("code")).replace("–", "-")
            pts = float(c.get("points", 0.0))
            if lab.startswith("≥"):
                cutoff = int(lab[1:])
                if years >= cutoff:
                    chosen = pts
            elif lab.startswith("≤"):
                cutoff = int(lab[1:])
                if years <= cutoff:
                    chosen = pts
            elif "-" in lab:
                lo, hi = [int(x) for x in lab.split("-")]
                if lo <= years <= hi:
                    chosen = pts
        return chosen

    # compute points
    points = 0.0
    points += age_points(age)
    points += edu_points(education_years)
    points += categorical_points("sex", sex)

    points += binary_points("sbp_over_140", sbp_mmHg > float(var("sbp_over_140")["threshold"]["sbp_mmHg"]))
    points += binary_points("bmi_over_30",  bmi > float(var("bmi_over_30")["threshold"]["bmi"]))
    points += binary_points(
        "total_chol_over_6_5",
        total_chol_mmol_L > float(var("total_chol_over_6_5")["threshold"]["chol_mmol_per_L"])
    )
    points += binary_points("physically_inactive", not physically_active)

    if model == "apoe":
        if apoe_status is None:
            raise ValueError("apoe_status must be provided when model='apoe' (use 'non_e4' or 'e4').")
        points += categorical_points("apoe_status", apoe_status)

    # logistic-on-points
    lop = m["logistic_on_points"]
    beta0 = float(lop["beta0"])
    beta2 = float(lop["beta2_per_point"])
    beta1 = float(lop.get("beta1_followup20y", 0.0))  # 20-year follow-up

    logit = beta0 + beta1 + beta2 * points
    p = 1.0 / (1.0 + math.exp(-logit))
    return float(p * 100.0)
