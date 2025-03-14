import requests
import pandas as pd

# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3000/login"
predict_url = "http://127.0.0.1:3000/models/lr_regression/predict"


# Données de connexion
credentials = {
    "username": "bruno",
    "password": "jedimaster"
}

# Send a POST request to the login endpoint
login_response = requests.post(
    login_url,
    headers={"Content-Type": "application/json"},
    json=credentials
)

# Check if the login was successful
if login_response.status_code == 200:
    token = login_response.json().get("token")
    print("Token JWT obtenu:", token)

    data = pd.read_csv("data/processed/X_test.csv")

    data = data.iloc[1,]
    inputdata = {
        "GREScore": int(data["GREScore"]),
        "TOEFLScore": int(data["TOEFLScore"]),
        "UniversityRating": int(data["UniversityRating"]),
        "SOP": float(data["SOP"]),
        "LOR": float(data["LOR"]),
        "CGPA": float(data["CGPA"]),
        "Research": int(data["Research"])}

    # Send a POST request to the prediction
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=inputdata
    )

    print("Réponse de l'API de prédiction:", response.text)
else:
    print("Erreur lors de la connexion:", login_response.text)