import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Employee, Department

class DepartmentNode(SQLAlchemyObjectType):
    class Meta:
        model = Department
        interfaces = (relay.Node,)

class EmployeeNode(SQLAlchemyObjectType):
    class Meta:
        model = Employee
        interfaces = (relay.Node,)
        
class EmployeeFilterInput(graphene.InputObjectType):
    hired_after = graphene.String()
    position = graphene.String()

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_departments = SQLAlchemyConnectionField(DepartmentNode.connection, sort=None)
    all_employees = SQLAlchemyConnectionField(EmployeeNode.connection, filter=EmployeeFilterInput(), sort=None)
    
    def resolve_all_employees(self, info, filter=None, **kwargs):
        query = db_session.query(Employee)
        if filter:
            if filter.get('hired_after'):
                query = query.filter(Employee.hiredon > filter['hired_after'])
            if filter.get('position'):
                query = query.filter(Employee.position == filter['position'])
        return query.all()

class CreateEmployee(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        lastname = graphene.String(required=True)
        position = graphene.String(required=True)
        hiredon = graphene.Date(required=True)
        department_id = graphene.ID(required=True)

    employee = graphene.Field(EmployeeNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, name, lastname, position, hiredon, department_id):
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

schema = graphene.Schema(query=Query, types=[DepartmentNode, EmployeeNode], mutation=Mutation)
