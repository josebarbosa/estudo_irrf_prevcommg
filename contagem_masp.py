import pandas as pd

df = pd.read_csv('folhamg022024.csv', sep=';', low_memory=False, encoding = "ISO-8859-1")

print(df['masp'].nunique())