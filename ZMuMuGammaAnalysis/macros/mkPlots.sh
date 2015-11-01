python ./zmmgBins.py --doScan ~/www/higgs/legacy/zmmg/zmumugamma_svar_v11/fit_full_syst_dpg_breakdown/ebee_highlow/scan_deltaEg_data_EB_high_low_r9.json --scanVar '#deltaE^{#gamma}_{HighR_{9}} - #deltaE^{#gamma}_{LowR_{9}}' --scanSign -1. -O ~/www/higgs/legacy/zmmg/zmumugamma_svar_v11/fit_full_syst_dpg_breakdown/ebee_highlow

python ./zmmgBins.py --doScan ~/www/higgs/legacy/zmmg/zmumugamma_svar_v11/fit_full_syst_dpg_breakdown/scan_deltaEg_global.json --scanVar '#deltaE^{#gamma}' -O ~/www/higgs/legacy/zmmg/zmumugamma_svar_v11/fit_full_syst_dpg_breakdown/

python ./zmmgBins.py --load ../../AnalysisScripts/zmmgFitSignles.json -O ~/www/higgs/legacy/zmmg/zmumugamma_svar_v11/fit_full_syst_dpg_breakdown/ --saveas png,pdf --legpos 0.15,0.15,0.6,0.45

## python -i ./zmmgBins.py --doScan ~/www/higgs/legacy/zmmg/zmumugamma_svar_v11/fit_full_syst_dpg_breakdown/results.txt --load 
