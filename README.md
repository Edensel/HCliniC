# Phase 3 Python-CLI-Project



# Clinical Staff Management System (Equity-Afya)

## Description

In the dynamic landscape of healthcare, optimizing clinical operations is paramount for delivering efficient and high-quality patient care. Introducing our Clinical Operations Optimization Platform, meticulously designed to revolutionize workflow management and enhance productivity within medical facilities. Leveraging state-of-the-art technology, including SQLAlchemy, this platform empowers clinics to seamlessly manage their resources, streamline scheduling, and foster collaboration among staff members. With intuitive features and robust functionality, it sets a new standard for clinical efficiency and excellence.

## Minimum Viable Product Features

### Clinic Management
- Empower authorized users to oversee clinic details with ease, including adding, editing, and deleting clinic information. Gain insights into clinic operations through comprehensive lists, displaying managers and staff members associated with each clinic.

### Search and Filter
- Effortlessly locate clinics, managers, and staff members using intuitive search and filter functionalities. Users can refine their searches based on various attributes, such as clinic location or staff specialization.

### Streamlined Shift Management
- Enhance scheduling efficiency by creating, updating, and deleting shift schedules within the platform. Seamlessly assign staff members to shifts, ensuring optimal coverage, and track shift assignments across clinics with ease.

### Manager Empowerment
- Facilitate seamless management of managers with comprehensive CRUD operations. Assign skilled managers to clinics and gain visibility into managerial responsibilities within each clinic.

### Staff Member Management
- Efficiently administer staff members with intuitive CRUD functionalities. Seamlessly assign staff members to clinics based on their expertise, and effortlessly track staff distribution across clinics.

## Project Structure

### `models.py`
- Defines the SQLAlchemy models for the database schema, including `Clinic`, `Manager`, `Staff`, `Shift`, and `Patient`.
- Establishes relationships between entities and defines association tables.

### `commands.py`
- Implements command-line interface (CLI) functionalities for interacting with the database.
- Provides commands for adding, deleting, and listing entities such as patients, doctors, and appointments.

### `generate_faker_data.py`
- Contains functions to generate fake data for testing and populating the database.
- Includes functions for creating fake clinics, managers, staff members, shifts, patients, and employee-shift associations.

## Getting Started

1. Clone the repository: `git clone https://git@github.com:Edensel/HCliniC.git`
2. Install dependencies: `python pipenv install && pipenv shell`
3. Initialize the database: `python models.py`
4. Optionally, populate the database with fake data: `python generate_faker_data.py`
5. Start using the CLI commands to interact with the system: `python commands.py`

## Author

- `Densel Esekon (@Edensel)`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
