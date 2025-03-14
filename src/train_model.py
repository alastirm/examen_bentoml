
import pandas as pd
import bentoml
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score


X_train = pd.read_csv("data/processed/X_train.csv", index_col="Serial No.")
X_test = pd.read_csv("data/processed/X_test.csv", index_col="Serial No.")
y_train = pd.read_csv("data/processed/y_train.csv", index_col="Serial No.")
y_test = pd.read_csv("data/processed/y_test.csv", index_col="Serial No.")

model = LinearRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

acc = model.score(X_test, y_test)


if acc >= 0.7:
    # Enregistrer le modèle dans le Model Store de BentoML
    model_ref = bentoml.sklearn.save_model("admission_lr", model)

    print(f"Modèle enregistré sous : {model_ref}")


