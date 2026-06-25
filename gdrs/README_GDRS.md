# GDRS Diabetes Risk Calculator (Python)

Reference implementation of the **German Diabetes Risk Score (GDRS)** algorithm for estimating **5-year type 2 diabetes risk** in adults without diabetes at baseline.  
This version uses the **2018 clinical extension** (EPIC-Potsdam derivation), which incorporates **HbA1c** alongside the original lifestyle-based score.

---

## Files included
- **gdrs_core.py** – main function `gdrs(...)`
- **gdrs_coeff_bundle_v1.json** – model coefficients and parameters

---

## Example usage

```python
from gdrs_core import gdrs, load_gdrs_bundle

# load coefficient bundle
bundle = load_gdrs_bundle("gdrs_coeff_bundle_v1.json")

# Example: 52-year-old man, former smoker (<20/day), hypertensive, HbA1c 5.7%
risk = gdrs(
    age=52,
    height=1.72,
    waist=98,
    hypertension=True,
    exercise=1.5,               # hours/week
    smoking="former_lt20",
    wholegrains=25,             # g/day
    coffee=225,                 # g/day (~mL/day)
    redmeat=75,                # g/day
    diabetes_one_parent=True,
    diabetes_both_parents=False,
    diabetes_sibling=False,
    hba1c=5.7,
    bundle=bundle
)

print(f"5-year diabetes risk: {risk:.2f}%")
```

### Example Output

```
5-year diabetes risk: 6.21%
```

---

## Inputs

- **age**: integer, years  
- **height**: m   
- **waist**: cm  
- **hypertension**: boolean (True/False)  
- **exercise**: physical activity, hours/week  
- **smoking**: one of  
  - `"never"`  
  - `"former_lt20"` (former smoker <20/day)  
  - `"former_ge20"` (former smoker ≥20/day)  
  - `"current_lt20"` (current smoker <20/day)  
  - `"current_ge20"` (current smoker ≥20/day)  
- **wholegrains**: g/day  
- **coffee**: g/day (~mL/day)  
- **redmeat**: g/day  
- **diabetes_one_parent**: boolean (True/False)  
- **diabetes_both_parents**: boolean (True/False)  
- **diabetes_sibling**: boolean (True/False)  
- **hba1c**: % (NGSP/DCCT standard)  
- **bundle**: loaded coefficient file (`gdrs_coeff_bundle_v1.json`)

---

## Output

A single float: the **5-year diabetes risk (%)**.

---

## References

- Mühlenbruch K, Paprott R, Joost H-G, Boeing H, Heidemann C, Schulze MB, et al.
  *Derivation and external validation of a clinical version of the German Diabetes Risk Score (GDRS) including measures of HbA1c.*
  BMJ Open Diabetes Research & Care. 2018;6(1):e000524.  
  doi:10.1136/bmjdrc-2018-000524
