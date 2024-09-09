import pandas as pd
from typing import List, Dict, Any

def validate_csv_structure(df: pd.DataFrame) -> bool:
    """
    Validate the structure of the CSV data.
    
    Args:
    df (pd.DataFrame): The DataFrame containing the CSV data.
    
    Returns:
    bool: True if the structure is valid, False otherwise.
    """
    required_columns = ['skor', 'baslik', 'entiri', 'silinmis', 'tarih']
    
    # Check if all required columns are present
    if not all(col in df.columns for col in required_columns):
        return False
    
    # Check data types
    expected_types = {
        'skor': 'int64',
        'baslik': 'object',
        'entiri': 'object',
        'silinmis': 'bool',
        'tarih': 'object'
    }
    
    for col, expected_type in expected_types.items():
        if df[col].dtype != expected_type:
            return False
    
    return True

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the data.
    
    Args:
    df (pd.DataFrame): The DataFrame to clean.
    
    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    # Convert 'tarih' to datetime
    df['tarih'] = pd.to_datetime(df['tarih'], errors='coerce')
    
    # Remove rows with invalid dates
    df = df.dropna(subset=['tarih'])
    
    # Ensure 'skor' is integer
    df['skor'] = df['skor'].astype(int)
    
    # Ensure 'silinmis' is boolean
    df['silinmis'] = df['silinmis'].astype(bool)
    
    # Strip whitespace from string columns
    for col in ['baslik', 'entiri']:
        df[col] = df[col].str.strip()
    
    return df

def validate_and_clean_data(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Validate and clean the input data.
    
    Args:
    data (List[Dict[str, Any]]): The input data as a list of dictionaries.
    
    Returns:
    pd.DataFrame: The validated and cleaned DataFrame.
    """
    df = pd.DataFrame(data)
    
    if not validate_csv_structure(df):
        raise ValueError("Invalid CSV structure")
    
    return clean_data(df)