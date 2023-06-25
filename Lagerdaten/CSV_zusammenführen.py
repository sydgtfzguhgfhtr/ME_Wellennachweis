import pandas as pd

csv1 = pd.read_csv(r"einreihige_Rillenkugellager\einreihige_Rillenkugellager-page-262-table-1.csv")
csv2 = pd.read_csv(r"einreihige_Rillenkugellager\einreihige_Rillenkugellager-page-263-table-1.csv")

merge = pd.concat([csv1,csv2],axis=1)

merge.to_csv("einreihige_Rillenkugellager.csv")