# plcom2012_core.py

import math
from typing import Dict, Literal, Optional
from ..common.io import load_bundle as _load_pkg_bundle

Race = Literal[
    "white",
    "black",
    "hispanic",
    "asian",
    "american_indian_alaska_native",
    "native_hawaiian_pacific_islander",
]
SmokingStatus = Literal["former", "current"]

def load_plcom2012_bundle(filename: str = "plcom2012_coeff_bundle_v1.json") -> Dict:
    """
    Load the PLCOM2012 coefficient bundle shipped with the package.
    """
    # adjust the package path to wherever you keep bundles in your project
    return _load_pkg_bundle("risk_calculators.plcom2012.bundles", filename)


def _build_plco_context(
    age_years: float,
    race: Race,
    education_level: int,             # 1..6 ordinal (see bundle notes)
    bmi: float,                        # kg/m^2
    copd: bool,
    personal_history_cancer: bool,
    family_history_lung_cancer: bool,
    smoking_status: SmokingStatus,     # 'former' | 'current'
    smoking_intensity_cigs_per_day: float,
    smoking_duration_years: float,
    quit_time_years: Optional[float],  # years since quit; set 0 for current smokers
    bundle: Dict,
) -> Dict[str, float]:
    """
    Build all engineered features exactly as expected by the JSON bundle.
    """
    if bundle is None:
        raise ValueError("'bundle' is required (pass load_plcom2012_bundle()).")

    model = bundle["model"]
    helpers = bundle.get("shared_transform_helpers", {})
    centers = helpers.get("centering", {})
    age_c = float(centers.get("age_years_center", 62.0))
    edu_c = float(centers.get("education_level_center", 4.0))
    bmi_c = float(centers.get("bmi_center", 27.0))
    dur_c = float(centers.get("smoking_duration_years_center", 27.0))
    quit_c = float(centers.get("quit_time_years_center", 10.0))

    # Per model convention: current smokers have quit time = 0
    qt = 0.0 if smoking_status == "current" else float(quit_time_years or 0.0)

    # Nonlinear intensity transform
    intensity_meta = helpers.get("smoking_intensity_transform", {})
    # Logistic model uses the inverse-power transform centered at 0.4021541613
    center_const = float(intensity_meta.get("steps", [None, None, None])[-1].split()[-1]) \
        if intensity_meta.get("steps") else 0.4021541613
    x = float(smoking_intensity_cigs_per_day) / 10.0
    # guard against zero cigs/day for an ever-smoker
    x = max(x, 1e-6)
    intensity_term = (x ** -1.0) - center_const

    # Indicators / centered terms
    ctx: Dict[str, float] = {
        "age_centered": float(age_years) - age_c,
        "education_centered": float(education_level) - edu_c,
        "bmi_centered": float(bmi) - bmi_c,
        "copd_yes": 1.0 if copd else 0.0,
        "personal_cancer_yes": 1.0 if personal_history_cancer else 0.0,
        "family_lung_cancer_yes": 1.0 if family_history_lung_cancer else 0.0,
        "smoking_current": 1.0 if smoking_status == "current" else 0.0,
        "smoking_intensity_term": intensity_term,
        "smoking_duration_centered": float(smoking_duration_years) - dur_c,
        "quit_time_centered": float(qt) - quit_c,
        # race one-hot (white is reference)
        "race_black": 1.0 if race == "black" else 0.0,
        "race_hispanic": 1.0 if race == "hispanic" else 0.0,
        "race_asian": 1.0 if race == "asian" else 0.0,
        "race_ai_an": 1.0 if race == "american_indian_alaska_native" else 0.0,
        "race_nh_pi": 1.0 if race == "native_hawaiian_pacific_islander" else 0.0,
    }
    return ctx


def plcom2012_risk_6y(
    age_years: float,
    race: Race,
    education_level: int,
    bmi: float,
    copd: bool,
    personal_history_cancer: bool,
    family_history_lung_cancer: bool,
    smoking_status: SmokingStatus,
    smoking_intensity_cigs_per_day: float,
    smoking_duration_years: float,
    quit_time_years: Optional[float],
    bundle: Dict = None,
) -> Dict[str, float]:
    """
    PLCOM2012 6-year absolute risk of lung cancer (ever-smokers).
    Returns:
      {
        'risk_6y': float,            # probability in percent [0, 100]
        'prob_6y': float,            # probability in [0, 1]
        'linear_predictor': float    # logistic LP
      }
    """
    if bundle is None:
        raise ValueError("'bundle' is required (pass load_plcom2012_bundle()).")

    model = bundle["model"]
    ctx = _build_plco_context(
        age_years=age_years,
        race=race,
        education_level=education_level,
        bmi=bmi,
        copd=copd,
        personal_history_cancer=personal_history_cancer,
        family_history_lung_cancer=family_history_lung_cancer,
        smoking_status=smoking_status,
        smoking_intensity_cigs_per_day=smoking_intensity_cigs_per_day,
        smoking_duration_years=smoking_duration_years,
        quit_time_years=quit_time_years,
        bundle=bundle,
    )

    # Linear predictor from bundle
    intercept = float(model["linear_predictor"]["intercept"])
    lp = intercept
    for term in model["linear_predictor"]["terms"]:
        name = term["name"]
        coef = float(term["coefficient"])
        if name not in ctx:
            raise KeyError(f"Context missing term '{name}'.")
        lp += coef * float(ctx[name])

    # Logistic probability
    prob = 1.0 / (1.0 + math.exp(-lp))
    prob = max(0.0, min(1.0, prob))
    return {
        "risk_6y": prob * 100.0,
        "prob_6y": prob,
        "linear_predictor": lp,
    }
