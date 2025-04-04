from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade

DATABASE_URL = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5434/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def select_1():
    result = (
        session.query(Student.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return result[1][1]


def select_2(subject_name):
    result = (
        session.query(Student.name, Subject.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id, Subject.name)
        .order_by(desc("avg_grade"))
        .limit(1)
        .first()
    )
    return result


def select_3(subject_name):
    result = (
        session.query(Group.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .select_from(Grade)
        .join(Student, Student.id == Grade.student_id)
        .join(Group, Group.id == Student.group_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name == subject_name)
        .group_by(Group.id)
        .all()
    )
    return result


def select_4():
    result = session.query(func.round(func.avg(Grade.grade), 2)).scalar()
    return result


def select_5(teacher_name):
    result = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return result


def select_6(group_name):
    result = (
        session.query(Student.name)
        .join(Group)
        .filter(Group.name == group_name)
        .all()
    )
    return result


def select_7(group_name, student_name):
    with Session() as session:
        result = (
            session.query(Student.name, Subject.name, Grade.grade)
            .select_from(Grade)
            .join(Grade.student)
            .join(Student.group)
            .join(Grade.subject)
            .filter(Group.name == group_name, Student.name == student_name)
            .all()
        )
        return result


def select_8(teacher_name):
    result = (
        session.query(func.round(func.avg(Grade.grade), 2))
        .select_from(Grade)
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.name == teacher_name)
        .first()
    )
    return result[0] if result else None


def select_9(student_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .distinct()
        .all()
    )
    return result


def select_10(student_name, teacher_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .distinct()
        .all()
    )
    return result


if __name__ == "__main__":
    print(select_1())
    print(select_2("Math"))
    print(select_3("Math"))
    print(select_4())

    teacher = session.query(Teacher).order_by(func.random()).first()
    if teacher:
        print(select_5(teacher.name))
    else:
        print(None)

    print(select_6("Group 1"))
    print(select_7("Group 1", "Victor English"))

    if teacher:
        print(select_8(teacher.name))
    else:
        print(None)

    first_student = session.query(Student.name).first()
    if first_student:
        print(select_9(first_student.name))
    else:
        print(None)

    if first_student and teacher:
        print(select_10(first_student.name,teacher.name))
    else:
        print(None)
