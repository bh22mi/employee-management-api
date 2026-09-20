from pydantic import BaseModel, EmailStr, Field

class EmployeeCreate(BaseModel):
    name:str = Field(min_length=2, max_length=100)
    email:EmailStr
    department:str = Field(min_length=2, max_length=100)
    salary:int = Field(gt=0)

class EmployeeResponse(BaseModel):
    id: int
    name:str
    email:str
    department:str
    salary:int

    class Config:
        from_attributes: True