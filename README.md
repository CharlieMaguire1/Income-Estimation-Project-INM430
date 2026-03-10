# London Income Estimation

**Status:** Early notebook-based modelling project | Core workflow complete

Estimate **Greater London small-area income patterns** by combining LSOA-level socioeconomic indicators with official MSOA income estimates and applying **kNN regression**.


---


## What this project does

This project builds an end-to-end workflow to:

- Clean a complex multi-sheet Excel data
- Engineer socioeconomic, housing, education, crime, and demographic features
- Merge the **LSOA predictors** with the **MSOA income estimates**
- Test multiple feature configurations
- Train and evaluate the **kNN regression** models
- Generate the predicted income values for London LSOAs


---


## Main data sources

- **GLA LSOA Atlas** for the predictor features
- **ONS Small Area Income Estimates** for the target variable
- A separate London crime source was reviewed, but it was not central to the final workflow


---


## Target variable

The chosen target was:

**Net income after housing costs**

This was selected because it reflects disposable household resources effectively after the major household costs.


---


## Workflow summary

1. Clean and simplify the multi-sheet LSOA Excel data  
2. Consolidate the multi-row headers into usable feature names  
3. Keep relevant 2011/12 variables  
4. Filter the MSOA income data to London
5. Merge the LSOA predictors with the MSOA income estimates  
6. Reconcile unmatched geographic units manually  
7. Apply the KNN imputation and standardisation  
8. Test the multiple feature configurations  
9. Train and evaluate the kNN regression  
10. Export the predicted LSOA income values  


---


## Modelling

Primary model:
- **kNN Regressor**

Feature selection and compression methods were explored by the following:
- Correlation analysis
- Random Forest feature importance
- Manual feature reduction
- PCA-based grouped feature compression


---


## Model configurations tested

### Model 1
All the numeric variables except the target.

### Model 2
40+ of the low-importance variables were removed.

### Model 3
Confidence interval variables were removed.

### Model 4
PCA-compressed feature groups.


---


## Best result

**Best-performing setup:** Model 1

### Final metrics
- **MAE:** 0.2483
- **RMSE:** 0.3297
- **R²:** 0.8933

### Other model results
- **Model 2:** R² = 0.7476
- **Model 3:** R² = 0.7430
- **Model 4:** R² = 0.7172


---


## Most important predictors

Across the feature-engineering experiments, the strongest predictors included:

- `employment_rate_2011`
- `no_qualifcations_count_2011`
- `children_poverty-percent_2011`
- `highest_qualification_lvl_4_above_count_2011`
- `lone_parent_household_percent_2011`


---


## Outputs

The project saves:

- trained kNN model
- fitted scaler
- evaluation outputs
- `lsoa_income_predictions.csv`


---


## Key limitation

The best-performing setup retained published confidence interval fields associated with the MSOA income estimates. These improved predictive performance, so results should be interpreted with that in mind.

Additional configurations excluding those fields were tested to assess stricter predictor sets.


---


## Repo structure

```text
london-income-estimation/
├── notebooks/
│   ├── eda/
│   ├── modelling/
│   ├── evaluation/
│   └── experiments/
├── merged_notebook.ipynb
├── merged_notebook.html
├── requirements.txt
└── README.md
```


---


## Technology used

- Python
- pandas
- NumPy
- scikit-learn
- SciPy
- matplotlib
- seaborn
- joblib


---


## Skills demonstrated:

- Data cleaning from messy MS Excel sources
- Small-area data integration
- Geographic key matching
- kNN imputation
- Feature scaling
- Feature engineering
- PCA
- Feature importance analysis
- kNN regression
- Model evaluation


---


## Future improvements

- Refactor the notebook workflow into a cleaner modular structure
- Validate the predicted LSOA values against stronger external benchmarks
- Convert the standardised predictions back to their original income units
- Map the predicted LSOA income spatially
- Compare against the stronger tabular baselines


---


## Author

Charlie Maguire
