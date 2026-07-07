from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Este é o home"}