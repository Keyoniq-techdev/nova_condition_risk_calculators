# PLCOM2012 Lung Cancer Risk Calculator (Python)

Reference implementation of the **PLCOm2012** prediction model for estimating **6-year risk of lung cancer incidence** among ever-smokers aged 55–74.  
This model was developed in the Prostate, Lung, Colorectal and Ovarian (PLCO) Cancer Screening Trial and validated in the National Lung Screening Trial (NLST).

---

## Package contents

This package provides:
- **plcom2012_core.py** – main function `plcom2012_risk_6y(...)`
- **plcom2012_coeff_bundle_v1.json** – model coefficients and parameters

---

## Quick start

```python
from plcom2012_core import load_plcom2012_bundle, plcom2012_risk_6y

# load coefficient bundle
bundle = load_plcom2012_bundle("plcom2012_coeff_bundle_v1.json")

# Example: Figure 1 profile (NEJM 2013)
risk = plcom2012_risk_6y(
    age_years=62,
    race="white",
    education_level=4,               # some college
    bmi=27.0,
    copd=False,
    personal_history_cancer=False,
    family_history_lung_cancer=False,
    smoking_status="former",
    smoking_intensity_cigs_per_day=20.0,
    smoking_duration_years=27.0,
    quit_time_years=10.0,
    bundle=bundle,
)

print(f"6-year lung cancer risk: {risk['risk_6y']:.2f}%")
```

### Example Output

```
6-year lung cancer risk: 0.89%
```

---

## Inputs

- **age_years**: integer, 55–74 years (model developed for this age range)  
- **sex**: encoded within coefficients by sex categories (handled via `bundle`)  
- **race**: `"white"`, `"black"`, `"hispanic"`, `"asian"`, or `"other"`  
- **education_level**: ordinal 1–6 (less than 7 years schooling → graduate education)  
- **bmi**: float, kg/m²  
- **copd**: boolean (True/False) – history of COPD, emphysema, or chronic bronchitis  
- **personal_history_cancer**: boolean (True/False) – prior cancer (excl. non-melanoma skin cancer)  
- **family_history_lung_cancer**: boolean (True/False)  
- **smoking_status**: `"current"` or `"former"`  
- **smoking_intensity_cigs_per_day**: average number of cigarettes/day while smoking  
- **smoking_duration_years**: total years smoked  
- **quit_time_years**: years since quitting (0 if current smoker)  
- **bundle**: loaded coefficient file (`plcom2012_coeff_bundle_v1.json`)

---

## Output

Dictionary containing:
- **linear_predictor**: raw logistic score  
- **prob_6y**: predicted 6-year probability (0–1)  
- **risk_6y**: 6-year absolute risk in % (0–100)

---

## References

- Tammemägi MC, Katki HA, Hocking WG, et al.  
  *Selection Criteria for Lung-Cancer Screening.*  
  N Engl J Med. 2013;368(8):728–736.  
  doi:10.1056/NEJMoa1211776
