from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Clinic(Base):
    __tablename__ = 'clinics'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)

    managers = relationship("Manager", back_populates="clinic")
    staff = relationship("Staff", back_populates="clinic")
    shifts = relationship("Shift", back_populates="clinic")
    doctors = relationship("Doctor", back_populates="clinic")

    def __repr__(self):
        return f"Clinic(id={self.id}, name='{self.name}', location='{self.location}')"

class Manager(Base):
    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    email = Column(String, unique=True)
    job_title = Column(String)
    clinic_id = Column(Integer, ForeignKey('clinics.id'))
    clinic = relationship("Clinic", back_populates="managers")
    shifts = relationship("Shift", back_populates="manager")

    def __repr__(self):
        return f"Manager(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')"

class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    email = Column(String, unique=True)
    job_title = Column(String)
    clinic_id = Column(Integer, ForeignKey('clinics.id'))

    clinic = relationship("Clinic", back_populates="staff")
    shifts = relationship("Shift", secondary="employee_shift_association", back_populates="staff")
    employee_associations = relationship("EmployeeShiftAssociation", back_populates="staff")

    def __repr__(self):
        return f"Staff(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')"

class Shift(Base):
    __tablename__ = 'shifts'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    name = Column(String)
    supervisor = Column(String)
    clinic_id = Column(Integer, ForeignKey('clinics.id'))
    manager_id = Column(Integer, ForeignKey('managers.id'))
    
    clinic = relationship("Clinic", back_populates="shifts")
    manager = relationship("Manager", back_populates="shifts")
    staff = relationship("Staff", secondary="employee_shift_association", back_populates="shifts")
    employee_associations = relationship("EmployeeShiftAssociation", back_populates="shift")

    def __repr__(self):
        return f"Shift(id={self.id}, name='{self.name}', clinic_id={self.clinic_id}, manager_id={self.manager_id})"
    
class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    email = Column(String, unique=True)
    job_title = Column(String)
    clinic_id = Column(Integer, ForeignKey('clinics.id'))
    
    clinic = relationship("Clinic", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor")

    def __repr__(self):
        return f"Doctor(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', clinic_id={self.clinic_id})"    
    
class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    year_of_birth = Column(Integer)
    email = Column(String, unique=True)
    phone_number = Column(String)

    appointments = relationship("Appointment", back_populates="patient")

    def __repr__(self):
        return f"Patient(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')" 

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    date = Column(DateTime)
    time = Column(String)

    # Additional attributes
    patient_name = Column(String)
    phone_number = Column(String)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

    def __repr__(self):
        return f"Appointment(id={self.id}, patient_id={self.patient_id}, doctor_id={self.doctor_id}, date='{self.date}', time='{self.time}', patient_name='{self.patient_name}', phone_number='{self.phone_number}')"     

class EmployeeShiftAssociation(Base):
    __tablename__ = 'employee_shift_association'
    employee_id = Column(Integer, ForeignKey('staff.id'), primary_key=True)
    shift_id = Column(Integer, ForeignKey('shifts.id'), primary_key=True)
    
    staff = relationship("Staff", back_populates="employee_associations")
    shift = relationship("Shift", back_populates="employee_associations")

engine = create_engine('sqlite:///clinical.db', echo=True)
Base.metadata.create_all(engine)
