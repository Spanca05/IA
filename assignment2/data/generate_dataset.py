import pandas as pd
import random

random.seed(42)

NUM_STUDENTS = 1000

students = []


for student_id in range(1, NUM_STUDENTS + 1):

    # Weekly study time (hours)
    study_time_weekly = round(random.uniform(0, 30), 1)

    # Number of absences
    absences = random.randint(0, 20)

    # Average sleep hours per night
    sleep_hours = round(random.uniform(3, 10), 1)

    # Stress level (1-10)
    stress_level = random.randint(1, 10)

    # Parental support (0-4)
    # 0 = none
    # 4 = very high
    parental_support = random.randint(0, 4)

    # Tutoring
    # 0 = no
    # 1 = yes
    tutoring = random.randint(0, 1)

    # Participation in extracurricular activities
    extracurricular = random.randint(0, 1)


    risk_score = 0


    if study_time_weekly < 4:
        risk_score += 6

    elif study_time_weekly < 8:
        risk_score += 3

    elif study_time_weekly < 12:
        risk_score -= 1

    
    if absences >= 15:
        risk_score += 4

    elif absences >= 8:
        risk_score += 2

    if sleep_hours < 5:
        risk_score += 3

    elif sleep_hours < 6:
        risk_score += 1


    if stress_level > 7:
        risk_score += 3

    elif stress_level > 5:
        risk_score += 1


    if parental_support >= 3:
        risk_score -= 2

    elif parental_support == 2:
        risk_score -= 1

    elif parental_support == 0:
        risk_score += 1


    if tutoring == 1:
        risk_score -= 1

    else:
        risk_score += 1

    
    if extracurricular == 1:
        risk_score -= 1


    noise = random.randint(-3, 3)

    risk_score += noise


    if risk_score >= 6:
        at_risk = 1
    else:
        at_risk = 0
        

    students.append({
        "student_id": student_id,
        "study_time_weekly": study_time_weekly,
        "absences": absences,
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
        "parental_support": parental_support,
        "tutoring": tutoring,
        "extracurricular": extracurricular,
        "at_risk": at_risk
    })


df = pd.DataFrame(students)


df.to_csv("assignment2/data/students_dataset.csv", index=False)

print("Dataset generated successfully!")
print(df.head())
