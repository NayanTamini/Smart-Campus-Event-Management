USE EventRegistrationDB;

-- 1. Basic SELECT
SELECT * FROM participant;
SELECT * FROM event;

-- 2. JOIN
SELECT
    p.Participant_Name,
    e.Event_Name,
    r.Registration_Date,
    r.Status
FROM registration r
JOIN participant p
    ON r.Participant_ID = p.Participant_ID
JOIN event e
    ON r.Event_ID = e.Event_ID;

-- 3. Event-wise registration count
SELECT
    e.Event_Name,
    COUNT(r.Registration_ID) AS Total_Registrations
FROM event e
LEFT JOIN registration r
    ON e.Event_ID = r.Event_ID
GROUP BY e.Event_ID, e.Event_Name;

-- 4. Revenue
SELECT
    COALESCE(SUM(Amount),0) AS Total_Revenue
FROM payment
WHERE Payment_Status = 'Paid';

-- 5. View
SELECT * FROM registration_details;

-- 6. Stored Procedure
CALL GetParticipantRegistrations(1);

-- 7. Trigger
SHOW TRIGGERS;

-- 8. Attendance
SELECT
    p.Participant_Name,
    e.Event_Name,
    a.Attendance_Status,
    a.Check_In_Time
FROM attendance a
JOIN registration r
    ON a.Registration_ID = r.Registration_ID
JOIN participant p
    ON r.Participant_ID = p.Participant_ID
JOIN event e
    ON r.Event_ID = e.Event_ID;