# Examen BentoML
python3 -m venv env
.\env\Scripts\activate
bentoml build   
bentoml containerize vermont_admission:latest
docker run --rm -p 3000:3000 docker run --rm -p 3000:3000 vermont_admission:7tazfkaa3sw22tcj

vermont_admission:7tazfkaa3sw22tcj  
python -m pytest .\src\test_unitaires.py
