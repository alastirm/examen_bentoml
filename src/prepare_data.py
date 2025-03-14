import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


df = pd.read_csv("data/raw/admission.csv")

# df.head()
df.info()
# df.describe()
# df.isna().sum()
df.columns
df = df.set_index("Serial No.")

df = df.rename(columns = 
               {"Chance of Admit " : "Chance of Admit",
                "GRE Score" : "GREScore",
                "TOEFL Score" : "TOEFLScore",
                "University Rating" : "UniversityRating",
                'LOR ' : 'LOR'})

features = df.drop(columns = "Chance of Admit")
target = df["Chance of Admit"]

X_train, X_test, y_train, y_test = train_test_split(features, target, 
                                                    test_size=0.3, 
                                                    random_state=1234)


X_train.to_csv("data/processed/X_train.csv")
X_test.to_csv("data/processed/X_test.csv")
y_train.to_csv("data/processed/y_train.csv")
y_test.to_csv("data/processed/y_test.csv")