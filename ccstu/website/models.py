#!/usr/bin/python
# -*- coding: utf-8 -*-
# from . import db
# from datetime import datetime

# class Programs(db.Model):
#     __tablename__ = 'programs'
#     program_id = db.Column(db.String(3), primary_key=True)
#     program_nameEN = db.Column(db.String(200))
#     program_nameTH = db.Column(db.String(200))
#     degree_EN = db.Column(db.String(200))
#     degree_TH = db.Column(db.String(200))
#     all_credits = db.Column(db.Integer)

#     # students = db.relationship("Student")  ## One to Many
#     # users = db.relationship("Users")  ## One to Many
#     # curri_format = db.relationship("Curriculum_format")  ## One to Many

# class Student(db.Model):
#     __tablename__ = 'student'
#     student_id = db.Column(db.String(10), primary_key=True)
#     program_id = db.Column(db.String(3), db.ForeignKey('programs.program_id'))
#     student_nameEN = db.Column(db.String(255))
#     student_nameTH = db.Column(db.String(255))
#     start_year = db.Column(db.Integer)
#     expected_grad = db.Column(db.Integer)
#     student_email = db.Column(db.String(200), unique=True)
#     student_phonenum = db.Column(db.String(10))
#     gender = db.Column(db.String(1))

#     # registrations = db.relationship("Registrations")  ## One to Many

# class Curriculum_format(db.Model):
#     __tablename__ = 'curriculum_format'
#     curriculum_formatID = db.Column(db.String(3), primary_key=True)
#     program_id = db.Column(db.String(3), db.ForeignKey('programs.program_id'))
#     subject_id = db.Column(db.String(500))
#     academic_year = db.Column(db.Integer)
#     semester = db.Column(db.Integer)
#     all_credits = db.Column(db.Integer)


# class Subject_type(db.Model):
#     __tablename__ = 'subject_type'
#     subject_type_id = db.Column(db.Integer, primary_key=True)
#     subject_type_name = db.Column(db.String(100))
#     sub_type_name = db.Column(db.String(100))

#     # subjects_all = db.relationship("Subjects")  ## One to Many

# class Subjects(db.Model):
#     __tablename__ = 'subjects'
#     subject_id = db.Column(db.String(6), primary_key=True)
#     subject_type_id = db.Column(db.Integer, db.ForeignKey('subject_type.subject_type_id'))
#     subject_name = db.Column(db.String(255))
#     credits = db.Column(db.Integer)
#     havePrerequisite = db.Column(db.Integer)
#     prerequisite_id = db.Column(db.String(20))

# class Registrations(db.Model):
#     __tablename__ = 'registrations'
#     registration_id = db.Column(db.String(10), primary_key=True)
#     student_id = db.Column(db.String(10))
#     subject_id = db.Column(db.String(100))
#     all_credits = db.Column(db.Integer)
#     academic_year = db.Column(db.Integer)
#     semester = db.Column(db.Integer)
#     section = db.Column(db.String(100))
#     timestamp = db.Column(db.Date)

#     # student = db.relationship("Student")  ## One to One

# class Academic_result(db.Model):
#     __tablename__ = 'academic_result'
#     academic_result_id = db.Column(db.String(10), primary_key=True)
#     registration_id = db.Column(db.String(10), db.ForeignKey('registrations.registration_id'))
#     grade_result = db.Column(db.String())

#     # registration = db.relationship("Registrations")

# class User(db.Model):
#     __tablename__ = 'user'
#     user_id = db.Column(db.String(7), primary_key=True)
#     program_id = db.Column(db.String(3), db.ForeignKey('programs.program_id'))
#     nameTH = db.Column(db.String(255))
#     nameEN = db.Column(db.String(255))
#     role = db.Column(db.String(100))
#     gender = db.Column(db.String(1))
#     email = db.Column(db.String(200))


#### db.Column(db.DateTime(timezone=True), default=func.now())
#### db.Column(db.Integer, db.ForeignKey('user.id'))
#### notes = db.relationship('Note')
