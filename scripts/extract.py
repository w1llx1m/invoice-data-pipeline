import pandas as pd

def extract():
   ret = pd.read_csv(".\\data\\raw\\invoices_20260724.csv") 
   print(ret)
   return ret

extract()

if __name__ == "__main__":
   extract()