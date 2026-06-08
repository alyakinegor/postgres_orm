from database import sesion_local
from models import Department, Employee, Decimal, Project

def create_department(name: str):
    with sesion_local() as session:
        department = Department(name=name)
        session.add(department)
        session.commit()
        session.refresh(department)
        return department

def create_employee(
        name: str,
        salary: Decimal,
        department_id: int | None = None
):
    with sesion_local() as session:
        employee = Employee(department_id=department_id, name=name, salary=salary)
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee
    

def create_project(
        name: str,
        budget: Decimal,
        employee_id: int | None = None
):
    with sesion_local() as session:
        project = Project(
            name=name, 
            budget=budget,
            employee_id=employee_id
        )
        session.add(project)
        session.commit()
        session.refresh(project)
        return project

with sesion_local() as session:
    department = Department(name='Dev')
    employee = Employee(name='Иван', salary=Decimal('100000.00'))
    project = Project(
        name='Modile',
        budget=Decimal('2000000.00')
    )
    department.employees.append(employee)
    employee.projects.append(project)
    session.add(department)
    session.commit()
department = create_department('Тест1')
print(department.id, department.name)