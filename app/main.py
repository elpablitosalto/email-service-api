from fastapi import FastAPI
from app.api.email import router as email_router

app = FastAPI(title="Email Service API")

app.include_router(email_router)

@app.get("/")
def root():
    return {"message": "Email Service API is running"} 