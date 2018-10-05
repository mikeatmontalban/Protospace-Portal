import functools

from datetime import date

import time
from time import strftime,localtime

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('training', __name__, url_prefix='/admin/training')

today = str(strftime("%Y-%m-%d", localtime()))


@bp.route('/', methods=('GET', 'POST'))
def admin():
    return render_template('training/home.html',now=now)


######################################################################

@bp.route('/schedule_class', methods=('GET', 'POST'))
def schedule_class():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    course_list = '<option value=""> -- Select a course -- </option>' + "\n"

    db = get_db()
    q = 'SELECT course_id,course_title FROM `courses`'
    db.execute(q)
    rows = db.fetchall()
    if rows is None:
        flash('No class titles found.')
    else:
        for row in rows:
            course_list += '<option value="' + str(row[0]) + '">' + row[1] + '</option>' + "\n"

    if request.method == 'POST':

        if request.form['ActionButton'] == 'Next':
            course_id = request.form['course_id']

            inst_list = ''
            q = 'SELECT a.instructor_id,b.firstname,b.lastname FROM course_instructors a, members b WHERE a.instructor_id=b.member_id AND a.course_id="' + course_id + '"'
            db.execute(q)
            rows = db.fetchall()
            if rows == ():
                print('1 inst rows: ' + str(rows))
                flash('No instructors found.')
                inst_list = '<input type="hidden" name="instructor_id" value=" ">'
            else:
                print('2 inst rows: ' + str(rows))
                for row in rows:
                    inst_list += '<br><input type="checkbox" name="instructor_id" value="' +\
                                                   str(row[0]) + '">' + row[1] + ' ' + row[2]

            adm_list = ''
            q = 'SELECT a.administrator_id,b.firstname,b.lastname FROM course_administrators a, ' +\
                'members b WHERE a.administrator_id=b.member_id AND a.course_id="' + course_id + '"'
            db.execute(q)
            rows = db.fetchall()
            if rows == ():
                flash('No administrators found.')
                adm_list = '<input type="hidden" name="administrator_id" value=" ">'
            else:
                for row in rows:
                    adm_list += '<br><input type="checkbox" name="administrator_id" value="' +\
                                                   str(row[0]) + '">' + row[1] + ' ' + row[2]

            print('inst_list: ' + str(inst_list))
            print('adm_list: ' + str(adm_list))
            
            return render_template('training/schedule_class.html',
                                   now=now,
                                   page="2",
                                   course_id=request.form['course_id'],
                                   class_date_time=request.form['class_date'] + ' ' + request.form['start_time'],
                                   fee_for_member=request.form['fee_for_member'],
                                   fee_for_nonmember=request.form['fee_for_nonmember'],
                                   inst_list=inst_list,
                                   adm_list=adm_list)


        elif request.form['ActionButton'] == 'Finish':
            
            if request.form['instructor_id'] is None:
                intstructor_id = 0
                instructor = ''
            else:
                instructor_id = request.form['instructor_id']
                q = 'SELECT firstname,lastname from members WHERE member_id="' + instructor_id + '"'
                db.execute(q)
                row = db.fetchone()
                if row is None:
                    instructor = ''
                else:
                    instructor = row[0] + ' ' + row[1]

            if request.form['administrator_id'] is None:
                administrator_id = 0
                administrator = ''
            else:
                administrator_id = request.form['administrator_id']
                q = 'SELECT firstname,lastname from members WHERE member_id="' + administrator_id + '"'
                db.execute(q)
                row = db.fetchone()
                if row is None:
                    administrator = ''
                else:
                    administrator = row[0] + ' ' + row[1]

            q = 'INSERT INTO `class_history` (course_id,instructor_id,administrator_id,fee_for_member,fee_for_nonmember,' +\
                'class_date_time,minimum_attendees,maximum_attendees,allow_self_registration,waiting,confirmed,holding,available) ' + "\n" +\
            'VALUES (' +\
            request.form['course_id'] + ',' +\
            instructor_id + ',' +\
            administrator_id + ',' +\
            request.form['fee_for_member'] + ',' +\
            request.form['fee_for_nonmember'] + ',' +\
            '"' + request.form['class_date_time'] + '",' +\
            request.form['min'] + ',' +\
            request.form['max'] + ',' +\
            '"' + request.form['online_reg'] + '",' +\
            '0,0,0,0)'

            print(q)
            db.execute(q)
            db.execute('commit')
            
            q = 'SELECT course_title from courses WHERE course_id="' + request.form['course_id'] + '"'
            db.execute(q)
            row = db.fetchone()
            course_title= row[0]

            if request.form['online_reg'] == 'on':
                self_registration = 'Members may self register'
            else:
                self_registration = 'Members may NOT self register'

            return render_template('training/schedule_class.html',
                                   now=now,
                                   page="3",
                                   course_title=course_title,
                                   class_date_time=request.form['class_date_time'],
                                   instructor=instructor,
                                   administrator=administrator,
                                   fee_for_member=request.form['fee_for_member'],
                                   fee_for_nonmember=request.form['fee_for_nonmember'],
                                   minimum=request.form['min'],
                                   maximum=request.form['max'],
                                   self_registration=self_registration)

        else:
            return render_template('training/lost.html',now=now)

    return render_template('training/schedule_class.html',now=now,page="1",course_list=course_list)


######################################################################

@bp.route('/class_history', methods=('GET', 'POST'))
def class_history():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    if request.method == 'POST':
        pass

    return render_template('training/class_history.html',now=now)


######################################################################

@bp.route('/open_shopping_carts', methods=('GET', 'POST'))
def open_shopping_carts():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    if request.method == 'POST':
        pass

    return render_template('training/open_shopping_carts.html',now=now)


######################################################################

@bp.route('/classes', methods=('GET', 'POST'))
def classes():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    class_list = '<tr><th>Subject</th><th>Class #</th><th>Date</th><th>Confirmed</th><th>Open</th></tr>'
    db = get_db()
    q = 'SELECT * FROM `class_history` WHERE `date` > CURDATE()'
    db.execute(q)
    row = db.fetchone()
    while row is not None:
        course_id = str(row[0])
        course_title = row[1]
        q = 'SELECT * FROM `courses` where `course_id` ="' + course_id + '"'
        db.execute(q)
        row = db.fetchone()
        if row is None:
            flash('course_id: ' + course_id + ' not found.')
        else:
            class_list = '<tr><td>' + course_title + '</td><td>' + date + '</td><td>' + \
            confirmed + '</td><td>' + open + '</td><td>Learn more</td></tr>'

    if request.method == 'POST':
        pass
    
    return render_template('training/classes.html',class_list=class_list,now=now)

