import pandas as pd


def validate_required_fields(df: pd.DataFrame) -> pd.Series:
    required_cols = ['first_name', 'last_name','email', 'product_id','qty','amount','invoice_date']
    return df[required_cols].notna().all(axis=1)

def validate_email(df: pd.DataFrame) -> pd.Series:
    email_match = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    return df['email'].astype(str).str.match(email_match)

def validate_amount(df: pd.DataFrame) -> pd.Series:
    return df['amount'] > 0

def validate_quantity(df: pd.DataFrame) -> pd.Series:
    return df['qty'] > 0

def validate_all(df: pd.DataFrame) -> pd.Series:
    mask_required = validate_required_fields(df)
    mask_email = validate_email(df)
    mask_amount = validate_amount(df)
    mask_quantity = validate_quantity(df)

    return mask_required & mask_email & mask_amount & mask_quantity

def validated_split(df: pd.DataFrame):
    mask_approved = validate_all(df)
    df_approved = df[mask_approved].copy()
    df_repproved = df[~mask_approved].copy()
    return df_approved, df_repproved