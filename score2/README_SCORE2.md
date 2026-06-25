# SCORE2 Risk Calculator (Python)

Reference implementation of the **SCORE2 algorithm** for estimating 10-year cardiovascular disease (CVD) risk in adults aged **40–69 years** without diabetes.

---

## Files included
- **score2_core.py** – main function `score2_risk(...)`
- **score2_coeff_bundle_v1.json** – model coefficients and region recalibration parameters

---

## Example usage

```python
from score2_core import score2_risk, load_coeff_bundle

# load coefficients
bundle = load_coeff_bundle("score2_coeff_bundle_v1.json")

# Example 1: male, smoker, age 50
risk_male = score2_risk(
    age=50,
    sex="male",
    smoker=True,
    sbp=140,
    tchol=5.5,
    hdl=1.3,
    bundle=bundle
)
print(f"Male example risk: {risk_male:.2f}%")

# Example 2: female, smoker, age 50
risk_female = score2_risk(
    age=50,
    sex="female",
    smoker=True,
    sbp=140,
    tchol=5.5,
    hdl=1.3,
    bundle=bundle
)
print(f"Female example risk: {risk_female:.2f}%")
```

### Output

```
Male example risk: 5.9%
Female example risk: 4.2%
```

---

## Inputs

- **age**: integer, years (valid 40–69)
- **sex**: "male" or "female"
- **smoker**: boolean (True/False)
- **sbp**: systolic blood pressure, mmHg
- **tchol**: total cholesterol, mmol/L
- **hdl**: HDL cholesterol, mmol/L
- **region**: one of "low", "moderate", "high", "very_high" (default is "low" for Switzerland risk region)
- **bundle**: loaded coefficient file (score2_coeff_bundle_v1.json)

---

## Output

A single float: the **10-year CVD risk (%)**.

---

## References

- SCORE2 working group and ESC Cardiovascular Risk Collaboration.  
  *SCORE2 risk prediction algorithms: new models to estimate 10-year risk of cardiovascular disease in Europe.*  
  **European Heart Journal** (2021) 42(25):2439–2454.  
  [doi:10.1093/eurheartj/ehab309](https://doi.org/10.1093/eurheartj/ehab309)
