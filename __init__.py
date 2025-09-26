"""
risk_calculators package

Unified access to multiple validated clinical risk calculators:
- CKD-PC (incident CKD)
- GDRS (diabetes)
- SCORE2 (cardiovascular disease)
- CAIDE (dementia)
- CLivD Modellab (liver disease)
- PLCOM2012 (lung cancer)

Each model has:
- a JSON bundle of coefficients/parameters
- a `load_*_bundle()` function to read the JSON
- a main risk function returning % risk
"""

# CKD-PC (kidney disease)
from .ckdpc.ckdpc_core import ckdpc_risk_5y, load_ckdpc_bundle

# GDRS (diabetes)
from .gdrs.gdrs_core import gdrs, load_gdrs_bundle

# SCORE2 (CVD)
from .score2.score2_core import score2_risk, load_score2_bundle

# CAIDE (dementia)
from .caide.caide_core import caide, load_caide_bundle

# CLivD (liver disease)
from .clivd.clivd_core import clivd_modellab_score, load_clivd_bundle

# PLCOM2012 (lung cancer)
from .plcom2012.plcom2012_core import load_plcom2012_bundle, plcom2012_risk_6y

# COPD (lung disease)
from .copd.copd_core import copd_casefinding_score, load_copd_bundle


__all__ = [
    # CKD-PC
    "ckdpc_risk_5y", "load_ckdpc_bundle",
    # GDRS
    "gdrs", "load_gdrs_bundle",
    # SCORE2
    "score2_risk", "load_score2_bundle",
    # CAIDE
    "caide", "load_caide_bundle",
    # CLivD
    "clivd_modellab_score", "load_clivd_bundle",
    # PLCOM2012
    "load_plcom2012_bundle", "plcom2012_risk_6y",
    # COPD
    "copd_casefinding_score", "load_copd_bundle",
]
