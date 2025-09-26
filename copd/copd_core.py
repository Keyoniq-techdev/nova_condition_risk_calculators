import json
from typing import Dict

from ..common.io import load_bundle as _load_pkg_bundle

def load_copd_bundle(filename: str = "copd_coeff_bundle_v1.json"):
    return _load_pkg_bundle("risk_calculators.copd.bundles", filename)

def copd_casefinding_score(
    smoking_status: str,
    asthma_history: bool,
    lrti_count_3y: str,
    salbutamol_3y: bool,
    bundle: Dict,
    threshold: float = 2.5
):
    """
    Returns linear score for Haroon COPD case-finding model, plus threshold flag.
    """
    smoking_status = smoking_status.lower()
    lrti_count_3y = str(lrti_count_3y)

    coeffs = bundle["score_model"]["coefficients"]

    score = (
        coeffs["smoking_status"][smoking_status]
        + (coeffs["asthma_history"] if asthma_history else 0.0)
        + coeffs["lrti_count_3y"][lrti_count_3y]
        + (coeffs["salbutamol_3y"] if salbutamol_3y else 0.0)
    )


    flag = score >= threshold

    result = {
        "score": float(score),
        "above_threshold": flag,
    }

    if flag:
        result["text"] = (
            f"Score ≥ {threshold}: likely undiagnosed COPD — "
            "recommend confirmatory spirometry."
        )
    else:
        result["text"] = (
            f"Score < {threshold}: below recommended cut-off for case-finding."
        )

    return f"COPD case-finding score: {result['score']:.2f}, {result['text']}"
