#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_mysqldb import MySQL, MySQLdb
# from flask_restful import Api, Resource
# from flask_cors import CORS
from os import path
import datetime
import pandas as pd

# DATABASE_URL = 'postgresql://patipan_sher43:ccs_tu2022@db:5432/ccs'


# db = SQLAlchemy()
# DB_NAME = "CCS.db"

def create_app():
    app = Flask(__name__)
    # api = Api(app)
    app.config['SECRET_KEY'] = 'DSI324-project'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'fordzaa55'
    app.config['MYSQL_DB'] = 'curriculum_dataset'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://{DATABASE_URL}'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db.init_app(app)
    global mysql
    mysql = MySQL(app)
    # CORS(app)

    from .views import views
    from .auth import auth
    # from . import views, auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # create_database(app)
    add_data(app, mysql)

    return app, mysql

# def create_database(app):
#     if not path.exists('website/'+ DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')

def add_data(app, mysql):
    # from .models import Programs, Subjects, Subject_type, Curriculum_format, Registrations
    with app.app_context():
        ### Programs
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM programs")
        program = cursor.fetchall()
        # program = db.session.query(Programs).count()
        num = len(program)

        if num == 3:  ### Count programs
            pass
        else:
            # dsi = Programs(program_id = 'DSI', program_nameEN = 'Bachelor of Science Program in Data Science and Innovation', program_nameTH = 'หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิทยาศาสตร์และนวัตกรรมข้อมูล', degree_EN = 'Bachelor of Science (Data Science and Innovation)', degree_TH = 'วิทยาศาสตรบัณฑิต (วิทยาศาสตร์และนวัตกรรมข้อมูล)', all_credits = 127)
            # ppe = Programs(program_id = 'PPE', program_nameEN = 'Bachelor of Arts Program in Philosophy, Politics and Economics', program_nameTH = 'หลักสูตรศิลปศาสตรบัณฑิต สาขาวิชาปรัชญา การเมือง และเศรษฐศาสตร์', degree_EN = 'Bachelor of Arts (Philosophy, Politics and Economics)', degree_TH = 'ศิลปศาสตรบัณฑิต (ปรัชญา การเมือง และเศรษฐศาสตร์)', all_credits = 126)
            # si = Programs(program_id = 'SI', program_nameEN = 'Bachelor of Arts Program in Interdisciplinary Studies of Social Science', program_nameTH = 'หลักสูตรศิลปศาสตรบัณฑิต สาขาวิชาสหวิทยาการสังคมศาสตร์', degree_EN = 'Bachelor of Arts (Interdisciplinary Studies of Social Science)', degree_TH = 'ศิลปศาสตรบัณฑิต (สหวิทยาการสังคมศาสตร์)', all_credits = 130)
            # list_program = [dsi,ppe,si]
            list_program = {'program_id' : ['DSI', 'PPE', 'SI'],
                            'program_nameEN': ['Bachelor of Science Program in Data Science and Innovation', 'Bachelor of Arts Program in Philosophy, Politics and Economics', 'Bachelor of Arts Program in Interdisciplinary Studies of Social Science'],
                            'program_nameTH':['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิทยาศาสตร์และนวัตกรรมข้อมูล', 'หลักสูตรศิลปศาสตรบัณฑิต สาขาวิชาปรัชญา การเมือง และเศรษฐศาสตร์', 'หลักสูตรศิลปศาสตรบัณฑิต สาขาวิชาสหวิทยาการสังคมศาสตร์'],
                            'degree_EN' : ['Bachelor of Science (Data Science and Innovation)', 'Bachelor of Arts (Philosophy, Politics and Economics)', 'Bachelor of Arts (Interdisciplinary Studies of Social Science)'],
                            'degree_TH' :['วิทยาศาสตรบัณฑิต (วิทยาศาสตร์และนวัตกรรมข้อมูล)', 'ศิลปศาสตรบัณฑิต (ปรัชญา การเมือง และเศรษฐศาสตร์)', 'ศิลปศาสตรบัณฑิต (สหวิทยาการสังคมศาสตร์)'],
                            'all_credits' :[127,126,130]}
            # for pg in list_program:
            #     db.session.add(pg)
            # db.session.commit()
            for i in range(3):
                cursor.execute("INSERT INTO programs(program_id, program_nameEN, program_nameTH, degree_EN, degree_TH, all_credits) VALUES (%s, %s, %s, %s, %s, %s)", (list_program['program_id'][i], list_program['program_nameEN'][i], list_program['program_nameTH'][i], list_program['degree_EN'][i], list_program['degree_TH'][i], list_program['all_credits'][i]))
                mysql.connection.commit()
            cursor.close()

        ### Subject_type
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM subject_type")
        result = cursor.fetchall()
        # sub_type = db.session.query(Subject_type).count()
        sub_type = len(result)
        if sub_type == 5:
            pass
        else:
            # st1 = Subject_type(subject_type_id=1, subject_type_name='วิชาศึกษาทั่วไป', sub_type_name=None)
            # st2 = Subject_type(subject_type_id=2, subject_type_name='วิชาเฉพาะ', sub_type_name=None)
            # st3 = Subject_type(subject_type_id=3, subject_type_name='วิชาเลือกเสรี', sub_type_name=None)
            # st4 = Subject_type(subject_type_id=4, subject_type_name='ฝึกปฏิบัติงาน', sub_type_name=None)
            # st5 = Subject_type(subject_type_id=5, subject_type_name='วิชาสหกิจศึกษา', sub_type_name=None)
            # list_sub_type = [st1, st2, st3, st4, st5]
            list_sub_type = {'subject_type_id': [1,2,3,4,5],
                            'subject_type_name': ['วิชาศึกษาทั่วไป', 'วิชาเฉพาะ', 'วิชาเลือกเสรี', 'ฝึกปฏิบัติงาน', 'วิชาสหกิจศึกษา'],
                            'sub_type_name': []}
            # for st in list_sub_type:
            #     db.session.add(st)
            # db.session.commit()
            for i in range(5):
                cursor.execute("INSERT INTO subject_type(subject_type_id, subject_type_name) VALUES (%s, %s)", (list_sub_type['subject_type_id'][i], list_sub_type['subject_type_name'][i]))
                mysql.connection.commit()
            cursor.close()

        ### Subjects
        df = pd.read_csv('subjects_text.csv')
        # data = []
        # for l in range(df.shape[0]):
        #     data.append(df.loc[l, :])

        sub_num_file = df.shape[0]
        # sub_num_query = db.session.query(Subjects).count()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM subjects")
        result = cursor.fetchall()
        sub_num_query = len(result)

        if sub_num_query != sub_num_file:
            for i in range(df.shape[0]):
                # if Subjects.query.filter_by(subject_id = df.loc[i,'subject_id']).first() is None:
                #     sub = Subjects(subject_id = df.loc[i,'subject_id'], subject_type_id = int(df.loc[i,'subject_type_id']), subject_name = df.loc[i,'subject_name'], credits = int(df.loc[i,'credits']), havePrerequisite = int(df.loc[i,'havePrerequisite']), prerequisite_id = df.loc[i,'prerequisite_id'])
                #     db.session.add(sub)
                #     db.session.commit()
                cursor.execute("SELECT * FROM subjects WHERE subject_id = %s", (df.loc[i, 'subject_id'], ))
                result = cursor.fetchone()
                if result is None:
                    if df.loc[i,'prerequisite_id'] is None:
                        pre_id = 'None'
                    else:
                        pre_id = df.loc[i,'prerequisite_id']
                    cursor.execute("INSERT INTO subjects(subject_id, subject_type_id, subject_name, credits, havePrerequisite, prerequisite_id) VALUES (%s, %s, %s, %s, %s, %s)", (df.loc[i,'subject_id'], int(df.loc[i,'subject_type_id']), df.loc[i,'subject_name'], int(df.loc[i,'credits']), int(df.loc[i,'havePrerequisite']), pre_id))
                    mysql.connection.commit()
        cursor.close()
        
        ### Curriculum_format
        df = pd.read_csv('curriculum_format-DSI.csv')
        data_curr = []
        for l in range(df.shape[0]):
            data_curr.append([df.iloc[l,0], df.iloc[l,1], df.iloc[l,2], df.iloc[l,3], df.iloc[l,4], df.iloc[l,5]])
        curr_num_file = len(data_curr)
        # curr_num_query = db.session.query(Curriculum_format).count()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM curriculum_format")
        result = cursor.fetchall()
        curr_num_query = len(result)
        if curr_num_query != curr_num_file:
            for i in range(curr_num_query,len(data_curr)):
                item = data_curr[i]
                # curr = Curriculum_format(curriculum_formatID = item[0], program_id = item[1], subject_id = item[2], academic_year = int(item[3]), semester = int(item[4]), all_credits = int(item[5]))
                # db.session.add(curr)
                # db.session.commit()
                cursor.execute("INSERT INTO curriculum_format(curriculum_formatID, program_id, subject_id, academic_year, semester, all_credits) VALUES (%s, %s, %s, %s, %s, %s)", (item[0], item[1], item[2], int(item[3]), int(item[4]), int(item[5])))
                mysql.connection.commit()
        cursor.close()

        ### Registrations
        # regis_count = db.session.query(Registrations).count()

        # if regis_count == 6:
        #     pass
        # else:
        #     r1 = Registrations(registration_id = '0000000001', student_id = '6209656187', subject_id = 'DSI100,DSI200,TU100,TU104,TU108', all_credits = 15, academic_year = 1, semester = 1, section = '650501,650501,650501,650501,650501', timestamp = datetime.date(2019,8,7))
        #     r2 = Registrations(registration_id = '0000000002', student_id = '6209656187', subject_id = 'DSI201,DSI202,DSI203,DSI205,TU101,TU105', all_credits = 18, academic_year = 1, semester = 2, section = '650501,650501,650501,650501,650501,650501', timestamp = datetime.date(2019,11,25))
        #     r3 = Registrations(registration_id = '0000000003', student_id = '6209656187', subject_id = 'DSI204,DSI206,DX312,DX313,EL217,TU101,TU131', all_credits = 21, academic_year = 2, semester = 1, section = '650501,650502,650501,650501,650501,650501,650501', timestamp = datetime.date(2020,7,7))
        #     r4 = Registrations(registration_id = '0000000004', student_id = '6209656187', subject_id = 'BA291,DSI207,DX310,DX311,DX314,PY252,TU107', all_credits = 21, academic_year = 2, semester = 2, section = '650501,650501,650501,650501,650501,650501,650501', timestamp = datetime.date(2020,12,8))
        #     r5 = Registrations(registration_id = '0000000005', student_id = '6209656187', subject_id = 'DSI310,DSI311,DSI312,DSI313,DSI314', all_credits = 15, academic_year = 3, semester = 1, section = '650501,650501,650501,650501,650501', timestamp = datetime.date(2021,7,12))
        #     r6 = Registrations(registration_id = '0000000006', student_id = '6209656187', subject_id = 'DSI320,DSI321,DSI322,DSI323,DSI324', all_credits = 15, academic_year = 3, semester = 2, section = '650501,650501,650501,650501,650501', timestamp = datetime.date(2021,12,1))
        #     list_regis = [r1,r2,r3,r4,r5,r6]
        #     for rg in list_regis:
        #         db.session.add(rg)
        #     db.session.commit()