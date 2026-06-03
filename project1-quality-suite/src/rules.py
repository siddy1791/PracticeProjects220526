import pandas as pd

def validate_null_check(df:pd.DataFrame,rule_config:dict) -> pd.DataFrame:
    """Finds rows where specified columns contain null or missing values."""
    columns = rule_config['columns']
    return df[df[columns].isnull().any(axis=1)]

def validate_duplicate_check(df:pd.DataFrame,rule_config:dict) -> pd.DataFrame:
    """Find records (whole row) which occur more than once in the table"""
    columns = rule_config['columns']
    return  df[df.duplicated(subset=columns)]

def validate_value_range_check(df:pd.DataFrame,rule_config:dict) -> pd.DataFrame:
    """Find records whose data is out of the desired range(outliers) in the table"""
    columns = rule_config['columns']
    max_value = rule_config['max']
    min_value = rule_config['min']

    # 1. Slice out a multi-column DataFrame containing ONLY the target columns
    target_matrix = df[columns]

    # 2. Evaluate the conditions across the entire grid matrix
    # This creates a matching grid of True/False values for every cell
    out_of_bounds_grid = (target_matrix > max_value) | (target_matrix < min_value)

    # 3. Collapse the grid row-by-row using .any(axis=1)
    # If ANY column in a given row evaluates to True (out of bounds), flag the whole row!
    failed_row_mask = out_of_bounds_grid.any(axis=1)

    # 4. Return the filtered root DataFrame rows that failed the test
    return df[failed_row_mask]



RULE_RIGISTRY = {
    'null_check' : validate_null_check,
    'duplicate_check' : validate_duplicate_check,
    'value_range_check' : validate_value_range_check
}