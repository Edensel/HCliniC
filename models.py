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
    role = Column(String)
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
    role = Column(String)
    clinic_id = Column(Integer, ForeignKey('clinics.id'))
    clinic = relationship("Clinic", back_populates="staff")
    shifts = relationship("Shift", secondary="employee_shift_association", back_populates="staff")

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
    clinic = relationship("Clinic", back_populates="shifts")
    manager_id = Column(Integer, ForeignKey('managers.id'))
    manager = relationship("Manager", back_populates="shifts")
    staff = relationship("Staff", secondary="employee_shift_association", back_populates="shifts")

    def __repr__(self):
        return f"Shift(id={self.id}, name='{self.name}', supervisor='{self.supervisor}')"
    
class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    date_of_birth = Column(DateTime)
    email = Column(String, unique=True)
    phone_number = Column(String)
    address = Column(String)
    medical_history = Column(String)

    def __repr__(self):
        return f"Patient(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')"    

# Association table between Employee and Shift
employee_shift_association = Table(
    'employee_shift_association',
    Base.metadata,
    Column('employee_id', Integer, ForeignKey('staff.id')),
    Column('shift_id', Integer, ForeignKey('shifts.id'))
)

engine = create_engine('sqlite:///clinical.db', echo=True)
Base.metadata.create_all(engine)
