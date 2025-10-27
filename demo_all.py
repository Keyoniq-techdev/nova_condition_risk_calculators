# examples/demo_all.py

from risk_calculators import (
    # CKD-PC
    load_ckdpc_bundle, ckdpc_risk_5y,
    # GDRS
    load_gdrs_bundle, gdrs,
    # SCORE2
    load_score2_bundle, score2_risk,
    # CAIDE
    load_caide_bundle, caide,
    # CLivD Modellab
    load_clivd_bundle, clivd_modellab_score,
    # PLCOM2012
    load_plcom2012_bundle, plcom2012_risk_6y,
    # COPD
    load_copd_bundle, copd_casefinding_score,
)


def run_demo():
    print("=== Demo: CKD-PC ===")
    ckdpc_bundle = load_ckdpc_bundle()
    r_ckdpc = ckdpc_risk_5y(
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
        bundle=ckdpc_bundle,
    )
    print(f"CKD-PC 5y risk: {r_ckdpc:.2f}%\n")

    print("=== Demo: GDRS ===")
    gdrs_bundle = load_gdrs_bundle()
    r_gdrs = gdrs(
        age=52,
        height=1.72,
        waist=98,
        hypertension=True,
        exercise=1.5,               # h/week
        smoking="former_lt20",
        wholegrains=25,             # g/day
        coffee=225,                 # g/day (~mL)
        redmeat=75,                 # g/day
        diabetes_one_parent=True,
        diabetes_both_parents=False,
        diabetes_sibling=False,
        hba1c=5.7,
        bundle=gdrs_bundle,
    )
    print(f"GDRS 5y diabetes risk: {r_gdrs:.2f}%\n")

    print("=== Demo: SCORE2 ===")
    score2_bundle = load_score2_bundle()
    r_score2 = score2_risk(
        age=50,
        sex="male",
        smoker=True,
        sbp=140,
        tchol=5.5,
        hdl=1.3,
        bundle=score2_bundle,
    )
    print(f"SCORE2 10y CVD risk: {r_score2:.2f}%\n")

    print("=== Demo: CAIDE ===")
    caide_bundle = load_caide_bundle()
    r_caide = caide(
        age=50,
        sex="female",
        education_years=8,
        sbp_mmHg=150,
        bmi=27,
        total_chol_mmol_L=7.0,
        physically_active=False,
        apoe_status="non_e4",
        bundle=caide_bundle,
    )
    print(f"CAIDE dementia risk (basic model): {r_caide:.2f}%\n")

    print("=== Demo: CLivD Modellab ===")
    clivd_bundle = load_clivd_bundle()

    ex = clivd_modellab_score(
        age=52,
        sex="male",
        whr=1.10,
        alcohol=14.0,
        ggt=65.0,
        diabetes=True,
        smoking="current",
        bundle=clivd_bundle,
    )

    print(f"CLivD Modellab — LP: {ex['linear_predictor']:.3f}, HR: {ex['hazard_ratio']:.3f}, "
          f"Risk group(15y): {ex['risk_group_15y']}")
    
    print("\n=== Demo: PLCOM2012 ===")
    plco_bundle = load_plcom2012_bundle()
    plco_res = plcom2012_risk_6y(
        age_years=62,
        race="white",
        education_level=4,
        bmi=27.0,
        copd=False,
        personal_history_cancer=False,
        family_history_lung_cancer=False,
        smoking_status="former",
        smoking_intensity_cigs_per_day=20,
        smoking_duration_years=27,
        quit_time_years=10,
        bundle=plco_bundle,
    )

    print(
        f"PLCOM2012 — 6y risk: {plco_res['risk_6y']:.2f}% "
        f"(prob={plco_res['prob_6y']:.4f}, LP={plco_res['linear_predictor']:.3f})"
    )

    print("\n=== Demo: COPD Case-Finding ===")
    copd_bundle = load_copd_bundle()
    copd=copd_casefinding_score(
        smoking_status="former",
        asthma_history=True,
        lrti_count_3y="1",
        salbutamol_3y=True,
        bundle=copd_bundle,
    )

    print(copd)

if __name__ == "__main__":
    run_demo()
