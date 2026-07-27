import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
FILE_PATH = BASE_DIR/"data"/"raw"/"invoices_20260724.csv"   

def extract():
   ret = pd.read_csv(FILE_PATH) 
   return ret



