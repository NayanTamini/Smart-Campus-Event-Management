USE EventRegistrationDB;

-- PARTICIPANT DATA
INSERT INTO participant
(Participant_Name, Email, Phone, Department)
VALUES
('Nayan Bhusari', 'nayan@gmail.com', '9876543210', 'Information Technology'),
('Amit Sharma', 'amit@gmail.com', '9876543211', 'Computer Science'),
('Sneha Patil', 'sneha@gmail.com', '9876543212', 'Electronics'),
('Rahul Verma', 'rahul@gmail.com', '9876543213', 'Information Technology'),
('Priya Joshi', 'priya@gmail.com', '9876543214', 'Mechanical');


-- EVENT DATA
INSERT INTO event
(Event_Name, Event_Date, Venue, Capacity, Registration_Fee)
VALUES
('Tech Fest 2026', '2026-10-10', 'Main Auditorium', 100, 200),
('Coding Competition', '2026-10-18', 'Computer Lab', 50, 100),
('Web Development Workshop', '2026-10-25', 'Seminar Hall', 60, 150),
('AI Seminar', '2026-11-05', 'Conference Hall', 80, 250),
('Sports Day', '2026-11-15', 'College Ground', 150, 50);


-- ORGANIZER DATA
INSERT INTO organizer
(Organizer_Name, Email)
VALUES
('Nayan Bhusari', 'nayan.organizer@gmail.com'),
('Rohit Deshmukh', 'rohit.organizer@gmail.com'),
('Kavya Kulkarni', 'kavya.organizer@gmail.com');


-- EVENT ORGANIZER DATA
INSERT INTO event_organizer
(Event_ID, Organizer_ID)
VALUES
(1, 1),
(1, 2),
(2, 2),
(3, 1),
(4, 3),
(5, 3);


-- REGISTRATION DATA
INSERT INTO registration
(Participant_ID, Event_ID, Registration_Date, Status)
VALUES
(1, 1, '2026-09-30', 'Registered'),
(1, 3, '2026-09-30', 'Registered'),
(2, 1, '2026-09-29', 'Registered'),
(3, 2, '2026-09-28', 'Registered'),
(4, 4, '2026-09-27', 'Registered'),
(5, 5, '2026-09-26', 'Registered'),
(1, 2, CURDATE(), 'Registered');


-- PAYMENT DATA
INSERT INTO payment
(Registration_ID, Amount, Payment_Date, Payment_Status)
VALUES
(1, 200, '2026-09-30', 'Paid'),
(2, 150, '2026-09-30', 'Paid'),
(3, 200, '2026-09-29', 'Paid'),
(4, 100, '2026-09-28', 'Pending'),
(5, 250, '2026-09-27', 'Paid'),
(6, 50, '2026-09-26', 'Pending'),
(7, 100, CURDATE(), 'Paid');


-- ATTENDANCE DATA
INSERT INTO attendance
(Registration_ID, Attendance_Status, Check_In_Time)
VALUES
(1, 'Present', '2026-10-10 09:30:00'),
(2, 'Present', '2026-10-25 10:00:00'),
(3, 'Absent', NULL),
(4, 'Present', '2026-10-18 09:45:00'),
(5, 'Present', '2026-11-05 10:15:00'),
(6, 'Absent', NULL),
(7, 'Present', '2026-10-18 09:50:00');