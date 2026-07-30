import pandas as pd
import datetime as dt
import re


def  capitalize_title(df: pd.DataFrame) -> pd.Series:
    cols_ToCapitalize = ['first_name', 'last_name', 'city']
    return df[cols_ToCapitalize].all(axis=1).astype(str).str.capitalize()

def date_format(df: pd.DataFrame) -> pd.Series:
    # date_ToFormat = ['invoice_date'] #dd/mm/yyyy
    pass

