import random
from faker import Faker

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Student, Group, Teacher, Subject, Grade

DATABASE_URL = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5434/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


def seed():

    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)
    session.commit()


    students = []
    for _ in range(50):
        student = Student(
            name=fake.name(),
            group=random.choice(groups)
        )
        students.append(student)
    session.add_all(students)
    session.commit()


    teachers = [Teacher(name=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()


    subjects = []
    subject_names = ["Math", "Biology", "Physics", "History", "Geography", "Chemistry", "English", "PE"]
    for name in random.sample(subject_names, k=8):
        subject = Subject(
            name=name,
            teacher=random.choice(teachers)
        )
        subjects.append(subject)
    session.add_all(subjects)
    session.commit()

    grades = []
    for student in students:
        for subject in subjects:
            for _ in range(random.randint(5, 20)):
                grade = Grade(
                    student_id=student.id,
                    subject_id=subject.id,
                    grade=random.randint(60, 100),
                    date_of=fake.date_between(start_date='-6M', end_date='today')
                )
                grades.append(grade)
    session.add_all(grades)
    session.commit()
    print("Базу даних заповнено!")


if __name__ == "__main__":
    seed()
