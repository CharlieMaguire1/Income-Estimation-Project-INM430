import pandas as pd

# Loading the Excel file for LSOA atlas data, which I will name "lsoa_census_data" from now on.
file_path = "../../data/raw/lsoa_census.xlsx"

# Retrieving and displaying the sheet names
sheets = pd.ExcelFile(file_path).sheet_names
print("The sheet names/tables for MSOA Income Estimate data:", sheets)

# Loading sheets as DataFrames
relevant_sheets = sheets[0:5]
lsoa_census_data = {sheet: pd.read_excel(file_path, sheet_name = sheet) 
                    for sheet in relevant_sheets}

# Exploring each DataFrame by looping through each sheet
for sheet, census in lsoa_census_data.items():
    print(f"Sheet: {sheet}")
    print(census.head())
    print(census.info())

# Defining a function that can clean each sheet 
def clean_sheet(lsoa_data, sheet_name):
    if sheet_name == 'iadatasheet1':
        # Dropping the columns by range
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[2:86], errors='ignore')  # Columns 3 to 86
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[116:125], errors='ignore')  # Columns 117 to 125
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[136:210], errors='ignore')  # Columns 137 to 210

    elif sheet_name == 'iadatasheet2':
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[2:44], errors='ignore')  # Columns 3 to 44
        lsoa_data = lsoa_data.drop(columns=[102], errors='ignore')  # Column 103
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[107:124], errors='ignore')  # Columns 108 to 124
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[125:131], errors='ignore')  # Columns 126 to 131

    elif sheet_name == 'iadatasheet3':
        # Removing the entire sheet
        return None

    elif sheet_name == 'iadatasheet4':
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[2:72], errors='ignore')  # Columns 3 to 72
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[142:168], errors='ignore')  # Columns 143 to 168
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[170:186], errors='ignore')  # Columns 171 to 186
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[227:251], errors='ignore')  # Columns 228 to 251, keep total for children

    elif sheet_name == 'iadatasheet5':
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[27:32], errors='ignore')  # Columns 28 to 32
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[33:51], errors='ignore')  # Columns 34 to 51
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[63:103], errors='ignore')  # Columns 64 to 103
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[103:136], errors='ignore')  # Columns 104 to 136
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[145:181], errors='ignore')  # Columns 146 to 181
        lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[191:203], errors='ignore')  # Columns 192 to 203

    elif sheet_name == 'iadatasheet6':
        # Removing the entire sheet
        return None

    # Removing the first column
    lsoa_data = lsoa_data.drop(columns=lsoa_data.columns[0], errors='ignore')
    
    return lsoa_data

# Iterating over sheets and cleaning them
lsoa_cleaned_sheets = {}
for sheet_name, lsoa_data in lsoa_census_data.items():
    lsoa_cleaned_data = clean_sheet(lsoa_data, sheet_name)
    if lsoa_cleaned_data is not None:
        lsoa_cleaned_sheets[sheet_name] = lsoa_cleaned_data

# Saving the cleaned sheets to a new Excel file
output_path = '../../data/processed/lsoa_data_cleaned.xlsx'
with pd.ExcelWriter(output_path) as writer:
    for sheet_name, lsoa_data in lsoa_cleaned_sheets.items():
        lsoa_data.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"The cleaned sheets have been saved to {output_path} successfully")

# Reading the cleaned Excel file and display the first three rows of each sheet
output_path = '../../data/processed/lsoa_data_cleaned.xlsx'

# Loading the cleaned sheets into a dictionary
cleaned_lsoa_data = pd.read_excel(output_path, sheet_name=None)

# Displaying the first three rows for each sheet
for sheet_name, lsoa_data in cleaned_lsoa_data.items():
    print(f"The first three rows of sheet: {sheet_name}")
    print(lsoa_data.head(3))
    print("\n" + "-" * 50 + "\n")

# Updating relevant sheets because some of them have been deleted
relevant_sheets = ['iadatasheet1', 'iadatasheet2', 'iadatasheet4', 'iadatasheet5']

# Merging the DataFrame sheets in lsoa_census_data dictionary
merged_data = cleaned_lsoa_data[relevant_sheets[0]]

for sheet in relevant_sheets[1:]:
    merged_data = merged_data.merge(
        cleaned_lsoa_data[sheet],
        how= 'left',
        on= 'lsoa_code',
        suffixes=('', f'_{sheet}')  # Handling the duplicate column names
    )


# Resolving the duplicate column names 
# Keeping the first occurrence of a column with duplicates
merged_data = merged_data.loc[:, ~merged_data.columns.duplicated()]

# Validate the merge
print(merged_data.info())

# Calculating the annual averages
merged_data['rate_of_people_income_support_2011_avg'] = merged_data[['rate_of_people_income_support_2011', 
                                                           'rate_of_people_income_support_2011.1', 
                                                           'rate_of_people_income_support_2011.2', 
                                                           'rate_of_people_income_support_2011.3']].mean(axis=1)

merged_data['rate_of_people_income_support_2012_avg'] = merged_data[['rate_of_people_income_support_2012', 
                                                           'rate_of_people_income_support_2012.1', 
                                                           'rate_of_people_income_support_2012.2', 
                                                           'rate_of_people_income_support_2012.3']].mean(axis=1)

# Aggregating into a single variable
merged_data['rate_of_people_income_support_2011_12'] = merged_data[['rate_of_people_income_support_2011_avg', 
                                                          'rate_of_people_income_support_2012_avg']].mean(axis=1)

# Dropping the original quarterly columns and placeholder columns
columns_to_drop = ['names_iadatasheet2', 'names_iadatasheet4', 'names_iadatasheet5', 
                   'rate_of_people_income_support_2011.1', 'rate_of_people_income_support_2011.2', 
                   'rate_of_people_income_support_2011.3', 'rate_of_people_income_support_2011.1', 
                   'rate_of_people_income_support_2011.2', 'rate_of_people_income_support_2011.3']
merged_data.drop(columns=columns_to_drop, inplace=True)

# Before I begin KNN Imputing, I need to change some column names to lowercase and correct some mistakes
merged_data.rename(columns={'avg_lvl_3_QCDA_per_student_2011_12': 'avg_lvl_3_qcda_per_student_2011_12'}, inplace=True)
merged_data.rename(columns={'lone_parent_household_percent_2011_iadatasheet2': 'lone_parent_household_percent_2011'}, inplace=True)

from sklearn.impute import KNNImputer
import pandas as pd

# 1. Converting the non-numeric values in numeric columns to NaN
numeric_columns = ['avg_point_ks2_percent_2011', 'avg_point_ks2_percent_2012', 'avg_capped_gcse_points_per_pupil_2011_12', 'avg_lvl_3_qcda_per_student_2011_12']
for col in numeric_columns:
    merged_data[col] = pd.to_numeric(merged_data[col], errors='coerce')

# 2. Handling missing values with KNN imputation
# Select the numeric columns (exclude columns like the target variable if needed)
numeric_columns_for_imputation = merged_data.select_dtypes(include=['float64']).columns

# Initialising KNNImputer (you can adjust n_neighbors based on your data)
knn_imputer = KNNImputer(n_neighbors = 5)

# Applying KNN imputation to the numeric columns
merged_data[numeric_columns_for_imputation] = knn_imputer.fit_transform(merged_data[numeric_columns_for_imputation])

# 3. Converting object columns like 'child_out_of_work_benefit_percent_2011' to numeric (if applicable)
merged_data['child_out_of_work_benefit_percent_2011'] = pd.to_numeric(merged_data['child_out_of_work_benefit_percent_2011'], errors='coerce')

# Checking to see if there are any columns left as objects
object_columns = merged_data.select_dtypes(include=['object']).columns
print(f"Object columns remaining: {object_columns}")

# Checking to see if there are any missing values after imputation
missing_values_after_imputation = merged_data.isnull().sum()
print(f"Missing values after KNN imputation: \n{missing_values_after_imputation}")

# Displaying the last 5 five rows
print(merged_data.tail())

# Removing the last three rows
merged_data = merged_data.iloc[:-3]

# Checking to see if it changed or not
print(merged_data.tail())

# Checking for missing values in each column
missing_values_per_column = merged_data.isnull().sum()

# Sending it to a csv file
missing_values_per_column.to_csv("../../data/raw/missing_values.csv")

# Creating a copy of merged_data 
merged_data = merged_data.copy()

# 1. Handling the missing values in 'child_out_of_work_benefit_percent_2011' (float column)
# Convert non-numeric values in this column to NaN
merged_data.loc[:, 'child_out_of_work_benefit_percent_2011'] = pd.to_numeric(merged_data['child_out_of_work_benefit_percent_2011'], errors='coerce')

# Applying KNN imputation to the column
knn_imputer = KNNImputer(n_neighbors = 5)
merged_data.loc[:, ['child_out_of_work_benefit_percent_2011']] = knn_imputer.fit_transform(merged_data[['child_out_of_work_benefit_percent_2011']])

# 2. Handling missing values in 'persistent_absentees__percent_2011_12' (object column)
# First, removing any '%' characters and convert to numeric
merged_data.loc[:, 'persistent_absentees__percent_2011_12'] = merged_data['persistent_absentees__percent_2011_12'].replace('%', '', regex=True)
merged_data.loc[:, 'persistent_absentees__percent_2011_12'] = pd.to_numeric(merged_data['persistent_absentees__percent_2011_12'], errors='coerce')

# Applying KNN imputation to the column
merged_data.loc[:, ['persistent_absentees__percent_2011_12']] = knn_imputer.fit_transform(merged_data[['persistent_absentees__percent_2011_12']])

# 3. Checking for missing values after imputation
# Checking missing values only for the specified columns
columns_of_interest = ['child_out_of_work_benefit_percent_2011', 'persistent_absentees__percent_2011_12']
missing_values_for_selected_columns = merged_data[columns_of_interest].isnull().sum()

print(f"Missing values for selected columns: \n{missing_values_for_selected_columns}")

# Converting 'child_tax_credit_lone_parent_percent_2011' and 'child_out_of_work_benefit_percent_2012' to float
merged_data['child_tax_credit_lone_parent_percent_2011'] = pd.to_numeric(merged_data['child_tax_credit_lone_parent_percent_2011'], errors='coerce')
merged_data['child_out_of_work_benefit_percent_2012'] = pd.to_numeric(merged_data['child_out_of_work_benefit_percent_2012'], errors='coerce')

print(merged_data.info())

# Saving the lsoa_census (merged_data) to the processed folder
lsoa_census_path = '../../data/processed/lsoa_census.csv'
merged_data.to_csv(lsoa_census_path, index=False)