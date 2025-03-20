import pandas as pd

def extract(file_path):
    df = pd.read_excel(file_path, engine="openpyxl")
    return df

file_path = "C:\\Users\\RAYENE\\Downloads\\production.xlsx"
df = extract(file_path)


