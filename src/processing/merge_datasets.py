# Loading the data
msoa_income_path = '../../data/processed/msoa_income_net_income_after_housing_costs.csv'
msoa_income_data = pd.read_csv(msoa_income_path)

# Extract the prefix from 'names' in the LSOA data
merged_data['msoa_prefix'] = merged_data['names'].str.extract(r'(^.* \d+)')

# Merge based on the prefix
merged_data_with_income = pd.merge(
    merged_data, 
    msoa_income_data, 
    left_on='msoa_prefix', 
    right_on='msoa_name', 
    how='left'
)

# Extracting unmatched rows from the MSOA income data
unmatched_msoa = msoa_income_data[~msoa_income_data['msoa_name'].isin(merged_data['msoa_prefix'].unique())]

# Saving the results
merged_data_path = '../../data/processed/lsoa_census_merged_with_income.csv'
unmatched_msoa_path = '../../data/processed/unmatched_msoa.csv'

# Saving the merged data
merged_data_with_income.to_csv(merged_data_path, index=False)

# Saving the unmatched MSOA data
unmatched_msoa.to_csv(unmatched_msoa_path, index=False)

# Displaying the outputs to check
print("Merged Data Preview:")
print(merged_data_with_income.head())

print("\nUnmatched MSOA Data Preview:")
print(unmatched_msoa.head())

# Reloading the updated dataset
updated_data_path = '../../data/processed/lsoa_census_merged_with_income.csv'
merged_data_with_income = pd.read_csv(updated_data_path)

print("Updated dataset loaded successfully.")

# Checking for missing values
missing_values = merged_data_with_income.isnull().sum()

# Displaying columns with missing values
print("Columns with missing values:")
print(missing_values[missing_values > 0])

from sklearn.impute import KNNImputer

# Creating a KNN imputer instance
imputer = KNNImputer(n_neighbors=5)  # You can adjust the number of neighbors if needed

# Applying KNN Imputation (excluding non-numeric columns)
numeric_columns = merged_data_with_income.select_dtypes(include=['float64', 'int64']).columns
merged_data_with_income[numeric_columns] = imputer.fit_transform(merged_data_with_income[numeric_columns])

# Displaying completion message
print("KNN imputation completed.")


# Generating the descriptive statistics for numeric columns
summary_stats = merged_data_with_income.describe()

print("Quick Statistical Summary:")
print(summary_stats)