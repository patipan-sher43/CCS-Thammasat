#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort, jsonify
from website.auth import login_is_required
from . import mysql
from flask_mysqldb import MySQLdb
import ast
# from .models import *
# from . import db
import json, os
import datetime
import decimal
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import numpy as np

views = Blueprint('views', __name__)


# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'

@views.route('/')
def home_page():
    return render_template('home_all.html')

@views.route('/api-service', methods=['GET', 'POST'])
def api_page():
    return render_template('api_page.html')

@views.route('/api-service/<variable>')
def api_page_result(variable):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    choice = variable.split('-')

    if choice[1] == 'subjects':
        if choice[0] == 'ALL':
            cursor.execute("SELECT credits, prerequisite_id, subject_id, subject_name FROM subjects")
            result = cursor.fetchall()
        else:
            DSI_list = ('TU050','TU100','TU108','TU104','DSI100','DSI200','TU107','TU105','TU106','DSI201','DSI202','DSI204','DSI205','TU101','TU131','DSI203','DSI206','DX312','DX313','EL217','DSI207','DX310','DX311','DX314','BA291','PY252','DSI310','DSI311','DSI312','DSI313','DSI314','DSI320','DSI321','DSI322','DSI323','DSI324','DSI380','DSI430','DSI431','DSI432','DSI433','DSI434','DSI440','DSI441','DSI442','DSI443','DSI444','DSI450','DSI451','DSI452','DSI453','DSI454','DSI460','DSI461','DSI462','DSI463','DSI464','DSI470','DSI471','DSI472','DSI473','DSI474','DSI480')
            PPE_list = ('TU100','TU101','TU102','TU103','IP100','IP101','TU104','TU105','TU106','IP102','IP103','TU121','TU124','TU111','TU112','TU115','TU117','TU131','TU142','TU143','TU151','TU153','TU155','TH162','CH171','FR070','JP171','RS171','GR171','SP171','AS171','AS173','AS175','AS177','AS179','AS181','AS183','FL171','FL172','TU121','TU124','TU111','TU112','TU115','TU117', 'TU131', 'TU142', 'TU143', 'TU151', 'TU153', 'TU155', 'TH162', 'CH171', 'CH172', 'FR070', 'FR171', 'FR172', 'JP171', 'JP172', 'RS171', 'RS172', 'GR171', 'GR172', 'SP171', 'SP172', 'AS171', 'AS172', 'AS173', 'AS174', 'AS175', 'AS176', 'AS177', 'AS178', 'AS179', 'AS180', 'AS181', 'AS182', 'AS183', 'AS184', 'EL171', 'EL172')
            SI_list = ('TU050','TU105','TU104','TU100','TU101','TU109','TU102','TU108','TU103','TU107','TU106','TU111','TU116','TU117','TU121','TU122','TU124','TU143','TU156','AS125')
            if choice[0] == 'DSI':
                cursor.execute(f"SELECT credits, prerequisite_id, subject_id, subject_name FROM subjects WHERE subject_id IN {DSI_list}")
                result = cursor.fetchall()
            elif choice[0] == 'PPE':
                cursor.execute(f"SELECT credits, prerequisite_id, subject_id, subject_name FROM subjects WHERE subject_id IN {PPE_list}")
                result = cursor.fetchall()
            elif choice[0] == 'SI':
                cursor.execute(f"SELECT credits, prerequisite_id, subject_id, subject_name FROM subjects WHERE subject_id IN {SI_list} or subject_id LIKE '{choice[0]}%'")
                result = cursor.fetchall()
    elif choice[1] == 'students':
        if choice[0] == 'ALL':
            cursor.execute("SELECT student_id FROM student")
            result = cursor.fetchall()
        else:
            cursor.execute("SELECT student_id FROM student WHERE program_id = %s", (choice[0],))
            result = cursor.fetchall()
    else:
        cursor.execute("SELECT subject_id, academic_year, all_credits, semester FROM curriculum_format WHERE program_id = %s", (choice[0],))
        result = cursor.fetchall()

    return jsonify(result)

@views.route('/terms-api', methods=['GET','POST'], endpoint='terms-api')
def terms_api_page():
    if request.method == 'POST':
        check = request.form.get('terms')
        if check == 'checked':
            return redirect(url_for('views.api_page'))
        else:
            flash('กรุณายอมรับเงื่อนไข ก่อนทำการกดยืนยัน', category='error')
    return render_template('terms_api_page.html')

@views.route('/student/home', methods=['GET', 'POST'], endpoint='student')
@login_is_required
def student_home():
    
    image = session["picture"]

    # student = Student.query.filter_by(student_email = session["email"]).first()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM student WHERE student_email = %s", (session["email"],))
    student = cursor.fetchone()
    cursor.close()

    # if student.gender == 'M':
    #     gender = 'ชาย'
    # elif student.gender == 'F':
    #     gender = 'หญิง'
    # else:
    #     gender = 'อื่นๆ'
    
    if student['gender'] == 'M':
        gender = 'ชาย'
    elif student['gender'] == 'F':
        gender = 'หญิง'
    else:
        gender = 'อื่นๆ'

    return render_template("home.html", result = student, gender = gender, image = image)

@views.route('/student/edit', methods=['GET', 'POST'])
def student_edit_info():
    # student = Student.query.filter_by(student_email = session['email']).first()

    if request.method == 'POST':
        NameTH = request.form.get('NameTH')
        NameEN = request.form.get('NameEN')
        gender = request.form.get('genderchoose')
        phone_number = request.form.get('phonenumber')
        email = session["email"]

        if len(NameTH) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        elif len(NameEN) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        else:
            ### Update user to database
            # student.student_id = student.student_id
            # student.program_id = student.program_id
            # student.student_nameEN = NameEN
            # student.student_nameTH = NameTH
            # student.gender = gender
            # student.student_phonenum = phone_number
            # student.start_year = student.start_year
            # student.expected_grad = student.expected_grad
            # student.student_email = email

            # db.session.add(student)
            # db.session.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE student SET student_nameEN= %s, student_nameTH= %s, student_email= %s, student_phonenum= %s, gender= %s WHERE student_email = %s", (NameEN, NameTH, email, phone_number, gender, session["email"]))
            mysql.connection.commit()
            cursor.close()

            flash('แก้ไขข้อมูลสำเร็จ!.', category='success')
            return redirect(url_for('views.student'))
    return render_template('student_home_edit.html')

@views.route('/student/curriculum', methods=['GET', 'POST'])
def curriculum_page():
    # result = Student.query.filter_by(student_email = session["email"]).first()
    # start_year = result.start_year

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM student WHERE student_email = %s", (session["email"],))
    result = cursor.fetchone()  
    start_year = result['start_year']

    semester_result = None
    subject_list = None
    subject_item = None
    subject_dict = None
    sub_sem_list = None
    section_list = None
    if request.method == 'POST':
        semester = request.form.get("academic-year")
        sem_list = semester.split('/')
    
        # semester_result = Registrations.query.filter_by(student_id = result.student_id, semester = int(sem_list[1]), academic_year = int(sem_list[0])).first()
        cursor.execute("SELECT * FROM registrations WHERE student_id = %s and semester = %s and academic_year = %s", (result['student_id'], int(sem_list[1]), int(sem_list[0])))
        semester_result = cursor.fetchone()

        if semester_result is not None:
            # subject_list = semester_result.subject_id.split(',')
            subject_list = semester_result['subject_id'].split(',')
           
            subject_dict = {}
            for i in subject_list:
                # subject_item = Subjects.query.filter_by(subject_id = i).first()
                # subject_dict[i] = [subject_item.subject_name, subject_item.credits]

                cursor.execute("SELECT * FROM subjects WHERE subject_id = %s", (i,))
                subject_item = cursor.fetchone()
                subject_dict[i] = [subject_item['subject_name'], subject_item['credits']]

            # section_list = semester_result.section.split(',')
            section_list = semester_result['section'].split(',')

            if result['program_id'] == 'DSI':
                curri_format_id = 'D' + sem_list[0] + sem_list[1]
                # sub_sem_list = Curriculum_format.query.filter_by(curriculum_formatID = curri_format_id).first()
                cursor.execute("SELECT * FROM curriculum_format WHERE curriculum_formatID = %s", (curri_format_id,))
                sub_sem_list = cursor.fetchone()
            elif result['program_id'] == 'PPE':
                curri_format_id = 'P' + sem_list[0] + sem_list[1]
                cursor.execute("SELECT * FROM curriculum_format WHERE curriculum_formatID = %s", (curri_format_id,))
                sub_sem_list = cursor.fetchone()
    else: 
        semester = "..."

    return render_template('student_curriculum.html', semester = semester, start_year = start_year, sem_result = semester_result, subject_list = subject_list, subject_dict = subject_dict, sub_sem_list = sub_sem_list, section = section_list)



@views.route('/student/test-regis', methods=['GET', 'POST'])
def student_test_regis():
    # result = Student.query.filter_by(student_email = session['email']).first()
    # start_year = result.start_year

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM student WHERE student_email = %s", (session["email"],))
    result = cursor.fetchone()
    start_year = result['start_year']

    final_match, acad_year, semester, result_curr_format, list_final_match = None, None, None, None, None
    if request.method == 'POST':
        form_result = request.form.get('academic-year').split('/')
        
        semester, acad_year = form_result[0], form_result[1]
        sub_list = []
        correct_sub = True

        final_match = None

        form_sub = [request.form.get('s1'), request.form.get('s2'), request.form.get('s3'),
                    request.form.get('s4'), request.form.get('s5'), request.form.get('s6'),
                    request.form.get('s7'), request.form.get('s8'), request.form.get('s9')]

        for i in form_sub:
            if i != 'None':
                if len(i) < 5:
                    correct_sub = False
                else:
                    sub_list.append(i)
        if correct_sub:
            if result['program_id'] == 'DSI':
                curri_format_id = 'D' + semester
                module4 = request.form.get('module')

                cursor.execute('SELECT * FROM curriculum_format WHERE curriculum_formatID = %(id)s', {'id': curri_format_id})
                result_curr_format = cursor.fetchone()

                # result_curr_format = Curriculum_format.query.filter_by(curriculum_formatID = curri_format_id).first()

                final_match = None
                if result_curr_format is not None:
                    if curri_format_id != 'D41' and module4 == 'None':
                        final_match = {}
                        for sub in sub_list:
                            if sub in result_curr_format['subject_id']:
                                final_match[sub] = 'ลงถูกต้องตามแผนการเรียน'
                            else:
                                if curri_format_id == 'D22' and (sub == 'BA291' or sub == 'PY252'):
                                    final_match[sub] = 'ลงถูกต้องตามแผนการเรียน (วิชาเลือกเสรี)'
                                else:
                                    final_match[sub] = 'ลงผิดลำดับ / ล่าช้า'
                        list_final_match = list(final_match.keys())
                    elif curri_format_id != 'D41' and module4 != 'None':
                        flash(f'ไม่สามารถลงทะเบียนได้ เนื่องจากภาคเรียนที่ {semester[1]}/{acad_year} ไม่มีการเลือกหมวดวิชา! กรุณาระบุช่องเลือกหมวดวิชาเป็น "ไม่มี"', category='error')
                    else:
                        final_match = {}
                        dict_module = ast.literal_eval(result_curr_format['subject_id'])
                        if module4 != 'None':
                            for sub in sub_list:
                                if sub in dict_module[module4]:
                                    final_match[sub] = 'ลงถูกต้องตามแผนการเรียน'
                                else:
                                    final_match[sub] = 'ลงผิดลำดับ / ล่าช้า'
                            list_final_match = list(final_match.keys())
                        else:
                            flash(f'กรุณาเลือกหมวดวิชาที่จะลงทะเบียนในภาคเรียนที่ 1/{acad_year}', category='error')
                else:
                    flash('ไม่พบข้อมูล!', category='error')
            elif result['program_id'] == 'PPE':
                curri_format_id = 'S' + semester
                cursor.execute('SELECT * FROM curriculum_format WHERE curriculum_formatID = %(id)s', {'id': curri_format_id})
                result_curr_format = cursor.fetchone()

                final_match = None
                if result_curr_format is not None:
                    final_match = {}
                    for sub in sub_list:
                        if sub in result_curr_format['subject_id']:
                            final_match[sub] = 'ลงถูกต้องตามแผนการเรียน'
                        else:
                            final_match[sub] = 'ลงผิดลำดับ / ล่าช้า / วิชาเลือกเสรี'
                    list_final_match = list(final_match.keys())
        else:
            flash('รหัสวิชาต้องมีความยาว 5 ตัวขึ้นไป และต้องลงอย่างน้อย 1 วิชา', category='error')

    return render_template('student_test_regis.html', start_year = start_year, final_match = final_match, academic_year = acad_year, semester = semester, result_format = result_curr_format, idx = list_final_match, program = result['program_id'])

@views.route('/student/add', methods=['GET', 'POST'])
def student_add_subject():
    # student = Student.query.filter_by(student_email = session["email"]).first()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM student WHERE student_email = %s", (session["email"],))
    student = cursor.fetchone()

    acad_year, semester = None,None
    if request.method == 'POST':
        form_result = request.form.get('academic-year').split('/')
        module4 = None
        if student['program_id'] == 'DSI':
            module4 = request.form.get('module')
        semester, acad_year = form_result[0], form_result[1]
        sub_list = {}
        section_set = ['650501', '650502']

        #### Check if form invalid
        correct_sub, None_sub = True, False
        correct_sec, None_sec = True, False
        null_val = False

        # final_match = None

        form_sub = [[request.form.get('s1'), request.form.get('c1')], [request.form.get('s2'), request.form.get('c2')], [request.form.get('s3'), request.form.get('c3')],
                    [request.form.get('s4'), request.form.get('c4')], [request.form.get('s5'), request.form.get('c5')], [request.form.get('s6'), request.form.get('c6')],
                    [request.form.get('s7'), request.form.get('c7')], [request.form.get('s8'), request.form.get('c8')], [request.form.get('s9'), request.form.get('c9')]]

        for i in form_sub:
            if i[0] == "" and i[1] == "":
                null_val = True
                break
            elif i[0] != 'None' and i[1] != 'None':
                if len(i[0]) < 5:
                    correct_sub = False
                elif len(i[1]) < 6:
                    correct_sec = False
                else:
                    sub_list[i[0]] = i[1]
            elif i[0] == 'None' and i[1] != 'None':
                None_sub = True
            elif i[1] == 'None' and i[0] != 'None':
                None_sec = True
            
        if null_val:
            flash('กรุณาระบุอย่างน้อย 1 วิชา', category='error')
        elif correct_sub and correct_sec and None_sub == False and None_sec == False:
            if student['program_id'] == 'DSI':
                if module4 == 'None' and semester != '41':
                    ##### Collect credits from all subjects
                    credits = 0
                    wrong_sub, wrong_cd = [], []
                    for k,v in sub_list.items():
                        # subject = Subjects.query.filter_by(subject_id = k).first()

                        cursor.execute("SELECT * FROM subjects WHERE subject_id = %s", (k,))
                        subject = cursor.fetchone()

                        if subject is not None and v in section_set:
                            # credits += subject.credits
                            credits += subject['credits']
                        else:
                            if subject is None:
                                wrong_sub.append(k)
                            else:
                                wrong_cd.append(v)

                    if wrong_sub != []:
                        flash(f'วิชา {wrong_sub[0]} ไม่พบในฐานข้อมูลรายวิชา! โปรดกรอกรหัสวิชาใหม่อีกครั้ง', category='error')
                    elif wrong_cd != []:
                        flash(f'รหัสกลุ่มเรียน {wrong_cd[0]} ไม่พบในฐานข้อมูล! โปรดกรอกกลุ่มเรียนใหม่อีกครั้ง', category='error')
                    else:
                        ##### Convert to text : subject_id
                        text_sub = ""
                        text_sec = ""
                        for k,v in sub_list.items():
                            text_sub = text_sub + k + ","
                            text_sec = text_sec + v + ","

                        text_sub, text_sec = text_sub[:-1], text_sec[:-1]

                        # check_regis = Registrations.query.filter_by(academic_year = int(semester[0]), semester = int(semester[1])).first()

                        cursor.execute("SELECT * FROM registrations WHERE academic_year = %s and semester = %s", (int(semester[0]), int(semester[1])))
                        check_regis = cursor.fetchone()

                        if check_regis is None:
                            # last_item = Registrations.query.all()
                            cursor.execute("SELECT * FROM registrations")
                            last_item = cursor.fetchall()
                            # if last_item != []:
                            #     num = int(last_item[-1].registration_id) + 1
                            #     regis_id = '0'*(10-len(str(num))) + str(num)
                            #     curr = Registrations(registration_id = regis_id, student_id = student.student_id, subject_id = text_sub, all_credits = credits, academic_year = semester[0], semester = semester[1], section = text_sec, timestamp = datetime.datetime.now().date())
                            #     db.session.add(curr)
                            #     db.session.commit()
                            #     flash('บันทึกข้อมูลสำเร็จ! คุณสามารถเช็คข้อมูลการลงทะเบียนที่เพิ่มล่าสุดได้ที่เมนู "ข้อมูลการลงทะเบียน"', category='success')
                            if last_item is not None:
                                num = int(len(last_item)) + 1
                                regis_id = '0'*(10-len(str(num))) + str(num)
                                cursor.execute("INSERT INTO registrations(registration_id, student_id, subject_id, all_credits, academic_year, semester, section, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (regis_id, student['student_id'], text_sub, credits, semester[0], semester[1], text_sec, datetime.datetime.now().date()))
                                mysql.connection.commit()
                                flash('บันทึกข้อมูลสำเร็จ! คุณสามารถเช็คข้อมูลการลงทะเบียนที่เพิ่มล่าสุดได้ที่เมนู "ข้อมูลการลงทะเบียน"', category='success')
                            else:
                                # curr = Registrations(registration_id = '0000000001', student_id = student.student_id, subject_id = text_sub, all_credits = credits, academic_year = semester[0], semester = semester[1], section = text_sec, timestamp = datetime.datetime.now().date())
                                # db.session.add(curr)
                                # db.session.commit()

                                cursor.execute("INSERT INTO registrations(registration_id, student_id, subject_id, all_credits, academic_year, semester, section, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", ('0000000001', student['student_id'], text_sub, credits, semester[0], semester[1], text_sec, datetime.datetime.now().date()))
                                mysql.connection.commit()
                                flash('บันทึกข้อมูลสำเร็จ! คุณสามารถเช็คข้อมูลการลงทะเบียนที่เพิ่มล่าสุดได้ที่เมนู "ข้อมูลการลงทะเบียน"', category='success')
                        else:
                            # flash('ไม่สามารถเพิ่มรายวิชาในภาคการศึกษาซ้ำได้!', category='error')
                            # check_regis.registration_id = check_regis.registration_id
                            # check_regis.student_id = check_regis.student_id
                            # check_regis.subject_id = text_sub
                            # check_regis.all_credits = credits
                            # check_regis.academic_year = int(semester[0])
                            # check_regis.semester = int(semester[1])
                            # check_regis.section = text_sec
                            # check_regis.timestamp = datetime.datetime.now().date()

                            # db.session.add(check_regis)
                            # db.session.commit()

                            cursor.execute("UPDATE registrations SET registration_id = %s, student_id = %s, subject_id = %s, all_credits = %s, academic_year = %s, semester = %s, section = %s, timestamp = %s", (check_regis['registration_id'], check_regis['student_id'], text_sub, credits, semester[0], semester[1], text_sec, datetime.datetime.now().date()))
                            mysql.connection.commit()
                            flash('บันทึกข้อมูลสำเร็จ! คุณสามารถเช็คข้อมูลการลงทะเบียนที่เพิ่มล่าสุดได้ที่เมนู "ข้อมูลการลงทะเบียน"', category='success')
                        cursor.close()

                elif semester != '41' and module4 != 'None':
                        flash(f'ไม่สามารถเพิ่มรายวิชาได้ เนื่องจากภาคเรียนที่ {semester[1]}/{acad_year} ไม่มีการเลือกหมวดวิชา! กรุณาระบุช่องเลือกหมวดวิชาเป็น "ไม่มี"', category='error')
                else:
                    pass
            elif student['program_id'] == 'PPE':
                ##### Collect credits from all subjects
                credits = 0
                wrong_sub, wrong_cd = [], []
                for k,v in sub_list.items():
                    # subject = Subjects.query.filter_by(subject_id = k).first()

                    cursor.execute("SELECT * FROM subjects WHERE subject_id = %s", (k,))
                    subject = cursor.fetchone()

                    if subject is not None and v in section_set:
                        # credits += subject.credits
                        credits += subject['credits']
                    else:
                        if subject is None:
                            wrong_sub.append(k)
                        else:
                            wrong_cd.append(v)

                if wrong_sub != []:
                    flash(f'วิชา {wrong_sub[0]} ไม่พบในฐานข้อมูลรายวิชา! โปรดกรอกรหัสวิชาใหม่อีกครั้ง', category='error')
                elif wrong_cd != []:
                    flash(f'รหัสกลุ่มเรียน {wrong_cd[0]} ไม่พบในฐานข้อมูล! โปรดกรอกกลุ่มเรียนใหม่อีกครั้ง', category='error')
                else:
                    ##### Convert to text : subject_id
                    text_sub = ""
                    text_sec = ""
                    for k,v in sub_list.items():
                        text_sub = text_sub + k + ","
                        text_sec = text_sec + v + ","

                    text_sub, text_sec = text_sub[:-1], text_sec[:-1]

                    # check_regis = Registrations.query.filter_by(academic_year = int(semester[0]), semester = int(semester[1])).first()

                    cursor.execute("SELECT * FROM registrations WHERE academic_year = %s and semester = %s", (int(semester[0]), int(semester[1])))
                    check_regis = cursor.fetchone()

                    if check_regis is None:
                        # last_item = Registrations.query.all()
                        cursor.execute("SELECT * FROM registrations")
                        last_item = cursor.fetchall()

                        if last_item is not None:
                            num = int(len(last_item)) + 1
                            regis_id = '0'*(10-len(str(num))) + str(num)
                            cursor.execute("INSERT INTO registrations(registration_id, student_id, subject_id, all_credits, academic_year, semester, section, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (regis_id, student['student_id'], text_sub, credits, semester[0], semester[1], text_sec, datetime.datetime.now().date()))
                            mysql.connection.commit()
                            flash('บันทึกข้อมูลสำเร็จ! คุณสามารถเช็คข้อมูลการลงทะเบียนที่เพิ่มล่าสุดได้ที่เมนู "ข้อมูลการลงทะเบียน"', category='success')
                        else:
                            cursor.execute("INSERT INTO registrations(registration_id, student_id, subject_id, all_credits, academic_year, semester, section, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", ('0000000001', student['student_id'], text_sub, credits, semester[0], semester[1], text_sec, datetime.datetime.now().date()))
                            mysql.connection.commit()
                            flash('บันทึกข้อมูลสำเร็จ! คุณสามารถเช็คข้อมูลการลงทะเบียนที่เพิ่มล่าสุดได้ที่เมนู "ข้อมูลการลงทะเบียน"', category='success')
                    else:
                        cursor.execute("UPDATE registrations SET registration_id = %s, student_id = %s, subject_id = %s, all_credits = %s, academic_year = %s, semester = %s, section = %s, timestamp = %s", (check_regis['registration_id'], check_regis['student_id'], text_sub, credits, semester[0], semester[1], text_sec, datetime.datetime.now().date()))
                        mysql.connection.commit()
                        flash('บันทึกข้อมูลสำเร็จ! คุณสามารถเช็คข้อมูลการลงทะเบียนที่เพิ่มล่าสุดได้ที่เมนู "ข้อมูลการลงทะเบียน"', category='success')
                    cursor.close()
        
        elif correct_sub == False:
            flash('รหัสวิชาต้องมีความยาว 5 ตัวขึ้นไป', category='error')
        elif correct_sec == False:
            flash('รหัสกลุ่มเรียนต้องมีความยาว 6 ตัว', category='error')
        elif None_sub:
            flash('ไม่สามารถเพิ่มรายวิชาได้ เนื่องจากมีการระบุกลุ่มเรียน แต่ไม่มีการระบุรหัสวิชา!', category='error')
        elif None_sec:
            flash('ไม่สามารถเพิ่มรายวิชาได้ เนื่องจากมีการระบุรหัสวิชา แต่ไม่มีการระบุกลุ่มเรียนของวิชานั้น!', category='error')
        
    return render_template('student_add_subject.html', start_year = student['start_year'], program = student['program_id'])

#----------------------------------------------------------#

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']

@views.route('/user/home', methods=['GET', 'POST'], endpoint='user_em')
@login_is_required
def user_em_home():
    
    image = session["picture"]
    # user = User.query.filter_by(email = session["email"]).first()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user WHERE email = %s", (session["email"],))
    user = cursor.fetchone()
    cursor.close()

    # if user.gender == 'M':
    #     gender = 'ชาย'
    # elif user.gender == 'F':
    #     gender = 'หญิง'
    # else:
    #     gender = 'อื่นๆ'

    if user['gender'] == 'M':
        gender = 'ชาย'
    elif user['gender'] == 'F':
        gender = 'หญิง'
    else:
        gender = 'อื่นๆ'
    
    return render_template("user_em_home.html", result = user, gender = gender, image = image)

@views.route('/user/edit', methods=['GET', 'POST'], endpoint='user_em_edit')
@login_is_required
def user_em_edit_info():
    # user = User.query.filter_by(email = session['email']).first()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        NameTH = request.form.get('NameTH')
        NameEN = request.form.get('NameEN')
        gender = request.form.get('genderchoose')

        if len(NameTH) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        elif len(NameEN) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        else:
            ### Update user to database
            # user.user_id = user.user_id
            # user.program_id = user.program_id
            # user.nameTH = NameTH
            # user.nameEN = NameEN
            # user.role = user.role
            # user.gender = gender
            # user.email = session['email']

            # db.session.add(user)
            # db.session.commit()

            cursor.execute("UPDATE user SET nameEN= %s, nameTH= %s, gender= %s WHERE email = %s", (NameEN, NameTH, gender, session["email"]))
            mysql.connection.commit()
            cursor.close()
            flash('แก้ไขข้อมูลสำเร็จ!.', category='success')
            return redirect(url_for('views.user_em'))

    return render_template('user_em_home_edit.html')


@views.route('/user/check', methods=['GET', 'POST'], endpoint='user_em_check')
def user_em_check_student_page():
    Not_found = False
    # user = User.query.filter_by(email = session['email']).first()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user WHERE email = %s", (session["email"],))
    user = cursor.fetchone()
    # student = Student.query.filter_by(program_id = user.program_id).all()
    cursor.execute("SELECT * FROM student WHERE program_id = %s", (user['program_id'],))
    student = cursor.fetchall()
    minus_year = datetime.datetime.now().year + 543 if datetime.datetime.now().day >= 1 and datetime.datetime.now().month >= 8 else datetime.datetime.now().year + 542

    return render_template('user_em_check.html', student = student, minus_year = minus_year)

@views.route('/user/overall', methods=['GET', 'POST'], endpoint='user_em_all')
def user_em_overall_page():
    result = None
    program = None
    count_program = None
    menu = None
    text_r = None
    if request.method == 'POST':
        menu = request.form.get('overall-choose')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if menu == 'overall1':
            m = datetime.date.today()
            if m.month >= 8:
                year = m.year
            else:
                year = m.year - 1 
            cursor.execute('SELECT gender, count(*) AS count_program FROM student WHERE expected_grad = %s GROUP BY gender', (year,))
            result = cursor.fetchall()

            if len(result) == 0:
                text_r = 'ไม่พบข้อมูล'
            else:
                def func(pct, allvalues):
                    absolute = int(pct / 100.*np.sum(allvalues))
                    return "{:.1f}%\n({:d} คน)".format(pct, absolute)
                plt.pie(count_program, labels = program, autopct=lambda pct: func(pct, count_program))
                plt.legend(title = "หลักสูตร:",loc ="center left", bbox_to_anchor =(1, 0, 0.5, 1))
                plt.title(f'กราฟแสดงสัดส่วนนักศึกษาที่จะจบการศึกษาในหลักสูตร (ข้อมูลล่าสุด ณ {datetime.datetime.now().date()})')
                plt.show()


        elif menu == 'overall2':
            cursor.execute('SELECT start_year, count(*) AS count_program FROM student GROUP BY start_year')
            result = cursor.fetchall()

            if len(result) == 0:
                text_r = 'ไม่พบข้อมูล'
            else:
                program = ['นศ.รหัส ' + str(item['start_year'])[:2] for item in result]
                count_program = [item['count_program'] for item in result]

                def func(pct, allvalues):
                    absolute = int(pct / 100.*np.sum(allvalues))
                    return "{:.1f}%\n({:d} คน)".format(pct, absolute)
                plt.pie(count_program, labels = program, autopct=lambda pct: func(pct, count_program))
                plt.legend(title = "หลักสูตร:",loc ="center left", bbox_to_anchor =(1, 0, 0.5, 1))
                plt.title(f'กราฟแสดงสัดส่วนนักศึกษาในแต่ละหลักสูตร (ข้อมูลล่าสุด ณ {datetime.datetime.now().date()})')
                plt.show()
    return render_template('user_em_overall.html', text_r = text_r)


@views.route('/user/de-home', methods=['GET', 'POST'], endpoint='user_de')
@login_is_required
def user_de_home():
    
    image = session["picture"]
    # user = User.query.filter_by(email = session["email"]).first()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user WHERE email = %s", (session["email"],))
    user = cursor.fetchone()
    cursor.close()

    # if user.gender == 'M':
    #     gender = 'ชาย'
    # elif user.gender == 'F':
    #     gender = 'หญิง'
    # else:
    #     gender = 'อื่นๆ'

    if user['gender'] == 'M':
        gender = 'ชาย'
    elif user['gender'] == 'F':
        gender = 'หญิง'
    else:
        gender = 'อื่นๆ'
    
    return render_template("user_de_home.html", result = user, gender = gender, image = image)

@views.route('/user/de-edit', methods=['GET', 'POST'], endpoint='user_de_edit')
@login_is_required
def user_de_edit_info():
    # user = User.query.filter_by(email = session['email']).first()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        NameTH = request.form.get('NameTH')
        NameEN = request.form.get('NameEN')
        gender = request.form.get('genderchoose')

        if len(NameTH) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        elif len(NameEN) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        else:
            ### Update user to database
            # user.user_id = user.user_id
            # user.program_id = user.program_id
            # user.nameTH = NameTH
            # user.nameEN = NameEN
            # user.role = user.role
            # user.gender = gender
            # user.email = session['email']

            # db.session.add(user)
            # db.session.commit()

            cursor.execute("UPDATE user SET nameEN= %s, nameTH= %s, gender= %s WHERE email = %s", (NameEN, NameTH, gender, session["email"]))
            mysql.connection.commit()
            cursor.close()
            flash('แก้ไขข้อมูลสำเร็จ!.', category='success')
            return redirect(url_for('views.user_de'))

    return render_template('user_de_home_edit.html')

@views.route('/user/de-overall', methods=['GET', 'POST'], endpoint='user_de_all')
def de_overall_page():
    result = None
    program = None
    count_program = None
    menu = None
    text_r = None
    if request.method == 'POST':
        menu = request.form.get('overall-choose')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if menu == 'overall1':
            m = datetime.date.today()
            if m.month >= 8:
                year = m.year
            else:
                year = m.year - 1 
            cursor.execute('SELECT program_id, count(*) AS count_program FROM student WHERE expected_grad = %s GROUP BY program_id', (year,))
            result = cursor.fetchall()

            if len(result) == 0:
                text_r = 'ไม่พบข้อมูล'
            else:
                def func(pct, allvalues):
                    absolute = int(pct / 100.*np.sum(allvalues))
                    return "{:.1f}%\n({:d} คน)".format(pct, absolute)
                plt.pie(count_program, labels = program, autopct=lambda pct: func(pct, count_program))
                plt.legend(title = "หลักสูตร:",loc ="center left", bbox_to_anchor =(1, 0, 0.5, 1))
                plt.title(f'กราฟแสดงสัดส่วนนักศึกษาที่จะจบการศึกษาในแต่ละหลักสูตร (ข้อมูลล่าสุด ณ {datetime.datetime.now().date()})')
                plt.show()


        elif menu == 'overall2':
            cursor.execute('SELECT program_id, count(*) AS count_program FROM student GROUP BY program_id')
            result = cursor.fetchall()

            if len(result) == 0:
                text_r = 'ไม่พบข้อมูล'
            else:
                program = [item['program_id'] for item in result]
                count_program = [item['count_program'] for item in result]

                def func(pct, allvalues):
                    absolute = int(pct / 100.*np.sum(allvalues))
                    return "{:.1f}%\n({:d} คน)".format(pct, absolute)
                plt.pie(count_program, labels = program, autopct=lambda pct: func(pct, count_program))
                plt.legend(title = "หลักสูตร:",loc ="center left", bbox_to_anchor =(1, 0, 0.5, 1))
                plt.title(f'กราฟแสดงสัดส่วนนักศึกษาในแต่ละหลักสูตร (ข้อมูลล่าสุด ณ {datetime.datetime.now().date()})')
                plt.show()

    return render_template('user_de_overall.html', menu = menu, program = program, count_p = count_program, text_r = text_r)
