import random
from faker import Faker
import mysql.connector
import streamlit as st
from datetime import datetime
db_config = {
    'host': 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
    'user': 'ZyFH9eafC8zpw21.root',
    'password': 'nlNXl13dHcuL7tgs',
    'database': 'Student_Info',
    'port': 4000,
    'ssl_ca': 'C:/Users/jamuna/Downloads/isrgrootx1(1).pem'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
fake = Faker()
def populate(n=500):
    for _ in range(n):
        name = fake.name()
        age = random.randint(18,30)
        gender = random.choice(['Male','Female','Other'])
        email = fake.email()
        phone = fake.numerify('##########')
        enrollment = fake.bothify(text='ENR#####')
        course_batch = f"Batch{random.randint(1,20)}"
        city = fake.city()
        graduation_year = random.randint(2018,2025)

        cursor.execute(
            "INSERT INTO Student_table (name, age, gender, email, phone, enrollment, course_batch, city, graduation_year) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (name, age, gender, email, phone, enrollment, course_batch, city, graduation_year)
        )
        sid = cursor.lastrowid

        cursor.execute(
            "INSERT INTO Programming_table (student_id, language_name, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (sid,
             random.choice(['Python','Java','C++','JavaScript']),
             random.randint(20,200),
             random.randint(1,10),
             random.randint(0,5),
             random.randint(0,3),
             round(random.uniform(40,100),2))
        )

        cursor.execute(
            "INSERT INTO Soft_skills (student_id, communication, team_work, presentation, leadership, critical_thinking, interpersonal_skill) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (sid,
             random.randint(1,10),
             random.randint(1,10),
             random.randint(1,10),
             random.randint(1,10),
             random.randint(1,10),
             random.randint(1,10))
        )

        placed = random.choice([True]*3 + [False])
        print(placed)
        if placed:
            status = 'Placed'
            mock_score = random.randint(60,100)
            internship = True if random.random() < .7 else False
            package = round(random.uniform(3.0,15.0),2)
            rounds = random.randint(1,5)
            date = fake.date_between(start_date='-1y', end_date='today')
            comp = fake.company()
        else:
            status, mock_score, internship, package, rounds, date, comp = (
                'Not Placed', random.randint(10,59), False, 0.0, 0, None, ''
            )

        cursor.execute(
            "INSERT INTO Placement_table (student_id, mock_interview_score, internship_completed, placement_package, placement_status, company_name, interview_rounds_cleared, placement_date) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (sid, mock_score, internship, package, status, comp, rounds, date)
        )

    conn.commit()
if st.sidebar.button("Populate 500 records"):
    populate()
    st.success("Inserted 500 fake students!")
