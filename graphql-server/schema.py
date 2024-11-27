import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Employee, Department

class DepartmentType(SQLAlchemyObjectType):
    class Meta:
        model = Department
        interfaces = ()

class EmployeeType(SQLAlchemyObjectType):
    class Meta:
        model = Employee
        interfaces = ()

class Query(graphene.ObjectType):
    all_departments = graphene.List(DepartmentType)
    all_employees = graphene.List(
        EmployeeType,
        hired_after=graphene.Date(),
        position=graphene.String()
    )

    def resolve_all_departments(self, info):
        return db_session.query(Department).all()

    def resolve_all_employees(self, info, hired_after=None, position=None):
        query = db_session.query(Employee)
        if hired_after:
            query = query.filter(Employee.hiredon > hired_after)
        if position:
            query = query.filter(Employee.position == position)
        return query.all()
    
class CreateEmployee(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        lastname = graphene.String(required=True)
        position = graphene.String(required=True)
        hiredon = graphene.Date(required=True)
        department_id = graphene.ID(required=True)

    employee = graphene.Field(lambda: EmployeeType)

    def mutate(self, info, name, lastname, position, hiredon, department_id):
        department = db_session.query(Department).filter_by(id=department_id).first()
        if not department:
            raise Exception("Department not found")
        
        employee = Employee(
            name=name,
            lastname=lastname,
            position=position,
            hiredon=hiredon,
            department=department
        )
        db_session.add(employee)
        db_session.commit()
        return CreateEmployee(employee=employee)
    
class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
