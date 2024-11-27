from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import db_session, engine, Base, Department, Employee
from schema import schema
from schema_relay import schema as schema_relay
from datetime import date

def init_data():
    Base.metadata.create_all(bind=engine)
    
    engineering = Department(name='Engineering', description='Handles product development and technology')
    hr = Department(name='Human Resources', description='Manages employee well-being and recruitment')
    sales = Department(name='Sales', description='Responsible for sales and customer relationships')

    db_session.add_all([engineering, hr, sales])

    employees = [
        Employee(name='Alice', lastname='Smith', hiredon=date(2020, 6, 15), position='Software Engineer', department=engineering),
        Employee(name='Bob', lastname='Brown', hiredon=date(2019, 3, 10), position='QA Engineer', department=engineering),
        Employee(name='Clara', lastname='Johnson', hiredon=date(2021, 9, 1), position='Recruiter', department=hr),
        Employee(name='David', lastname='Davis', hiredon=date(2018, 7, 22), position='HR Manager', department=hr),
        Employee(name='Eve', lastname='Wilson', hiredon=date(2022, 1, 5), position='Sales Executive', department=sales),
        Employee(name='Frank', lastname='Taylor', hiredon=date(2020, 11, 15), position='Account Manager', department=sales)
    ]
    db_session.add_all(employees)
    db_session.commit()

# Flask app setup
app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    )
)

app.add_url_rule(
    '/graphql-relay',
    view_func=GraphQLView.as_view(
        'graphql-relay',
        schema=schema_relay,
        graphiql=True,
    )
)

if __name__ == '__main__':
    app.run(debug=True)
