from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import employees

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Employee Management API',
    description='REST API for managing employees',
    version='1.0.0')

app.include_router(employees.router)

@app.get('/')
def root():
    return {'message': 'Employee Management API is running'}

@app.get('/health')
def get_health():
    return {'status':'healthy'}




