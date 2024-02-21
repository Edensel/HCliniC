from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, Clinic, Manager, Staff, Shift, Patient, employee_shift_association
from datetime import datetime
import random
import os

# Create an SQLAlchemy engine to interact with the database
engine = create_engine('sqlite:///clinical.db')

# Check if the database file exists
if not os.path.exists('clinical.db'):
    print("Database file 'clinical.db' does not exist. Please create it.")
    exit()

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a Faker instance
fake = Faker()

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def create_fake_clinics(num_clinics=100):
    for _ in range(num_clinics):
        clinic = Clinic(
            name=fake.company(),
            location=fake.address()
        )
        session.add(clinic)
    session.commit()

def create_fake_managers(num_managers=100):
    clinics = session.query(Clinic).all()
    for _ in range(num_managers):
        clinic = random.choice(clinics)
        manager = Manager(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=random.choice(['Male', 'Female']),
            email=fake.email(),
            job_title=fake.job(),
            role=fake.random_element(elements=('Supervisor', 'Manager')),
            clinic=clinic
        )
        try:
            session.add(manager)
            session.commit()
        except IntegrityError:
            session.rollback()
            continue

def create_fake_staff(num_staff=100):
    clinics = session.query(Clinic).all()
    for _ in range(num_staff):
        clinic = random.choice(clinics)
        staff = Staff(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=random.choice(['Male', 'Female']),
            email=fake.email(),
            job_title=fake.job(),
            role=fake.random_element(elements=('Receptionist', 'Nurse', 'Technician')),
            clinic=clinic
        )
        try:
            session.add(staff)
            session.commit()
        except IntegrityError:
            session.rollback()
            continue

def create_fake_shifts(num_shifts=100):
    clinics = session.query(Clinic).all()
    for _ in range(num_shifts):
        clinic = random.choice(clinics)
        shift = Shift(
            start_time=fake.date_time_this_decade(),
            end_time=fake.date_time_this_decade(),
            name=fake.random_element(elements=('Morning', 'Afternoon', 'Night')),
            supervisor=fake.name(),
            clinic=clinic
        )
        session.add(shift)
    session.commit()

def create_fake_patients(num_patients=100):
    for _ in range(num_patients):
        patient = Patient(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=random.choice(['Male', 'Female']),
            date_of_birth=fake.date_of_birth(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            address=fake.address(),
            medical_history=fake.text()
        )
        session.add(patient)
    session.commit()

def create_fake_employee_shift_association(num_associations=100):
    employees = session.query(Staff).all()
    shifts = session.query(Shift).all()
    for _ in range(num_associations):
        employee = random.choice(employees)
        shift = random.choice(shifts)
        shift.staff.append(employee)
    session.commit()

# Call the functions to generate fake data
create_fake_clinics()
create_fake_managers()
create_fake_staff()
create_fake_shifts()
create_fake_patients()
create_fake_employee_shift_association()
