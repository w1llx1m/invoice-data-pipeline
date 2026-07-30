import pandas as pd


def capitalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols_to_capitalize = ['first_name', 'last_name', 'city']
    df = df.copy()
    df[cols_to_capitalize] = df[cols_to_capitalize].apply(
        lambda col: col.astype(str).str.title()
    )
    return df


def email_format(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['email'] = df['email'].astype(str).str.lower()
    return df


def blank_removal(df: pd.DataFrame) -> pd.DataFrame:
    cols_to_fill = ['stock_code', 'product_id']
    df = df.copy()
    df[cols_to_fill] = df[cols_to_fill].apply(
        lambda col: col.astype(str).str.strip()
    )
    return df

