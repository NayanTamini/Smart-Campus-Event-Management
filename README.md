# Smart Campus Event Management & Registration System

## Project Overview

The Smart Campus Event Management & Registration System is a database-driven web application developed to manage college events, participants, registrations, payments and attendance.

The system uses MySQL as the database and Python Flask for the web application.

## Objectives

- Manage college events efficiently.
- Maintain participant information.
- Manage event registrations.
- Track registration payments.
- Record participant attendance.
- Monitor event capacity and seat availability.
- Analyze event popularity and revenue.
- Demonstrate database concepts such as SQL JOINs, Views, Stored Procedures, Triggers and Transactions.

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- JavaScript
- MySQL Workbench
- Visual Studio Code

## Main Features

### 1. Smart Dashboard
Displays:
- Total Events
- Total Participants
- Total Registrations
- Total Revenue
- Popular Event
- Upcoming Events
- Seat Availability

### 2. Event Management
- Add events
- View events
- Update events
- Delete events
- View registration count
- Calculate occupancy
- Display event status

### 3. Participant Management
- Add participants
- View participants
- Update participant details
- Delete participants

### 4. Registration Management
Displays participant registrations along with:
- Event information
- Registration status
- Payment status
- Attendance status

### 5. Payment Management
- View payment records
- Track payment status
- Calculate total paid revenue

### 6. Attendance Tracking
- Mark participants Present or Absent
- Record check-in time
- View attendance records

### 7. Analytics
- Event-wise registration analysis
- Event-wise revenue
- Participant registration activity
- Total registrations
- Total revenue

## Database Tables

The system contains the following tables:

1. participant
2. event
3. organizer
4. event_organizer
5. registration
6. payment
7. attendance

## Database Concepts Demonstrated

### Primary Keys
Each major entity has a unique primary key.

### Foreign Keys
Foreign keys maintain relationships between participants, events, registrations, payments and attendance.

### Normalization
The database is designed using normalized tables to reduce data redundancy and maintain data integrity.

### SQL JOINs
JOIN queries combine information from multiple related tables.

### View

`registration_details` provides combined participant and event registration information.

### Stored Procedure

`GetParticipantRegistrations` retrieves registration details for a particular participant.

### Trigger

`check_event_capacity` checks event capacity before allowing a new registration.

### Transaction

Registration and payment operations demonstrate transaction management using COMMIT.

## Project Structure

```text
Event-Registration-System/
│
├── app.py
├── requirements.txt
├── README.md
├── ER_Diagram.png
│
├── database/
│   ├── schema.sql
│   ├── sample_data.sql
│   └── queries.sql
│
├── templates/
│   ├── dashboard.html
│   ├── index.html
│   ├── events.html
│   ├── edit_event.html
│   ├── participants.html
│   ├── edit_participant.html
│   ├── registrations.html
│   ├── payments.html
│   ├── attendance.html
│   └── analytics.html
│
├── static/
│   └── css/
│       └── style.css
│
└── screenshots/