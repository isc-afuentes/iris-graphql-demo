from sqlalchemy import *
from sqlalchemy.orm import relationship, declarative_base, Session, scoped_session, sessionmaker, relationship, backref

engine = create_engine('iris://superuser:SYS@localhost:1972/USER')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

Base.query = db_session.query_property()

class Department(Base):
    __tablename__ = 'departments'
    __table_args__ = {'schema': 'dc_graphql'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    employees = relationship('Employee', back_populates='department')

class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'dc_graphql'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    hiredon = Column(Date)
    position = Column(String)
    department_id = Column(Integer, ForeignKey('dc_graphql.departments.id'))

    department = relationship('Department', back_populates='employees')
