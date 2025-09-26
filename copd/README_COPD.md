# COPD Case-Finding Score (Python)

Reference implementation of the **Haroon et al. 2014 CPRD algorithm** for estimating the likelihood of **undiagnosed COPD** in adults aged **≥35 years**.

---

## Files included
- **copd_core.py** – main function `copd_casefinding_score(...)`
- **copd_coeff_bundle_v1.json** – model coefficients and variable definitions

---

## Example usage

```python
from copd_core import copd_casefinding_score, load_copd_bundle

# load coefficients
bundle = load_copd_bundle("haroon_copd_casefinding_v1.json")

# Example: former smoker, asthma history, >1 LRTI in last 3y, salbutamol use
result = copd_casefinding_score(
    smoking_status="former",
    asthma_history=True,
    lrti_count_3y=">1",
    salbutamol_3y=True,
    bundle=bundle
)

print(result)
```
### Output

```
COPD case-finding score: 5.17, Score ≥ 2.5: likely undiagnosed COPD — recommend confirmatory spirometry.
```

---

## Inputs

- **smoking_status**: "never", "former", "current", "missing"
- **asthma_history**: boolean (True/False)
- **lrti_count_3y**: "0", "1", or ">1" (number of lower respiratory tract infections in last 3 years, excluding the previous 60 days)
- **salbutamol_3y**: boolean (True/False; any prescription in last 3 years, excluding final 60 days)
- **bundle**: loaded model coefficient file (haroon_copd_casefinding_v1.json)

---

## Output

- **score**: float, linear predictor (β-sum)
- **text**: short interpretation string

---

## References

- Haroon S, et al.  
  *Case finding for COPD in primary care: external validation of a simple tool.*  
  **BMJ Open Respiratory Research** 2014;1:e000001.  
  [doi:10.1136/bmjresp-2013-000001](https://doi.org/10.1136/bmjresp-2013-000001)
