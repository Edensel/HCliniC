import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Clinic, Manager, Staff, Shift, Patient, Appointment, EmployeeShiftAssociation, Doctor

# Rest of your code


# Create engine and bind to the existing database
engine = create_engine('sqlite:///clinical.db')
Base.metadata.bind = engine

# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_patient(args):
    name = input("Enter patient's name: ")
    gender = input("Enter patient's gender: ")
    year_of_birth = int(input("Enter patient's year of birth: "))
    email = input("Enter patient's email: ")
    phone_number = input("Enter patient's phone number: ")

    new_patient = Patient(
        first_name=name,
        gender=gender,
        year_of_birth=year_of_birth,
        email=email,
        phone_number=phone_number
    )
    session.add(new_patient)
    session.commit()
    print("Patient added successfully.")

def add_doctor(args):
    name = input("Enter doctor's name: ")
    gender = input("Enter doctor's gender: ")
    email = input("Enter doctor's email: ")
    job_title = input("Enter doctor's job title: ")

    new_doctor = Doctor(
        first_name=name,
        gender=gender,
        email=email,
        job_title=job_title
    )
    session.add(new_doctor)
    session.commit()
    print("Doctor added successfully.")

def add_clinic(args):
    name = input("Enter clinic name: ")
    location = input("Enter clinic location: ")

    new_clinic = Clinic(name=name, location=location)
    session.add(new_clinic)
    session.commit()
    print("Clinic added successfully.")

def add_appointment(args):
    patient_id = int(input("Enter patient ID: "))
    doctor_id = int(input("Enter doctor ID: "))
    date = input("Enter appointment date (YYYY-MM-DD): ")
    time = input("Enter appointment time (HH:MM AM/PM): ")
    patient_name = input("Enter patient name: ")
    phone_number = input("Enter patient phone number: ")

    new_appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        date=date,
        time=time,
        patient_name=patient_name,
        phone_number=phone_number
    )
    session.add(new_appointment)
    session.commit()

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
    patient_id = int(input("Enter patient ID to delete: "))
    patient = session.query(Patient).filter_by(id=patient_id).first()
    if patient:
        session.delete(patient)
        session.commit()
        print("Patient deleted successfully.")
    else:
        print("Patient not found.")

def delete_doctor():
    doctor_id = int(input("Enter doctor ID to delete: "))
    doctor = session.query(Doctor).filter_by(id=doctor_id).first()
    if doctor:
        session.delete(doctor)
        session.commit()
        print("Doctor deleted successfully.")
    else:
        print("Doctor not found.")

def delete_appointment():
    appointment_id = int(input("Enter appointment ID to delete: "))
    appointment = session.query(Shift).filter_by(id=appointment_id).first()
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
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "gender": patient.gender,
            "year_of_birth": patient.year_of_birth,
            "email": patient.email,
            "phone_number": patient.phone_number
        })
    print("\nList of Patients:")
    print(patient_data)
    input("Press Enter to continue...")

def list_clinics(args):
    clinics = session.query(Clinic).all()
    clinic_data = []
    for clinic in clinics:
        clinic_data.append({
            "id": clinic.id,
            "name": clinic.name,
            "location": clinic.location,
        })
    print("\nList of Clinics:")
    print(clinic_data)
    input("Press Enter to continue...")

def list_doctors(args):
    doctors = session.query(Doctor).all()
    doctor_data = []
    for doctor in doctors:
        doctor_data.append({
            "id": doctor.id,
            "first_name": doctor.first_name,
            "last_name": doctor.last_name,
            "gender": doctor.gender,
            "email": doctor.email,
            "job_title": doctor.job_title
        })
    print("\nList of Doctors:")
    print(doctor_data)
    input("Press Enter to continue...")

def list_appointments(args):
    appointments = session.query(Shift).all()
    appointment_data = []
    for appointment in appointments:
        appointment_data.append({
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "date": appointment.date,
            "time": appointment.time
        })
    print("\nList of Appointments:")
    print(appointment_data)
    input("Press Enter to continue...")

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

    add_clinic_parser = subparsers.add_parser("add_clinic", help="Add a clinic")
    add_clinic_parser.set_defaults(func=add_clinic)

    while True:
        print("\nMenu:")
        print("1. Add Patient")
        print("2. Add Doctor")
        print("3. Add Appointment")
        print("4. Add Clinic")
        print("5. List Patients")
        print("6. List Doctors")
        print("7. List Appointments")
        print("8. List Clinics")
        print("9. Delete Entity")
        print("0. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            add_patient(None)
        elif choice == "2":
            add_doctor(None)
        elif choice == "3":
            add_appointment(None)
        elif choice == "4":
            add_clinic(None)
        elif choice == "5":
            patients = list_patients(None)
            for patient in patients:
                print("\nList of Patients:")
            input("Press Enter to continue...")
        elif choice == "6":
            doctors = list_doctors(None)
            for doctor in doctors:
                print("\nList of Doctors:")
            input("Press Enter to continue...")
        elif choice == "7":
            appointments = list_appointments(None)
            for appointment in appointments:
                print("\nList of Appointments:")
            input("Press Enter to continue...")
        elif choice == "8":
            clinics = list_clinics(None)
            for clinic in clinics:
                print("\nList of Clinics:")
            input("Press Enter to continue...")
        elif choice == "9":
            delete_entity(None)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")

if __name__ == "__main__":
    main()
