from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

from db_config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM event")
    total_events = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM participant")
    total_participants = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM registration")
    total_registrations = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COALESCE(SUM(Amount), 0) AS total
        FROM payment
        WHERE Payment_Status = 'Paid'
    """)
    total_revenue = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT
            e.Event_ID,
            e.Event_Name,
            e.Event_Date,
            e.Venue,
            e.Capacity,
            e.Registration_Fee,
            COUNT(r.Registration_ID) AS registered
        FROM event e
        LEFT JOIN registration r
            ON e.Event_ID = r.Event_ID
        GROUP BY
            e.Event_ID,
            e.Event_Name,
            e.Event_Date,
            e.Venue,
            e.Capacity,
            e.Registration_Fee
        ORDER BY e.Event_Date
    """)
    events = cursor.fetchall()

    for event in events:
        event["available"] = event["Capacity"] - event["registered"]

        occupancy = (event["registered"] / event["Capacity"]) * 100

        if occupancy >= 100:
            event["status"] = "Full"
        elif occupancy >= 90:
            event["status"] = "Almost Full"
        elif occupancy >= 70:
            event["status"] = "Filling Fast"
        else:
            event["status"] = "Available"

    cursor.execute("""
        SELECT
            e.Event_Name,
            COUNT(r.Registration_ID) AS registrations
        FROM event e
        LEFT JOIN registration r
            ON e.Event_ID = r.Event_ID
        GROUP BY e.Event_ID, e.Event_Name
        ORDER BY registrations DESC
        LIMIT 1
    """)
    popular_event = cursor.fetchone()

    cursor.execute("""
        SELECT
            Event_Name,
            Event_Date,
            Venue
        FROM event
        WHERE Event_Date >= CURDATE()
        ORDER BY Event_Date
        LIMIT 3
    """)
    upcoming_events = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_events=total_events,
        total_participants=total_participants,
        total_registrations=total_registrations,
        total_revenue=total_revenue,
        events=events,
        popular_event=popular_event,
        upcoming_events=upcoming_events
    )


@app.route("/participants")
def participants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM participant")
    participants = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("participants.html", participants=participants)


@app.route("/participants/add", methods=["POST"])
def add_participant():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    department = request.form["department"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO participant
        (Participant_Name, Email, Phone, Department)
        VALUES (%s, %s, %s, %s)
    """, (name, email, phone, department))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("participants"))


@app.route("/participants/delete/<int:id>")
def delete_participant(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM participant WHERE Participant_ID = %s",
        (id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("participants"))
@app.route("/participants/update/<int:id>", methods=["POST"])
def update_participant(id):
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    department = request.form["department"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE participant
        SET Participant_Name = %s,
            Email = %s,
            Phone = %s,
            Department = %s
        WHERE Participant_ID = %s
    """, (name, email, phone, department, id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("participants"))


@app.route("/participants/edit/<int:id>")
def edit_participant(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM participant WHERE Participant_ID = %s",
        (id,)
    )

    participant = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "edit_participant.html",
        participant=participant
    )

@app.route("/events")
def events():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            e.Event_ID,
            e.Event_Name,
            e.Event_Date,
            e.Venue,
            e.Capacity,
            e.Registration_Fee,
            COUNT(r.Registration_ID) AS registered
        FROM event e
        LEFT JOIN registration r
            ON e.Event_ID = r.Event_ID
        GROUP BY
            e.Event_ID,
            e.Event_Name,
            e.Event_Date,
            e.Venue,
            e.Capacity,
            e.Registration_Fee
        ORDER BY e.Event_Date
    """)

    events = cursor.fetchall()

    for event in events:
        event["available"] = event["Capacity"] - event["registered"]

        event["occupancy"] = round(
            (event["registered"] / event["Capacity"]) * 100,
            1
        )

        if event["occupancy"] >= 100:
            event["status"] = "Full"
        elif event["occupancy"] >= 90:
            event["status"] = "Almost Full"
        elif event["occupancy"] >= 70:
            event["status"] = "Filling Fast"
        else:
            event["status"] = "Available"

    cursor.close()
    conn.close()

    return render_template("events.html", events=events)


@app.route("/attendance")
def attendance():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.Registration_ID,
            p.Participant_Name,
            e.Event_Name,
            e.Event_Date,
            a.Attendance_Status,
            a.Check_In_Time
        FROM registration r
        JOIN participant p
            ON r.Participant_ID = p.Participant_ID
        JOIN event e
            ON r.Event_ID = e.Event_ID
        LEFT JOIN attendance a
            ON r.Registration_ID = a.Registration_ID
        ORDER BY e.Event_Date, p.Participant_Name
    """)

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("attendance.html", records=records)


@app.route("/attendance/update/<int:registration_id>", methods=["POST"])
def update_attendance(registration_id):
    status = request.form["status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    if status == "Present":
        cursor.execute("""
            UPDATE attendance
            SET Attendance_Status = %s,
                Check_In_Time = %s
            WHERE Registration_ID = %s
        """, (status, datetime.now(), registration_id))

    else:
        cursor.execute("""
            UPDATE attendance
            SET Attendance_Status = %s,
                Check_In_Time = NULL
            WHERE Registration_ID = %s
        """, (status, registration_id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("attendance"))  

@app.route("/registrations")
def registrations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.Registration_ID,
            p.Participant_Name,
            e.Event_Name,
            e.Event_Date,
            r.Registration_Date,
            r.Status,
            COALESCE(pay.Payment_Status, 'Not Paid') AS Payment_Status,
            COALESCE(a.Attendance_Status, 'Not Marked') AS Attendance_Status
        FROM registration r
        JOIN participant p
            ON r.Participant_ID = p.Participant_ID
        JOIN event e
            ON r.Event_ID = e.Event_ID
        LEFT JOIN payment pay
            ON r.Registration_ID = pay.Registration_ID
        LEFT JOIN attendance a
            ON r.Registration_ID = a.Registration_ID
        ORDER BY r.Registration_ID DESC
    """)

    registrations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "registrations.html",
        registrations=registrations
    )


@app.route("/payments")
def payments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            py.Payment_ID,
            r.Registration_ID,
            p.Participant_Name,
            e.Event_Name,
            py.Amount,
            py.Payment_Date,
            py.Payment_Status
        FROM payment py
        JOIN registration r
            ON py.Registration_ID = r.Registration_ID
        JOIN participant p
            ON r.Participant_ID = p.Participant_ID
        JOIN event e
            ON r.Event_ID = e.Event_ID
        ORDER BY py.Payment_ID DESC
    """)

    payments = cursor.fetchall()

    cursor.execute("""
        SELECT COALESCE(SUM(Amount), 0) AS total_revenue
        FROM payment
        WHERE Payment_Status = 'Paid'
    """)

    total_revenue = cursor.fetchone()["total_revenue"]

    cursor.close()
    conn.close()

    return render_template(
        "payments.html",
        payments=payments,
        total_revenue=total_revenue
    )

@app.route("/analytics")
def analytics():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            e.Event_Name,
            e.Capacity,
            COUNT(r.Registration_ID) AS registrations,
            COALESCE(SUM(
                CASE
                    WHEN py.Payment_Status = 'Paid'
                    THEN py.Amount
                    ELSE 0
                END
            ), 0) AS revenue
        FROM event e
        LEFT JOIN registration r
            ON e.Event_ID = r.Event_ID
        LEFT JOIN payment py
            ON r.Registration_ID = py.Registration_ID
        GROUP BY
            e.Event_ID,
            e.Event_Name,
            e.Capacity
        ORDER BY registrations DESC
    """)

    event_analytics = cursor.fetchall()

    cursor.execute("""
        SELECT
            p.Participant_Name,
            COUNT(r.Registration_ID) AS registrations
        FROM participant p
        LEFT JOIN registration r
            ON p.Participant_ID = r.Participant_ID
        GROUP BY
            p.Participant_ID,
            p.Participant_Name
        ORDER BY registrations DESC
    """)

    participant_analytics = cursor.fetchall()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_registrations
        FROM registration
    """)

    total_registrations = cursor.fetchone()["total_registrations"]

    cursor.execute("""
        SELECT
            COALESCE(SUM(Amount), 0) AS total_revenue
        FROM payment
        WHERE Payment_Status = 'Paid'
    """)

    total_revenue = cursor.fetchone()["total_revenue"]

    cursor.close()
    conn.close()

    return render_template(
        "analytics.html",
        event_analytics=event_analytics,
        participant_analytics=participant_analytics,
        total_registrations=total_registrations,
        total_revenue=total_revenue
    )
if __name__ == "__main__":
    app.run(debug=True)