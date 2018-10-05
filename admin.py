import functools

from datetime import date

import time
from time import strftime,localtime

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/', methods=('GET', 'POST'))
def admin():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    return render_template('admin/home.html',now=now)


######################################################################

@bp.route('/members/reset_password', methods=('GET', 'POST'))
def reset_password():
    db = get_db()
    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    if request.method == 'POST':
        member_id = request.form['member_id']
        if 'NewPass' not in request.form:
            flash('Please enter a new password.')
        else:
            NewPass = request.form['NewPass']
            if 'ConfirmNewPass' not in request.form:
                flash('Please confirm the new password.')
            else:
                ConfirmNewPass = request.form['ConfirmNewPass']
                if NewPass != ConfirmNewPass:
                    flash('New passwords are not equal. Please re-enter them.')
                else:
                    q = 'SELECT firstname,lastname FROM `members` WHERE member_id='
                    db.execute(q + member_id)
                    row = db.fetchone()
                    name = row[0] + ' ' + row[1]
                    if 'change_portal_password' in request.form:
                        q = 'UPDATE passwords SET password="' + generate_password_hash(NewPass) + '" WHERE member_id=' + member_id
                        db.execute(q)
                        db.execute('commit')
                        flash('The portal password for ' + name + ' has been reset.')
                    if 'change_windows_password' in request.form:
                        q = 'UPDATE passwords SET windows_password="' + generate_password_hash(NewPass) + '" WHERE member_id=' + member_id
                        db.execute(q)
                        db.execute('commit')
                        flash('The windows password for ' + name +  ' has been reset.')
                        
                    return redirect(url_for('member.member'))

    q = 'SELECT member_id,firstname,lastname FROM `members` ORDER BY firstname'
    db.execute(q)
    member_names = db.fetchall()

    return render_template('admin/members/reset_password.html',
                           member_names=member_names,
                           now=now)



######################################################################

@bp.route('/members/delete_duplicate_member', methods=('GET', 'POST'))
def delete_duplicate_member():
    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    db = get_db()

    if request.method == 'POST':
        if 'ActionButton' in request.form:
            if request.form['ActionButton'] == 'Delete':
                if request.form['memberbox'] != '':
                    delete_member_id = request.form['memberbox']
                    q = 'SELECT firstname,lastname FROM `members` WHERE member_id=' + delete_member_id
                    db.execute(q)
                    (firstname, lastname) = db.fetchone()
                    q = 'SELECT member_id FROM `members` WHERE firstname="' + firstname +'" AND lastname="' + lastname + '"'
                    db.execute(q)
                    rows = db.fetchall()
                    if len(rows) > 1:
                        flash('multiple IDs found: ' + str(rows) + ' deleting: ' + delete_member_id)
                    else:
                        flash('Only one ID found (' + str(rows[0][0]) + ') for: ' + firstname + ' ' + lastname)

                    return render_template('member/home.html',member_record=g.user,now=now)

    q = 'SELECT member_id,firstname,lastname FROM `members` ORDER BY firstname'
    db.execute(q)
    members = db.fetchall()
    
    return render_template('admin/members/delete_duplicate_member.html',members=members,now=now)


######################################################################

@bp.route('/members/add_second_email', methods=('GET', 'POST'))
def add_second_email():
    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    if request.method == 'POST':
        pass

    return render_template('admin/members/add_second_email.html',now=now)


######################################################################

@bp.route('/members/add_keycard', methods=('GET', 'POST'))
def add_keycard():
    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    if request.method == 'POST':
        pass

    return render_template('admin/members/add_keycard.html',now=now)


######################################################################

@bp.route('/members/vacation', methods=('GET', 'POST'))
def vacation():
    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    db = get_db()

    if request.method == 'POST':
        if request.form['memberbox'] != '':
            leaving_member_id = request.form['memberbox']
        if request.form['effective_date'] == '':
            effective_date = 'when expires'
        else:
            effective_date = request.form['effective_date']
        if 'record_as_vacation' in request.form:
            if request.form['record_as_vacation'] == 'on':
                record_as_vacation = 'y'
            else:
                record_as_vacation = 'n'
        else:
            record_as_vacation = 'n'
        if request.form['ActionButton'] == 'End Membership':
            resignation = 'yes'
        flash('leaving_member_id: ' + str(leaving_member_id) + ' effective_date: ' + str(effective_date) +\
              ' record_as_vacation: ' + record_as_vacation + ' resignation: ' + resignation)
        return render_template('member/home.html',member_record=g.user,now=now)

    q = 'SELECT member_id,firstname,lastname FROM `members` ORDER BY firstname'
    db.execute(q)
    members = db.fetchall()
    return render_template('admin/members/vacation.html',members=members,now=now)


######################################################################

@bp.route('/the_space/door_access', methods=('GET', 'POST'))
def door_access():
    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    if request.method == 'POST':
        pass

    return render_template('admin/the_space/door_access.html',now=now)


######################################################################

@bp.route('/the_space/update_door_controller', methods=('GET', 'POST'))
def update_door_controller():
    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    if request.method == 'POST':
        pass

    return render_template('admin/the_space/update_door_controller.html',now=now)
