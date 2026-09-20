from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeResponse

router = APIRouter(
    prefix = '/employees',
    tags=['Employees'])


@router.post('/', response_model=EmployeeResponse)
def create_employee(
        employee : EmployeeCreate,
        db: Session = Depends(get_db)
):
    new_emp = Employee(
        name = employee.name,
        email = employee.email,
        department = employee.department,
        salary = employee.salary
        )
    
    db.add(new_emp)

    try:
        db.commit()
        db.refresh(new_emp)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail='Employee already exists'
        )


    return new_emp

@router.get('/',response_model=list[EmployeeResponse])
def get_employees(db: Session= Depends(get_db)) :
    employees = db.query(Employee).all()
    return employees

@router.get('/{emp_id}', response_model=EmployeeResponse)
def get_employee(emp_id: int, db: Session=Depends(get_db)):
    employee= (db.query(Employee).filter(Employee.id ==emp_id).first())

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail='Employee Not Found'
        )
    
    return employee

@router.put('/{emp_id}',response_model=EmployeeResponse)
def update_employee(emp_id: int, emp_create:EmployeeCreate, db: Session=Depends(get_db)):
    employee= (db.query(Employee).filter(Employee.id==emp_id).first())

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail='Emploee not found'
        )
    
    employee.name = emp_create.name
    employee.email = emp_create.email
    employee.salary = emp_create.salary
    employee.department = emp_create.department

    try:
        db.commit()
        db.refresh(employee)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail='Email already exists'
        )

    return employee

@router.delete('/{emp_id}')
def delete_employee(emp_id:int, db:Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == emp_id).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail='Employee Not Found'
        )
    

    db.delete(employee)
    db.commit()

    return {'message':'Employee deleted successfully'}
    