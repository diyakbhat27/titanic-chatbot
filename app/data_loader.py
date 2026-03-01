import pandas as pd
import os

def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "titanic.xlsx")

    df = pd.read_excel(file_path)
    return df