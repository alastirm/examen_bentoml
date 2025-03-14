
# API base model
from pydantic import BaseModel, Field
from typing import Optional, List

# basics
import pandas as pd
import numpy as np
# securisation
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from datetime import datetime, timedelta

# bentoml
import bentoml
from bentoml.io import NumpyNdarray, JSON
from bentoml.exceptions import InvalidArgument, BentoMLException
from http import HTTPStatus


# Define a custom exception for login
class MyCustomException(BentoMLException):
    error_code = HTTPStatus.UNAUTHORIZED

# Define a simple custom exception for invalid argument errors
class MyCustomInvalidArgsException(InvalidArgument):
    pass

# Secret key and algorithm for JWT authentication
JWT_SECRET_KEY = "your_jwt_secret_key_here"
JWT_ALGORITHM = "HS256"

users = {
    "bruno": "jedimaster",
    "anakin": "order66"
    }

predict_url = "http://127.0.0.1:3000/models/lr_regression/predict"

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("APPPPPPPPPPPPPPPPPPPPPPPPPPP", request.url.path)
        if request.url.path == "/models/lr_regression/predict":
            token = request.headers.get("Authorization")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Missing authentication token"})

            try:
                token = token.split()[1]  # Remove 'Bearer ' prefix
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

            request.state.user = payload.get("sub")

        response = await call_next(request)
        return response

# model for the student data in input
class Studentdata(BaseModel):
    GREScore: int
    TOEFLScore: int
    UniversityRating: int
    SOP: float
    LOR: float
    CGPA: float
    Research: int

# load the trained model from bento
admission_lr = bentoml.sklearn.get("admission_lr:latest").to_runner()

# create the service API
vermont_admission = bentoml.Service("vermont_admission", runners=[admission_lr])

# Add the JWTAuthMiddleware to the service
vermont_admission.add_asgi_middleware(JWTAuthMiddleware)

# endpoint login for the service
@vermont_admission.api(input=JSON(), output = JSON(), route = "/login")
def login(credentials: dict) -> dict:
    username = credentials.get("username")
    password = credentials.get("password")

    if username in users and users[username] == password:
        token = create_jwt_token(username)
        return {"token": token}
    else:
        raise MyCustomException("Invalid credentials")
 


# Create an API endpoint for the service
@vermont_admission.api(
    input = JSON(pydantic_model=Studentdata),
    output = JSON(),
    route = "models/lr_regression/predict")

async def predict_admission(studentdata: Studentdata, 
                            ctx: bentoml.Context):

    request = ctx.request
    user = request.state.user if hasattr(request.state, 'user') else None

    # Convert the input data to a numpy array
    studentdata_arr = np.array(
        [studentdata.GREScore,
         studentdata.TOEFLScore,
         studentdata.UniversityRating,
         studentdata.SOP,
         studentdata.LOR,
         studentdata.CGPA,
         studentdata.Research])
    
    result = await admission_lr.predict.async_run(studentdata_arr.reshape(1, -1))

    return {"prediction": result.tolist(),
                "user": user}


def create_jwt_token(user_id: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token  



    
