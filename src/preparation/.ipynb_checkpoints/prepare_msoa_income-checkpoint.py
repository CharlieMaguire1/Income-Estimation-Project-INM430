import pandas as pd

# Defining the path for the raw and processed MSOA Income Estimate data
file_path = "../../data/raw/msoa_income.xlsx"
processed_path = "../../data/processed/" 

# Retrieving and displaying the sheet names
sheets = pd.ExcelFile(file_path).sheet_names
print("The sheet names/tables for MSOA Income Estimate data:", sheets)

# Defining the relevant sheets now the names are known
relevant_sheets = ["Total weekly income", "Net weekly income", 
"Net income before housing costs", "Net income after housing costs"]

# Storing processed data by initialising a dictionary
adjust_data = {}

# Processing each relevant sheet
for sheet in relevant_sheets:
    print(f"Processing sheet: {sheet}")

    # Loading the relevant sheets and skipping the first three rows
    msoa_income_data = pd.read_excel(file_path, sheet_name = sheet, header = 4)

    # Removing the last row as it is irrelevant (i.e. not a numerical value or a category)
    msoa_income_data = msoa_income_data[:-1]

    # Standardising the column names 
    msoa_income_data.columns = (
        msoa_income_data.columns
        .str.strip() # Ensuring that the space before and after the strings do not affect analysis
        .str.lower() # Coverting the strings to lowercase
        .str.replace(" ", "_") # Replacing the spaces in between words with underscores
        .str.replace("£", "", regex = False) # Removing any currency symbols from numerical values
    )

    # Looking for any duplicates using the 'msoa_code' as this should be unique to each row
    duplicate_rows = msoa_income_data[msoa_income_data.duplicated(subset = ["msoa_code"])]
    if not duplicate_rows.empty:
        print(f"The duplicate rows found in {sheet}:")
        print(duplicate_rows)
        print("-" * 60)
    else:
        print("There are no duplicate rows in {sheet}.")
    
    # Checking for any missing values in the dataset
    print(f"The missing values in {sheet}:")
    print(msoa_income_data.isnull().sum())
    print("-" * 60)

    # Converting data types - income and limits to numeric data types
    # In other words, changing the values where variable names contain the word 'limit' or 'income'.
    cols_numeric = [col for col in msoa_income_data.columns if "income" in col or "limit" in col]
    msoa_income_data[cols_numeric] = msoa_income_data[cols_numeric].apply(pd.to_numeric, errors = "coerce")

    # Identifying anomalies/outliers through some descriptive statisitics 
    print(f"These are the descriptive statistics for {sheet}:")
    print(msoa_income_data[cols_numeric].describe())
    print("-" * 60)

    # Some basic integrity checks such as negative or invalid values (the incomes should not be negative)
    income_invalid = msoa_income_data[cols_numeric].lt(0).any(axis = 1)
    if income_invalid.any():
        print(f"The invalid incomes values found in {sheet}:")
        print(msoa_income_data[income_invalid])
    else:
        print(f"No invalid income values in {sheet}")

    adjust_data[sheet] = msoa_income_data

# Defining the sheet names; one for analysis and the rest for backup
chosen_sheet = "Net income after housing costs"
other_sheets = ["Total weekly income", "Net weekly income", "Net income before housing costs"]

# Defining a function to filter for only London data
def filtering_for_london(data):
    return data[data['region_name'].str.lower() == 'london']

# Separating the chosen sheet for analysis
chosen_data = adjust_data[chosen_sheet]
print(f"Processing the data for {chosen_sheet}")

# Filtering for only the London data
filtered_chosen_data = filtering_for_london(chosen_data)
print(f"Successfully filtered {chosen_sheet} for London data")

# Saving the chosen sheet after filtering for London data
chosen_file_name = f"{processed_path}msoa_income_{chosen_sheet.replace(' ', '_').lower()}.csv"
filtered_chosen_data.to_csv(chosen_file_name, index = False)
print(f"{chosen_file_name} has been saved successfully. \n")

# Separating the remaining sheets for backup
for sheet in other_sheets:
    msoa_income_data = adjust_data[sheet]
    print(f"Processing the data for {sheet}")

    # Filtering for only London data
    filtered_msoa_data = filtering_for_london(msoa_income_data)
    print(f"Successfully filtered {chosen_sheet} for London data")

    # Saving each backup sheet after filtering for London
    backup_file_name = f"{processed_path}backup_msoa_income_{sheet.replace(' ', '_').lower()}.csv"
    filtered_msoa_data.to_csv(backup_file_name, index = False)
    print(f"{backup_file_name} has been saved successfully. \n")

