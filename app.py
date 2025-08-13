from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Table, Column
from sqlalchemy import Date, String, Integer, Float, ForeignKey

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)
db.init_app(app)



# service_mechanics = Table(
#     'service_mechanics',
#     Base.metadata,
#     Column('ticket_id', Integer, ForeignKey('service_tickets.id')),
#     Column('mechanic_id', Integer, ForeignKey('mechanics.id'))
# )

class Customers(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(360), unique=True, nullable=False) 
    phone: Mapped[str] = mapped_column(String(360), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=True)

    service_tickets: Mapped[list['Service_tickets']] = relationship('Service_tickets', back_populates='customer')


class Mechanics(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(360), unique=True, nullable=False) 
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    salary: Mapped[str] = mapped_column(String(360), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=True)

    ticket_mechanics: Mapped[list['Ticket_mechanics']] = mapped_column('Ticket_mechanics', back_populates='mechanic')
    service_tickets: Mapped[list['Service_tickets']] = mapped_column('Service_tickets', secondary='ticket_mechanics', back_populates='mechanics')

class Service_tickets(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id'), nullable=False)
    service_desc: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    VIN: Mapped[str] = mapped_column(String(360), unique=True, nullable=False) 
    service_date: Mapped[date] = mapped_column(Date, nullable=False)

    customer: Mapped['Customers'] = relationship('Customers', back_populates='service_tickets')
    ticket_mechanics: Mapped[list['Ticket_mechanics']] = relationship('Ticket_mechanics', back_populates='service_ticket')
    mechanics: Mapped[list['Mechanics']] = relationship('Mechanics', secondary='ticket_mechanics', back_populates='service_tickets')
    

class Ticket_mechanics(Base):
    __tablename__ = 'ticket_mechanics'

    ticket_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id'), nullable=False)
    mechanic_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id'), nullable=False)

    service_ticket: Mapped['Service_tickets'] = mapped_column('Service_tickets', back_populates='ticket_mechanics')
    mechanic: Mapped['Mechanics'] = mapped_column('Mechanics', back_populates='ticket_mechanics')


with app.app_context():
    db.create_all()

app.run()




# ________________________

# ```
# # Define the association table
# student_course_association = Table(
#     'student_course_association', Base.metadata,
#     Column('student_id', Integer, ForeignKey('students.id')),
#     Column('course_id', Integer, ForeignKey('courses.id'))
# )

# class Student(Base):
#     __tablename__ = 'students'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     # Define the relationship to Course, using the association table
#     # and back_populates to synchronize with the 'students' attribute on Course
#     courses = relationship('Course', secondary=student_course_association, back_populates='students')

# class Course(Base):
#     __tablename__ = 'courses'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     # Define the relationship to Student, using the association table
#     # and back_populates to synchronize with the 'courses' attribute on Student
#     students = relationship('Student', secondary=student_course_association, back_populates='courses')
# ```