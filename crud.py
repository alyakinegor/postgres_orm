from database import sesion_local
from models import Department, Employee, Decimal, Project
from sqlalchemy import select, update, delete, func

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

# with sesion_local() as session:
#     department = Department(name='Dev')
#     employee = Employee(name='Иван', salary=Decimal('100000.00'))
#     project = Project(
#         name='Modile',
#         budget=Decimal('2000000.00')
#     )
#     department.employees.append(employee)
#     employee.projects.append(project)
#     session.add(department)
#     session.commit()

def get_employee_by_id(employee_id: int):
    with sesion_local() as session:
        return session.get(Employee, employee_id)

def get_all_employees():
    with sesion_local() as session:
        stmt = select(Employee)
        employees = session.execute(stmt).scalars().all()
        return employees
def get_all_departments():
    with sesion_local() as session:
        stmt = select(Department)
        dp = session.execute(stmt).scalars().all()
        return dp

def get_all_projects():
    with sesion_local() as session:
        stmt = select(Project)
        pr = session.execute(stmt).scalars().all()
        return pr

def get_employees_with_salary_gt(amount):
    with sesion_local() as session:
        stmt = select(Employee).where(Employee.salary > amount)
        return session.execute(stmt).scalars().all()

def get_employees_order_by_salary_desc():
    with sesion_local() as session:
        stmt = select(Employee).order_by(Employee.salary.desc())
        return session.execute(stmt).scalars().all()
    
def get_employees_page(page:int, per_page: int):
    with sesion_local() as session:
        stmt = select(Employee).offset((page -1) * per_page).limit(per_page)
        return session.execute(stmt).scalars().all()
    
def update_employee_salary(employee_id: int, salary: int):
    with sesion_local() as session:
        employee = session.get(Employee, employee_id)
        if employee is None:
            return None
        employee.salary = salary
        session.commit()
        session.refresh(employee)
        return employee
    
def update_employee_via_update(employee_id:int, salary):
    with sesion_local() as session:
        stmt = (
            update(Employee).where(Employee.id == employee_id).values(salary=salary)
        )
        session.execute(stmt)
        session.commit()

def delete_project(project_id):
    with sesion_local() as session:
        project = session.get(Project, project_id)
        if project is None:
            return False
        
        session.delete(project)
        session.commit()
        return True
    
def delete_project_via_delete(project_id):
    stmt = (
        delete(Project).where(Project.id == project_id)
    )
    session.execute(stmt)
    session.commit()
    return True
def get_employees_with_department_names():
    with sesion_local() as session:
        stmt = (
            select(Employee.name, Department.name).join(Department, Employee.department_id == Department.id)
        )
        return session.execute(stmt).all()
    
def get_employees_with_optional_department():
    with sesion_local() as session:
        stmt = (
            select(Employee.name, Department.name).outerjoin(Department, Employee.department_id == Department.id)
        )
        return session.execute(stmt).all()
    
def get_project_employees_departments():
    with sesion_local() as session:
        stmt = select(Project.name.label("project_name"),Employee.name.label("employee_name"), Department.name.label('department_name')).join(Employee, Employee.id == Project.employee_id).join(Department, Department.id == Employee.department_id)
        return session.execute(stmt).all()

def count_employees():
    with sesion_local() as session:
        stmt = select(func.count(Employee.id))
        return session.execute(stmt).scalar()
    
def get_average_salary():
    with sesion_local() as session:
        stmt = select(func.avg(Employee.salary))
        return session.execute(stmt).scalar()
    
def get_max_salary():
    with sesion_local() as session:
        stmt = select(func.max(Employee.salary))
        return session.execute(stmt).scalar()
def get_min_salary():
    with sesion_local() as session:
        stmt = select(func.min(Employee.salary))
        return session.execute(stmt).scalar()
    
def get_total_active_projects_budget():
    with sesion_local() as session:
        stmt = (
            select(func.sum(Project.budget)).where(Project.is_active._is(True))
        )
        return session.execute(stmt).scalar()
    
def count_employees_by_department():
    with sesion_local() as session:
        stmt = (
            select(Department.name, func.count(Employee.id)).join(Employee, Employee.department_id == Department.id).group_by(Department.name)
        )
        return session.execute(stmt).all()
    
def get_average_salary_for_department():
    with sesion_local() as session:
        stmt = (
            select(Department.name, func.avg(Employee.salary.label('avg_salary'))).join(Employee, Employee.department_id == Department.id).group_by(Department.name)
        )
        return session.execute(stmt).all()
    
def deactivate_project(project_id: int):
    with sesion_local() as session:
        project = session.get(Project, project_id)
        if project is None:
            return None
        project.is_active = False
        session.commit()
        session.refresh(project)
        return project




# department = create_department('Тест1')
# print(department.id, department.name)