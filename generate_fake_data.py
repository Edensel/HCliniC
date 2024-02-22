from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, Clinic, Manager, Staff, Shift, Patient, Appointment, Doctor, EmployeeShiftAssociation
import random
import os

engine = create_engine('sqlite:///clinical.db')

if not os.path.exists('clinical.db'):
    print("Database file 'clinical.db' does not exist. Please create it.")
    exit()

Base.metadata.create_all(engine)

fake = Faker()

Session = sessionmaker(bind=engine)
session = Session()

def create_fake_clinics(num_clinics=10):
    for _ in range(num_clinics):
        clinic = Clinic(
            name=fake.company(),
            location=fake.address()
        )
        session.add(clinic)
    session.commit()

def create_fake_managers(num_managers=10):
    clinics = session.query(Clinic).all()
    for _ in range(num_managers):
        clinic = random.choice(clinics)
        manager = Manager(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=fake.random_element(elements=('Male', 'Female')),
            email=fake.email(),
            job_title=fake.job(),
            clinic=clinic
        )
        try:
            session.add(manager)
            session.commit()
        except IntegrityError:
            session.rollback()
            continue

def create_fake_staff(num_staff=10):
    clinics = session.query(Clinic).all()
    for _ in range(num_staff):
        clinic = random.choice(clinics)
        staff = Staff(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=fake.random_element(elements=('Male', 'Female')),
            email=fake.email(),
            job_title=fake.job(),
            clinic=clinic
        )
        try:
            session.add(staff)
            session.commit()
        except IntegrityError:
            session.rollback()
            continue

def create_fake_shifts(num_shifts=10):
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

def create_fake_doctors(num_doctors=10):
    clinics = session.query(Clinic).all()
    for _ in range(num_doctors):
        clinic = random.choice(clinics)
        doctor = Doctor(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=fake.random_element(elements=('Male', 'Female')),
            email=fake.email(),
            job_title=fake.job(),
            clinic=clinic
        )
        try:
            session.add(doctor)
            session.commit()
        except IntegrityError:
            session.rollback()
            continue

def create_fake_patients(num_patients=10):
    for _ in range(num_patients):
        patient = Patient(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=fake.random_element(elements=('Male', 'Female')),
            year_of_birth=fake.random_int(min=1950, max=2000),
            email=fake.email(),
            phone_number=fake.phone_number()
        )
        session.add(patient)
    session.commit()

def create_fake_appointments(num_appointments=10):
    patients = session.query(Patient).all()
    doctors = session.query(Doctor).all()
    for _ in range(num_appointments):
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        appointment = Appointment(
            patient=patient,
            doctor=doctor,
            date=fake.date_this_decade(),
            time=fake.time(),
            patient_name=fake.name(),
            phone_number=fake.phone_number()
        )
        session.add(appointment)
    session.commit()

def create_fake_employee_shift_association(num_associations=10):
    employees = session.query(Staff).all()
    shifts = session.query(Shift).all()
    for _ in range(num_associations):
        employee = random.choice(employees)
        shift = random.choice(shifts)
        shift.staff.append(employee)
    session.commit()


create_fake_clinics()
create_fake_managers()
create_fake_staff()
create_fake_doctors()
create_fake_shifts()
create_fake_patients()
create_fake_appointments()
create_fake_employee_shift_association()
