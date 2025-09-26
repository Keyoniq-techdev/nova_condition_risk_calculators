# CKD-PC Kidney Disease Risk Calculator (Python)

Reference implementation of the **CKD Prognosis Consortium (CKD-PC)** prediction equations for estimating **5-year risk of incident chronic kidney disease (CKD)**, defined as **eGFR <60 mL/min/1.73m²**, in adults with baseline eGFR >60.  
This version uses the **“all events” models** from the 2019 JAMA publication and its supplement.

---

## Package contents

This package provides:
- **ckdpc_core.py** – main function `ckdpc_risk_5y(...)`
- **ckdpc_coeff_bundle_v1.json** – model coefficients and parameters (nondiabetic & diabetic)

---

## Quick start

```python
from ckdpc_core import load_ckdpc_bundle, ckdpc_risk_5y

# load coefficient bundle
bundle = load_ckdpc_bundle("ckdpc_coeff_bundle_v1.json")

# Example: 60-year-old man, Black, hypertensive, eGFR 85, ACR 15 mg/g
risk = ckdpc_risk_5y(
    diabetes=False,
    sex="male",
    age=60,
    black=True,
    egfr=85,
    history_cvd=True,
    ever_smoker=True,
    hypertensive=True,
    bmi=30,
    acr_mg_g=15.0,
    bundle=bundle
)

print(f"5-year CKD risk: {risk:.2f}%")
```

### Example Output

```
5-year CKD risk: 18.72%
```

---

## Inputs

- **diabetes**: boolean (True/False) – diabetes status at baseline  
- **sex**: `"male"` or `"female"`  
- **age**: integer, years  
- **black**: boolean (True/False) – Black race indicator  
- **egfr**: float, mL/min/1.73m² (must be >60 at baseline)  
- **history_cvd**: boolean (True/False) – prior cardiovascular disease  
- **ever_smoker**: boolean (True/False) – smoking history  
- **hypertensive**: boolean (True/False) – hypertension  
- **bmi**: float, kg/m²  
- **acr_mg_g**: float or None, urine albumin-to-creatinine ratio, mg/g (optional: may be omitted if not available; handled internally per CKD-PC design)
- **hba1c**: float, % (only required if `diabetes=True`)  
- **dm_medication_status**: `"oral"`, `"insulin"`, or `"no_meds"` (only for diabetic model)  
- **bundle**: loaded coefficient file (`ckdpc_coeff_bundle_v1.json`)

---

## Output

A single float: the **5-year absolute risk (%)** of incident CKD (eGFR <60). Values are bounded between 0 and 100.  

---

## References

- CKD Prognosis Consortium.  
  *Development and Validation of Risk Prediction Models for Incident Chronic Kidney Disease.*  
  JAMA. 2019;322(21):2104–2114.  
  doi:10.1001/jama.2019.17379  

- Online calculator: [CKD-PC Risk Tool](http://ckdpcrisk.org/ckdrisk)
