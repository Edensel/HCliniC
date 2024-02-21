import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Clinic, Manager, Staff, Shift, Patient, employee_shift_association

# Create engine and bind to existing database
engine = create_engine('sqlite:///clinical.db')
Base.metadata.bind = engine

# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_patient(args):
    name = input("Enter patient's name: ")
    gender = input("Enter patient's gender: ")
    age = int(input("Enter patient's age: "))
    email = input("Enter patient's email: ")
    phone = input("Enter patient's phone number: ")
    address = input("Enter patient's address: ")

    new_patient = Patient(name=name, gender=gender, age=age, email=email, phone=phone, address=address)
    session.add(new_patient)
    session.commit()
    print("Patient added successfully.")

def add_doctor(args):
    name = input("Enter doctor's name: ")
    specialization = input("Enter doctor's specialization: ")
    email = input("Enter doctor's email: ")
    phone = input("Enter doctor's phone number: ")

    new_doctor = Doctor(name=name, specialization=specialization, email=email, phone=phone)
    session.add(new_doctor)
    session.commit()
    print("Doctor added successfully.")

def add_appointment(args):
    patient_id = input("Enter patient ID: ")
    doctor_id = input("Enter doctor ID: ")
    date = input("Enter appointment date (YYYY-MM-DD): ")
    time = input("Enter appointment time (HH:MM AM/PM): ")

    new_appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date, time=time)
    session.add(new_appointment)
    session.commit()
    print("Appointment added successfully.")

def delete_entity(args):
    entity_type = input("Enter entity type to delete (patient, doctor, appointment): ")
    if entity_type == "patient":
        delete_patient()
    elif entity_type == "doctor":
        delete_doctor()
    elif entity_type == "appointment":
        delete_appointment()
    else:
        print("Invalid entity type.")

def delete_patient():
    patient_id = input("Enter patient ID to delete: ")
    patient = session.query(Patient).filter_by(id=patient_id).first()
    if patient:
        session.delete(patient)
        session.commit()
        print("Patient deleted successfully.")
    else:
        print("Patient not found.")

def delete_doctor():
    doctor_id = input("Enter doctor ID to delete: ")
    doctor = session.query(Doctor).filter_by(id=doctor_id).first()
    if doctor:
        session.delete(doctor)
        session.commit()
        print("Doctor deleted successfully.")
    else:
        print("Doctor not found.")

def delete_appointment():
    appointment_id = input("Enter appointment ID to delete: ")
    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    if appointment:
        session.delete(appointment)
        session.commit()
        print("Appointment deleted successfully.")
    else:
        print("Appointment not found.")

def list_patients(args):
    patients = session.query(Patient).all()
    patient_data = []
    for patient in patients:
        patient_data.append({
            "id": patient.id,
            "name": patient.name,
            "gender": patient.gender,
            "age": patient.age,
            "email": patient.email,
            "phone": patient.phone,
            "address": patient.address
        })
    return patient_data

def list_doctors(args):
    doctors = session.query(Doctor).all()
    doctor_data = []
    for doctor in doctors:
        doctor_data.append({
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization,
            "email": doctor.email,
            "phone": doctor.phone
        })
    return doctor_data

def list_appointments(args):
    appointments = session.query(Appointment).all()
    appointment_data = []
    for appointment in appointments:
        appointment_data.append({
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "date": appointment.date,
            "time": appointment.time
        })
    return appointment_data

def main():
    parser = argparse.ArgumentParser(description="Clinic Management System")

    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # Subcommands for adding entities
    add_patient_parser = subparsers.add_parser("add_patient", help="Add a patient")
    add_patient_parser.set_defaults(func=add_patient)

    add_doctor_parser = subparsers.add_parser("add_doctor", help="Add a doctor")
    add_doctor_parser.set_defaults(func=add_doctor)

    add_appointment_parser = subparsers.add_parser("add_appointment", help="Add an appointment")
    add_appointment_parser.set_defaults(func=add_appointment)

    # Subcommands for deleting entities
    delete_entity_parser = subparsers.add_parser("delete_entity", help="Delete an entity")
    delete_entity_parser.set_defaults(func=delete_entity)

    # Subcommands for listing entities
    list_patients_parser = subparsers.add_parser("list_patients", help="List all patients")
    list_patients_parser.set_defaults(func=list_patients)

    list_doctors_parser = subparsers.add_parser("list_doctors", help="List all doctors")
    list_doctors_parser.set_defaults(func=list_doctors)

    list_appointments_parser = subparsers.add_parser("list_appointments", help="List all appointments")
    list_appointments_parser.set_defaults(func=list_appointments)

    while True:
        print("\nMenu:")
        print("1. Add Patient")
        print("2. Add Doctor")
        print("3. Add Appointment")
        print("4. List Patients")
        print("5. List Doctors")
        print("6. List Appointments")
        print("7. Delete Entity")
        print("0. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            add_patient(None)
        elif choice == "2":
            add_doctor(None)
        elif choice == "3":
            add_appointment(None)
        elif choice == "4":
            patients = list_patients(None)
            for patient in patients:
                print(patient)
            input("Press Enter to continue...")
        elif choice == "5":
            doctors = list_doctors(None)
            for doctor in doctors:
                print(doctor)
            input("Press Enter to continue...")
        elif choice == "6":
            appointments = list_appointments(None)
            for appointment in appointments:
                print(appointment)
            input("Press Enter to continue...")
        elif choice == "7":
            delete_entity(None)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")

if __name__ == "__main__":
    main()
