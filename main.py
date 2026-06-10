
from decimal import Decimal
from database import Base, engine
from crud import (
    create_department,
    create_employee,
    create_project,
    deactivate_project,
    get_all_departments,
    get_all_employees,
    get_all_projects,
    get_employees_with_department_names,
    get_project_employees_departments,
    update_employee_salary
    
)

def main():
    Base.metadata.create_all(engine)
    it = create_department('IT')
    hr = create_department('HR')
    if it:
        ivan = create_employee('Ivan', Decimal("10000.00"), it.id)
        anna = create_employee('Anna', Decimal("80000.00"), it.id)
        if ivan:
            create_project('Internal CRM', Decimal('50000.00'), ivan.id)
        if anna:
            create_project('Mobile CRM', Decimal('100000.00'), anna.id)
    print('Все отделы:')
    for dp in get_all_departments():
        print(dp.id, dp.name)
    print('Все сотрудники:')
    for emp in get_all_employees():
        print(emp.id, emp.name)
    print('Все проекты:')
    for pr in get_all_projects():
        print(pr.id, pr.name)
    print('Сотрудники и отделы:')
    for emp, dp in get_employees_with_department_names():
        print(emp, dp)
    print('Проекты, сотрудники, и отделы: ')
    for row in get_project_employees_departments():
        print(row.project_name, row.employee_name, row.department_name)

main()