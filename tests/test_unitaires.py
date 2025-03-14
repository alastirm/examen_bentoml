import requests
import pandas as pd
import bentoml
import jwt
from datetime import datetime, timedelta
import json

# Secret key and algorithm for JWT authentication
JWT_SECRET_KEY = "your_jwt_secret_key_here"
JWT_ALGORITHM = "HS256"

# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3000/login"
predict_url = "http://127.0.0.1:3000/models/lr_regression/predict"

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

# test jeton manquant

def test_missingtoken():

    token = ""
    # Send a POST request to the prediction
    response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": ""
            },
            json=inputdata
        )
   

    print("Réponse de l'API de prédiction:", response.text)
    
    assert response.text == '{"detail":"Missing authentication token"}'

# test jeton mauvais 

def test_badtoken():

    token = "zadazaqcqazxc"
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
    
    assert response.text == '{"detail":"Invalid token"}'


# test jeton expiré

def test_expired_token():

    expiration =  datetime.now() + timedelta(hours=-1)
    payload = {
        "sub": "bruno",
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=inputdata
        )
    
    assert response.text == '{"detail":"Token has expired"}'

# test bon jeton

def test_goodtoken():
    expiration =  datetime.now() + timedelta(hours=1)
    payload = {
        "sub": "bruno",
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=inputdata
        )
    
    assert response.status_code == 200 


def test_validuser():
    credentials = {
        "username": "bruno",
        "password": "jedimaster"
    }

    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=credentials
        )
    
    token = login_response.json().get("token")

    response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=inputdata
        )
    
    assert response.status_code == 200 

def test_nonvaliduser():
    credentials = {
        "username": "tata",
        "password": "yoyo"
    }

    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=credentials
    )
    
    assert login_response.status_code == 401 

def test_noresponse_badtoken():
    token = "azdkazd"
    response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=inputdata
        )

    assert response.status_code == 401 

def test_noresponse_missingtoken():
    response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": ""
            },
            json=inputdata
        )

    assert response.status_code == 401 

def test_unvalid_data():
    inputdata = {"invalide" : "invalide"}

    credentials = {
        "username": "bruno",
        "password": "jedimaster"
    }

    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=credentials
        )
    
    token = login_response.json().get("token")

    response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=inputdata
        )
    
    assert response.status_code == 400 

def test_valid_predict():
    inputdata = {
        "GREScore": 1,
        "TOEFLScore": 2,
        "UniversityRating": 4,
        "SOP": 1.5,
        "LOR": 1.5,
        "CGPA": 1.5,
        "Research": 1}


    credentials = {
        "username": "bruno",
        "password": "jedimaster"
    }

    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=credentials
        )
    
    token = login_response.json().get("token")

    response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=inputdata
        )
    
    response = json.loads(response.content.decode('utf-8'))
    
    assert type(response['prediction'][0][0]) == float