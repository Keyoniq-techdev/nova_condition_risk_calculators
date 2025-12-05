# CLivD Liver Disease Risk Calculator (Python)

Reference implementation of the **CLivD Modellab** risk score for estimating **15-year risk of incident advanced chronic liver disease (CLD)** in the general adult population.  
This version implements the **laboratory-based model (Modellab)** from Åberg *et al.*, *J Hepatol* 2022, which uses **age, sex, waist–hip ratio, alcohol intake, diabetes, smoking, and gamma-glutamyl transferase (GGT)**.

---

## Package contents

This package provides:
- **clivd_core.py** – main function `clivd_modellab_score(...)`
- **clivd_coeff_bundle_v1.json** – model coefficients, truncation limits, and spline definitions

---

## Quick start

```python
from clivd_core import load_clivd_bundle, clivd_modellab_score

# load coefficient bundle
bundle = load_clivd_bundle("clivd_coeff_bundle_v1.json")

# Example: 52-year-old man, diabetes, current smoker, 14 drinks/week,
# waist–hip ratio 1.10, GGT 65 U/L
result = clivd_modellab_score(
    age=52,
    sex="male",
    whr=1.10,
    alcohol=14.0,
    ggt=65.0,
    diabetes=True,
    smoking="current",
    bundle=bundle,
)

print(result)
```

### Example Output

```
{
  'linear_predictor': 2.43,
  'hazard_ratio': 11.39,
  'risk_group_15y': 'intermediate'
}
```

---

## Inputs

- **age**: float, years  
- **sex**: `"male"` or `"female"`  
- **whr**: float, waist–hip ratio (unitless)  
- **alcohol**: float, drinks per week (1 drink = 10 g ethanol, truncated at 50)  
- **ggt**: float, U/L (truncated at 200)  
- **diabetes**: boolean (True/False) – diabetes at baseline  
- **smoking**: `"current"` or `"never_or_past"`  
- **bundle**: loaded coefficient file (`clivd_coeff_bundle_v1.json`)

---

## Output

A dictionary containing:  
- **linear_predictor** – Cox model log-hazard score (LP)  
- **hazard_ratio** – relative risk = exp(LP)  
- **risk_group_15y** – categorical risk group based on LP cut points:  
  - `"minimal"` (<0.5% risk)  
  - `"low"` (0.5–4%)  
  - `"intermediate"` (5–9%)  
  - `"high"` (≥10%)  

---

## Notes

- This implementation computes **relative risks and risk-group assignment** only.  
- The authors did not publish baseline survival functions, so **absolute 15-year risk (%)** cannot be directly reproduced.  
- Risk-group cutoffs are taken from the supplementary material.  

---

## References

- Åberg F, Luukkonen PK, But A, et al.  
  *Development and validation of a model to predict incident chronic liver disease in the general population: The CLivD score.*  
  J Hepatol. 2022;77(1):111–120.  
  doi: 10.1016/j.jhep.2022.02.021   
