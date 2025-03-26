import pandas as pd

t8 = pd.read_csv("C:\\Users\\Lenovo\\Desktop\\Bank_Transaction_Fraud_Detection.csv")

print(pd.DataFrame(t8))
print(pd.isnull(t8))

print(t8.isnull().sum().sum())

print(pd.isna(t8))

