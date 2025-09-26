# CAIDE Dementia Risk Calculator (Python)

Reference implementation of the **CAIDE 20-year dementia risk score** for middle-aged adults, with **Model 1 (basic)** and **Model 2 (adds APOE ε4)** variants.

---

## Files included
- **caide_core.py** – main function `caide(...)`
- **caide_coeff_bundle_v1.json** – model coefficients, point mappings, and parameters for Model 1 & Model 2

---

## Example usage

```python
from caide_core import caide, load_caide_bundle

# load coefficient bundle
bundle = load_caide_bundle("caide_coeff_bundle_v1.json")

# Example: 50-year-old woman, 8 years education, SBP 150, BMI 27,
# cholesterol 7.0 mmol/L, inactive, non-ε4 (intermediate-risk profile)
risk_basic = caide(
    age=50,
    sex="female",
    education_years=8,
    sbp_mmHg=150,
    bmi=27,
    total_chol_mmol_L=7.0,
    physically_active=False,
    model="basic",
    bundle=bundle
)

risk_apoe = caide(
    age=50,
    sex="female",
    education_years=8,
    sbp_mmHg=150,
    bmi=27,
    total_chol_mmol_L=7.0,
    physically_active=False,
    apoe_status="non_e4",
    model="apoe",
    bundle=bundle
)

print(f"20-year dementia risk (Model 1): {risk_basic:.2f}%")
print(f"20-year dementia risk (Model 2): {risk_apoe:.2f}%")
```

### Example Output

```
20-year dementia risk (Model 1): 6.91%
20-year dementia risk (Model 2): 4.06%
```

---

## Inputs

- **age**: int, years  
- **sex**: `"female"` | `"male"`  
- **education_years**: int, years of formal education  
- **sbp_mmHg**: float, systolic blood pressure (mmHg)  
- **bmi**: float, kg/m²  
- **total_chol_mmol_L**: float, mmol/L  
- **physically_active**: bool (True if ≥2×/week; else False)  
- **apoe_status** *(Model 2 only)*: `"non_e4"` | `"e4"`  
- **model**: `"basic"` or `"apoe"`  
- **bundle**: result of `load_caide_bundle("caide_coeff_bundle_v1.json")`

---

## Output

A single float: the **20-year dementia risk (%)**.

---

## Notes

- This implementation uses the **points-based score** with the paper’s **logistic-on-points** coefficients:  
  - Model 1: β₀ = −7.406, β₁(20y) = 0.796, β₂(per point) = 0.401  
  - Model 2: β₀ = −8.083, β₁(20y) = 1.020, β₂(per point) = 0.390   
- For production, consider input validation aligned to the study population (e.g., midlife ages 39–64) even though the categorical bins technically cover all numeric ages.

---

## Reference

Kivipelto M, Ngandu T, Laatikainen T, Winblad B, Soininen H, Tuomilehto J.  
**Risk score for the prediction of dementia risk in 20 years among middle aged people: a longitudinal, population-based study.** *Lancet Neurol.* 2006;5:735–741. doi:10.1016/S1474-4422(06)70537-3.