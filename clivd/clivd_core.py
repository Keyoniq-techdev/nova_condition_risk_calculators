import json, math
from typing import Dict, Literal
from ..common.io import load_bundle as _load_pkg_bundle

Sex = Literal["male", "female"]
Smoking = Literal["current", "never_or_past"]

def load_clivd_bundle(filename: str = "clivd_coeff_bundle_v1.json"):
    """Load the CLivD Modellab coefficient bundle shipped with the package."""
    return _load_pkg_bundle("risk_calculators.clivd.bundles", filename)


def _build_clivd_context(
    age: float,
    sex: Sex,
    whr: float,
    alcohol: float,  # drinks/week
    ggt: float,      # U/L
    diabetes: bool,
    smoking: Smoking,
    bundle: Dict,
) -> Dict[str, float]:
    """
    Build the model context (feature-engineered terms) for CLivD Modellab.
    Applies truncation and spline transforms per supplement.
    """
    if bundle is None:
        raise ValueError("'bundle' is required (pass load_clivd_bundle()).")

    # Apply truncation rules
    alc = max(0.0, min(float(alcohol), bundle["shared_transform_helpers"]["variable_truncation"]["alcohol_drinks_per_week"]["truncate_max"]))
    ggt_val = max(0.0, min(float(ggt), bundle["shared_transform_helpers"]["variable_truncation"]["ggt_ul"]["truncate_max"]))

    female = 1.0 if sex == "female" else 0.0
    diabetes_yes = 1.0 if diabetes else 0.0
    smoking_current = 1.0 if smoking == "current" else 0.0

    # Alcohol spline basis
    s1 = max(alc - 0.1, 0.0) ** 3
    s2 = max(alc - 1.0, 0.0) ** 3
    s3 = max(alc - 3.0, 0.0) ** 3
    s4 = max(alc - 9.0, 0.0) ** 3
    s5 = max(alc - 33.0, 0.0) ** 3

    return {
        "age": age,
        "waist_hip_ratio_x10": whr * 10.0,
        "alcohol_linear": alc,
        "alcohol_spline_s1": s1,
        "alcohol_spline_s2": s2,
        "alcohol_spline_s3": s3,
        "alcohol_spline_s4": s4,
        "alcohol_spline_s5": s5,
        "ggt": ggt_val,
        "female_indicator": female,
        "diabetes_yes": diabetes_yes,
        "smoking_current": smoking_current,
        "interaction_female_x_ggt": ggt_val * female,
        "interaction_female_x_smoking": female * smoking_current,
    }


def clivd_modellab_score(
    age: float,
    sex: Sex,
    whr: float,
    alcohol: float,
    ggt: float,
    diabetes: bool,
    smoking: Smoking,
    bundle: Dict = None,
) -> Dict[str, object]:
    """
    CLivD Modellab 15-year risk score.

    Returns:
      {
        'linear_predictor': float,
        'hazard_ratio': float,
        'risk_group_15y': str
      }
    """
    if bundle is None:
        raise ValueError("'bundle' is required (pass load_clivd_bundle()).")

    model = bundle["model"]

    ctx = _build_clivd_context(
        age=age, sex=sex, whr=whr, alcohol=alcohol,
        ggt=ggt, diabetes=diabetes, smoking=smoking,
        bundle=bundle
    )

    # Linear predictor
    intercept = float(model["linear_predictor"]["intercept"])
    lp = intercept
    for term in model["linear_predictor"]["terms"]:
        coef = float(term["coefficient"])
        name = term["name"]
        if name not in ctx:
            raise KeyError(f"Context missing term '{name}'.")
        lp += coef * float(ctx[name])

    # Hazard ratio (relative risk)
    hr = math.exp(lp)

    # Risk-group classification from supplement cut points
    if lp < -0.258:
        group = "minimal"
    elif lp <= 2.066:
        group = "low"
    elif lp <= 2.784:
        group = "intermediate"
    else:
        group = "high"

    return {
        "linear_predictor": lp,
        "hazard_ratio": hr,
        "risk_group_15y": group
    }