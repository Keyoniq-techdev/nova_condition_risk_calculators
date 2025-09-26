# Chronic Disease Risk Calculators – Summary

| Model        | Function (Prediction Target) | Inputs | Output | Model Type | DOI |
|--------------|------------------------------|--------|--------|------------|-----|
| **SCORE2** | 10-year first-onset CVD (non-fatal MI, non-fatal stroke, CVD death) | Age, sex, smoking, systolic BP, total cholesterol, HDL cholesterol, ESC region | 10-year absolute risk (%) | Competing-risk–adjusted model (Fine–Gray) | [10.1093/eurheartj/ehab309](https://doi.org/10.1093/eurheartj/ehab309) |
| **GDRS (clinical, 2018)** | 5-year incident type 2 diabetes | Age, height, waist circumference, hypertension, physical activity, smoking (5 levels), wholegrains, coffee, red meat, parental/sibling diabetes, HbA1c | 5-year absolute risk (%) | Cox proportional hazards | [10.1136/bmjdrc-2018-000524](https://doi.org/10.1136/bmjdrc-2018-000524) |
| **CAIDE** | 20-year incident dementia (midlife adults) | Age, sex, education, systolic BP, BMI, total cholesterol, physical activity, ± APOE ε4 | 20-year absolute risk (%) | Points-based score with logistic mapping | [10.1016/S1474-4422(06)70537-3](https://doi.org/10.1016/S1474-4422(06)70537-3) |
| **CKD-PC (2019)** | 5-year incident CKD (eGFR <60; baseline eGFR >60) | Age, sex, Black race indicator, baseline eGFR, CVD history, ever-smoker, hypertension, BMI; in diabetes: HbA1c & diabetes meds; albuminuria optional (ACR-missing supported) | 5-year absolute risk (%) | Multicohort competing-risk framework (subdistribution hazards) | [10.1001/jama.2019.17379](https://doi.org/10.1001/jama.2019.17379) |
| **CLivD (lab version)** | 15-year incident advanced chronic liver disease (general population) | Age, sex, waist–hip ratio, alcohol/week, GGT, diabetes, smoking | Risk category (minimal/low/intermediate/high) and relative risk (hazard ratio) | Cox proportional hazards (baseline survival not published) | [10.1016/j.jhep.2022.02.016](https://doi.org/10.1016/j.jhep.2022.02.016) |
| **PLCOm2012** | 6-year incident lung cancer (ever-smokers) | Age, race/ethnicity, education, BMI, COPD history, personal & family cancer history, smoking status, intensity, duration, years since quit | 6-year absolute risk (%) | Logistic regression | [10.1056/NEJMoa1211776](https://doi.org/10.1056/NEJMoa1211776) |
| **COPD case-finding (Haroon 2014)** | Undiagnosed (current) COPD in primary care (screening/case-finding) | Smoking status, asthma history, lower respiratory tract infections (3y), salbutamol prescriptions (3y) | Likelihood score / threshold → spirometry recommendation | Logistic regression (externally validated) | [10.1136/bmjresp-2013-000001](https://doi.org/10.1136/bmjresp-2013-000001) |

---

**Notes:**  
- Keep each model's native horizon; avoid re-horizoning fixed-horizon logistic models.  
- CLivD provides categories/relative risk (no published baseline survival).  
- Risks reflect external cohorts; local calibration may adjust absolute levels.
