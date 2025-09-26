import json, math
from ..common.io import load_bundle as _load_pkg_bundle
from typing import Dict, Literal, Optional


def load_ckdpc_bundle(filename: str = "ckdpc_coeff_bundle_v1.json"):
    """Load the default CKD-PC bundle shipped with the package."""
    return _load_pkg_bundle("risk_calculators.ckdpc.bundles", filename)


DM_Med = Literal["oral", "insulin", "no_meds"]


def _build_context(
    diabetes: bool,
    age: float,
    female: bool,
    black: bool,
    eGFR: float,
    history_cvd: bool,
    ever_smoker: bool,
    hypertensive: bool,
    bmi: float,
    acr_mg_g: Optional[float] = None,  # ACR now optional
    hba1c: Optional[float] = None,
    dm_medication_status: Optional[DM_Med] = None,
    bundle: Dict = None,
) -> Dict[str, float]:
    """
    Build and return the model context (feature-engineered terms) for CKD-PC.

    Missing ACR handling:
      - Non-diabetic model uses: log10(ACR) - expected_log10ACR(...).
        If ACR is None or <= 0, set the albuminuria term = 0.
      - Diabetic model centers albuminuria at log10(10 mg/g) = 1.0.
        If ACR is None or <= 0, set the albuminuria term = 0.

    Units: eGFR mL/min/1.73m^2; ACR mg/g; HbA1c % (NGSP); BMI kg/m^2.
    """
    if bundle is None:
        raise ValueError("'bundle' is required (pass load_ckdpc_bundle()).")

    model_key = "diabetic" if diabetes else "nondiabetic"

    # Shared transforms / centered terms
    age_centered_per5 = (age / 5.0) - 11.0
    egfr_low_component = 15.0 - min(eGFR, 90.0) / 5.0
    egfr_high_component = max(0.0, eGFR - 90.0) / 5.0
    bmi_centered_per5 = (bmi / 5.0) - 5.4

    albuminuria_term = 0.0  # default when ACR is missing/invalid

    if not diabetes:
        expected_log10acr = (
            0.6754442
            + 0.0222581 * age_centered_per5
            + 0.0459020 * (1.0 if female else 0.0)
            - 0.0340495 * (1.0 if black else 0.0)
            + 0.0085871 * egfr_low_component
            - 0.0275825 * egfr_high_component
            + 0.0495695 * (1.0 if history_cvd else 0.0)
            + 0.0381086 * (1.0 if ever_smoker else 0.0)
            + 0.1286836 * (1.0 if hypertensive else 0.0)
            + 0.0218783 * bmi_centered_per5
        )
        if acr_mg_g is not None and acr_mg_g > 0:
            albuminuria_term = math.log10(acr_mg_g) - expected_log10acr
        else:
            albuminuria_term = 0.0
    else:
        # Diabetic model: centered at 10 mg/g (log10=1.0)
        if hba1c is None:
            raise ValueError("For the diabetes model, 'hba1c' is required (% NGSP).")
        if dm_medication_status is None:
            raise ValueError("For the diabetes model, provide 'dm_medication_status' (oral|insulin|no_meds).")
        if acr_mg_g is not None and acr_mg_g > 0:
            albuminuria_term = math.log10(acr_mg_g) - 1.0
        else:
            albuminuria_term = 0.0  # missing ACR -> 0 (treated as 10 mg/g)

    # Diabetes-only extra terms
    hba1c_centered = (float(hba1c) - 7.0) if (diabetes and hba1c is not None) else 0.0
    insulin_indicator = 1.0 if (diabetes and dm_medication_status == "insulin") else 0.0
    no_meds_indicator = 1.0 if (diabetes and dm_medication_status == "no_meds") else 0.0
    interaction_hba1c_insulin = hba1c_centered * insulin_indicator
    interaction_hba1c_no_meds = hba1c_centered * no_meds_indicator

    ctx: Dict[str, float] = {
        "age_centered_per5": age_centered_per5,
        "female": 1.0 if female else 0.0,
        "black": 1.0 if black else 0.0,
        "egfr_low_component": egfr_low_component,
        "egfr_high_component": egfr_high_component,
        "history_cvd": 1.0 if history_cvd else 0.0,
        "ever_smoker": 1.0 if ever_smoker else 0.0,
        "hypertensive": 1.0 if hypertensive else 0.0,
        "bmi_centered_per5": bmi_centered_per5,
        "albuminuria_term": albuminuria_term,
        # diabetes model extras (terms exist in bundle only for the diabetic model)
        "hba1c_centered": hba1c_centered,
        "insulin_indicator": insulin_indicator,
        "no_meds_indicator": no_meds_indicator,
        "interaction_hba1c_insulin": interaction_hba1c_insulin,
        "interaction_hba1c_no_meds": interaction_hba1c_no_meds,
    }

    return ctx


def ckdpc_risk_5y(
    diabetes: bool,
    age: float,
    sex: Literal["male", "female"],
    black: bool,
    egfr: float,
    history_cvd: bool,
    ever_smoker: bool,
    hypertensive: bool,
    bmi: float,
    acr_mg_g: Optional[float] = None,
    bundle: Dict = None,
    hba1c: Optional[float] = None,
    dm_medication_status: DM_Med = "oral",
) -> float:
    """
    CKD-PC 5-year absolute risk of incident eGFR <60 (all events).
    Returns % risk.
    """
    if bundle is None:
        raise ValueError("'bundle' is required (pass load_ckdpc_bundle()).")

    sub_id = "diabetic" if diabetes else "nondiabetic"
    try:
        model = bundle["models"][sub_id]
    except KeyError as e:
        raise KeyError(f"Bundle missing models['{sub_id}']") from e

    ctx = _build_context(
        diabetes=diabetes,
        age=age,
        female=(sex.lower() == "female"),
        black=black,
        eGFR=egfr,
        history_cvd=history_cvd,
        ever_smoker=ever_smoker,
        hypertensive=hypertensive,
        bmi=bmi,
        acr_mg_g=acr_mg_g,
        hba1c=hba1c,
        dm_medication_status=dm_medication_status,
        bundle=bundle,
    )

    # Linear predictor
    intercept = float(model["linear_predictor"]["intercept"])
    lp = intercept
    for term in model["linear_predictor"]["terms"]:
        name = term["name"]
        coef = float(term["coefficient"])
        if name not in ctx:
            raise KeyError(f"Context missing term '{name}'.")
        lp += coef * float(ctx[name])

    # Weibull/Fine–Gray absolute risk at 5 years
    gamma = float(model["risk_model"]["gamma"])
    risk = 1.0 - math.exp(- (5.0 ** gamma) * math.exp(lp))

    return float(max(0.0, min(1.0, risk)) * 100.0)
