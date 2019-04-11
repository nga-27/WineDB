import numpy as np 
import pandas as pd 

print("Starting wineDB...")

FILENAME = "Nick and Jill's Wine List.xlsx"

xl = pd.ExcelFile(FILENAME)

#print(xl.sheet_names[1])
sheetData = pd.read_excel(FILENAME, xl.sheet_names[1])

print(sheetData.columns)

w = sheetData.groupby(['Country']).count()
print(w)
v = sheetData.groupby(['Grape Variety']).count()
print(v)

# will provide keys of groupings!
y = sheetData.groupby(['Country']).groups.keys()
print(y)

z = sheetData.groupby(['Grape Variety']).groups.keys()
print(z)

print("")
print("")
z2 = sheetData.groupby(['Grape Variety']).groups.items()
print(z2)