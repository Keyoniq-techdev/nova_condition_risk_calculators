import json, math
from typing import Dict, Literal
from ..common.io import load_bundle as _load_pkg_bundle

def load_gdrs_bundle(filename: str = "gdrs_coeff_bundle_v1.json"):
    return _load_pkg_bundle("risk_calculators.gdrs.bundles", filename)

SmokingCat = Literal["never", "former_lt20", "former_ge20", "current_lt20", "current_ge20"]

def gdrs(
    age: int,
    height: float,                  # m
    waist: float,                   # cm
    hypertension: bool,
    exercise: float,                # h/week
    smoking: SmokingCat,            # "never"|"former_lt20"|"former_ge20"|"current_lt20"|"current_ge20"
    wholegrains: float,             # g/day
    coffee: float,                  # g (~mL)/day
    redmeat: float,                 # g/day
    diabetes_one_parent: bool,
    diabetes_both_parents: bool,
    diabetes_sibling: bool,
    hba1c: float,
    bundle: Dict
) -> float:
    """
    Returns 5-year *clinical* GDRS risk (%) using parameters read from the JSON bundle.
    """

    def var(name: str) -> Dict:
        for v in bundle["original_points_model"]["variables"]:
            if v["name"] == name:
                return v
        raise KeyError(name)

    def points_per_unit(name: str) -> float:
        return float(var(name)["points_per_unit"])

    def per(name: str) -> float:
        return float(var(name).get("scaling", {}).get("per", 1.0))

    def bin_points(name: str) -> float:
        return float(var(name)["points_if_true"])

    def smoking_points(code: str) -> float:
        cats = {c["code"]: float(c["points"]) for c in var("smoking")["categories"]}
        if code not in cats:
            raise ValueError(f"Unknown smoking category {code!r}. Allowed: {list(cats)}")
        return cats[code]

    # weights
    w_age      = points_per_unit("age")
    w_height   = points_per_unit("height")
    w_waist    = points_per_unit("waist")
    p_hyp      = bin_points("hypertension")
    w_exercise = points_per_unit("exercise")

    w_wg, per_wg     = points_per_unit("wholegrains"), per("wholegrains")
    w_coffee, per_coffee = points_per_unit("coffee"), per("coffee")
    w_redmeat, per_redmeat = points_per_unit("redmeat"), per("redmeat")

    p_one_parent   = bin_points("diabetes_one_parent")
    p_both_parents = bin_points("diabetes_both_parents")
    p_sibling      = bin_points("diabetes_sibling")

    # clinical extension coeffs
    coeffs = bundle["clinical_extension"]["clinical_points"]["coefficients"]
    op_mult = float(coeffs["original_points"])
    hba1c_mult = float(coeffs["hba1c"])
    intercept = float(bundle["clinical_extension"]["clinical_points"].get("intercept", 0.0))

    # risk params
    rm_orig = bundle["original_points_model"]["risk_model"]
    s0_orig = float(rm_orig["baseline_survival"])
    mean_orig = float(rm_orig["mean_points"])
    scale_orig = 100.0 if rm_orig.get("scale_per_100_points", True) else 1.0

    rm_clin = bundle["clinical_extension"]["risk_model"]
    s0_clin = float(rm_clin["baseline_survival"])
    mean_clin = float(rm_clin["mean_points"])
    scale_clin = 100.0 if rm_clin.get("scale_per_100_points", True) else 1.0

    # family history precedence
    parent_points = (
        p_both_parents if diabetes_both_parents else 0.0
    ) + (p_one_parent if diabetes_one_parent and not diabetes_both_parents else 0.0)

    # original points
    original_points = (
        w_age * age +
        w_height * (height*100) + # model needs height in cm
        w_waist * waist +
        (p_hyp if hypertension else 0.0) +
        w_exercise * exercise +
        smoking_points(smoking) +
        w_wg * (wholegrains / per_wg) +
        w_coffee * (coffee / per_coffee) +
        w_redmeat * (redmeat / per_redmeat) +
        parent_points +
        (p_sibling if diabetes_sibling else 0.0)
    )

    # risks
    p_original = 1.0 - (s0_orig ** (math.exp((original_points - mean_orig) / scale_orig)))
    clinical_points = op_mult * original_points + hba1c_mult * hba1c + intercept
    p_clinical = 1.0 - (s0_clin ** (math.exp((clinical_points - mean_clin) / scale_clin)))

    return float(p_clinical * 100.0)
