import json
import importlib.resources as res
from typing import Dict

def load_bundle(package_subpath: str, filename: str) -> Dict:
    """
    Load a JSON bundle that lives inside the package.
    Example:
        load_bundle("risk_calculators.ckdpc.bundles", "ckdpc_coeff_bundle_v1.json")
    """
    with res.files(package_subpath).joinpath(filename).open("r", encoding="utf-8") as f:
        return json.load(f)
