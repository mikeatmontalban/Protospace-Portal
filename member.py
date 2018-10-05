import os.path

from flaskr.db import get_db

import functools

from datetime import date

import time
from time import strftime,localtime

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('member', __name__, url_prefix='/member')

######################################################################

@bp.route('/', methods=('GET', 'POST'))
def member():
    now=str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    if request.method == 'POST':
        db = get_db()

        if 'SearchMembersButton' in request.form:
            if request.form['member_name'] != '':
                q = 'SELECT member_id,firstname,lastname FROM `members` WHERE ' +\
                    'firstname like "%' + request.form['member_name'] + '%" OR ' +\
                    'lastname like "%' + request.form['member_name'] + '%"'
                db.execute(q)
                rows = db.fetchall()
                if rows is None:
                    flash(request.form['member_name'] + ': no match found')
                elif len(rows) == 1:
                    q = 'SELECT * FROM `members` WHERE member_id=' + str(rows[0][0])
                    db.execute(q)
                    row = db.fetchone()
                    return render_template('member/home.html',member_record=row,now=now)
                else:
                    matching_members = []
                    for row in rows:
                        member_id = str(row[0])
                        member_link = '<a href="' + url_for('member.member',member_id=member_id) + '">' +\
                                                row[1] + ' ' + row[2] + '</a>'
                        matching_member = [member_id, member_link]
                        photo_path = '/static/img/members/' + member_id + '.jpg'
                        if os.path.exists('/Web/protospace/portal/flaskr' + photo_path):
                            matching_member.append('<img src="' + photo_path + '" height="120" width="90">')
                        else:
                            matching_member.append('No photo')
                        matching_members.append(matching_member)
                    return render_template('member/show_matching_members.html',
                                           matching_members=matching_members,
                                           now=now)

            elif request.form['member_id'] != '':
                q = 'SELECT * FROM `members` WHERE member_id=' + request.form['member_id']
                db.execute(q)
                rows = db.fetchall()
                if len(rows) != 1:
                    flash(request.form['member_id'] + ': not found.')
                else:
                    return render_template('member/home.html',member_record=rows[0],now=now)
                
                return render_template('member/home.html',member_record=g.user,now=now)

                
        elif 'submenu' in request.form:
            submenu= request.form['submenu']
            member_id = str(g.user[0])
            if submenu == 'Transactions':
                q = 'SELECT date,amount,description,transaction,category FROM `journal` WHERE member_id="' + member_id + '"'
                db.execute(q)
                transactions = db.fetchall()
                print('transactions: ' + str(transactions))
                return render_template('member/show_transactions.html',
                                       now=now,member_record=g.user,
                                       submenu=submenu,
                                       transactions=transactions)
            
            elif submenu == 'Training':
                my_history = []
                q = 'SELECT class_id,status FROM `member_training_history` WHERE member_id="' + member_id + '"'
                db.execute(q)
                transactions = db.fetchall()
                for (class_id,status) in transactions:
                    q = 'SELECT course_id,class_date_time FROM `class_history` WHERE class_id=' + str(class_id)
                    db.execute(q)
                    row = db.fetchone()
                    if row is None:
                        flash('Class history not found: ' + q)
                    else:
                        (course_id,class_date_time) = row
                        q = 'SELECT course_title FROM `courses` WHERE course_id=' + str(course_id)
                        db.execute(q)
                        course_title = db.fetchone()[0]
                        my_history.append([course_title,class_date_time,status,class_id,course_id])

                return render_template('member/show_training.html',
                                       now=now,
                                       member_record=g.user,
                                       submenu=submenu,
                                       my_history=my_history)

                
            elif submenu == 'Membership':
                return render_template('member/show_membership.html',
                                       now=now,
                                       member_record=g.user,
                                       submenu=submenu)
            
            elif submenu == 'Keys':
                member_id = str(session.get('member_id'))
                q = 'SELECT lastname,firstname,key_number FROM `members` WHERE member_id="' + member_id + '"'
                db.execute(q)
                row = db.fetchall()
                if row == ():
                    flash('Card number not found for ' + member_id)
                else:
                    return render_template('member/show_keys.html',
                                           now=now,
                                           member_record=g.user,
                                           submenu=submenu,
                                           card_number=row[0][2],
                                           notes=row[0][1] + ' ' + row[0][0],
                                           last_seen="Never.")
                
            elif submenu == 'Storage':
                member_id = str(session.get('member_id'))
                q = 'SELECT lastname,firstname,shelf_address FROM `members` WHERE member_id="' + member_id + '"'
                db.execute(q)
                row = db.fetchone()
                if row == ():
                    flash('No storage found for ' + member_id)
                else:
                    return render_template('member/show_storage.html',
                                           now=now,
                                           member_record=g.user,
                                           submenu=submenu,
                                           location=row[2],
                                           description=row[1] + ' ' + row[0] + ' Member Shelf')
#                                           until=row[0][3])
            
            elif submenu == 'Notes':
                return render_template('member/show_notes.html',now=now,member_record=g.user,submenu=submenu)

        else:
            flash('How did we get here?')
                
    return render_template('member/home.html',member_record=g.user,now=now)


######################################################################

@bp.route('/change_password', methods=('GET', 'POST'))
def change_password():
    if request.method == 'POST':
        oldpass = request.form['oldpass']
        if not oldpass:
            flash('Please enter your current password.')
        else:
            member_id = str(session.get('member_id'))
            q = 'SELECT password FROM passwords WHERE member_id = "' + member_id + '"'
            db = get_db()
            db.execute(q)
            password = db.fetchone()[0]
            if not check_password_hash(password,oldpass):
                flash('Incorrect password: {}'.format(password))
            else:
                newpass1 = request.form['newpass1']
                if not newpass1:
                    flash('Please enter a new password.')
                newpass2 = request.form['newpass2']
                if not newpass2:
                    flash('Please confirm your new password.')
                else:
                    if newpass1 != newpass2:
                        flash('New passwords are not equal. Please re-enter them.')
                    else:
                        if 'change_portal_password' in request.form:
                            q = 'UPDATE passwords SET password="' + generate_password_hash(newpass1) + '" WHERE member_id='
                            db.execute(q + member_id)
                            db.execute('commit')
                            flash('Your portal password has been reset.')
                        if 'change_windows_password' in request.form:
                            q = 'UPDATE passwords SET windows_password="' + generate_password_hash(newpass1) + '" WHERE member_id='
                            db.execute(q + member_id)
                            db.execute('commit')
                            flash('Your windows password has been reset.')
                        
                        return redirect(url_for('member.member'))

    return render_template('member/change_password.html',
                           now=str(strftime("%a, %d %b %Y %H:%M:%S", localtime())))

######################################################################

@bp.route('/request_new_keycard', methods=('GET', 'POST'))
def request_new_keycard():
    now=str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    step = ''
    if request.method == 'POST':
        if 'photo_choice' in request.form:
            photo_choice = request.form['photo_choice']
            if photo_choice == 'Upload':
                pass
            elif photo_choice == 'CropDB':
                pass

            step = 'pick_background'

        elif 'background' in request.form:
            step = 'prepare_card'
            
    return render_template('member/request_new_keycard.html',now=now,step=step)


######################################################################

@bp.route('/member_cash_journal', methods=('GET', 'POST'))
def member_cash_journal():
    now=str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    db = get_db()

    member_id = str(g.user[0])
    q = 'SELECT firstname,lastname FROM `members` WHERE member_id=' + member_id
    db.execute(q)
    row = db.fetchone()
    name = str(row[0]) + ' ' + str(row[1])
    q = 'SELECT date,transaction,description,amount,category FROM `journal` WHERE member_id=' + member_id
    db.execute(q)
    rows = db.fetchall()
    beginning_date = rows[0][0]
    balance = 0.0
    member_journal = [[beginning_date,'','Balance on ' + str(beginning_date),0.0,'','']]
    for row in rows:
        (date,transaction,description,amount,category) = row
        balance = balance + float(amount)
        entry = [date,transaction,description,amount,'{0:.2f}'.format(balance),category]
        member_journal.append(entry)
              
    return render_template('member/member_cash_journal.html',
                           member_id=member_id,
                           name=name,
                           member_journal=member_journal,
                           now=now)



######################################################################

@bp.route('/add_keycard', methods=('GET', 'POST'))
def add_keycard():
    now=str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    db = get_db()

    if request.method == 'POST':
        member_id = request.form['member_id']
        key_number = request.form['key_number']
        import re
        if not re.match('\w{10}',key_number):
            flash('Invalid key number: ' + key_number)
        else:
            q = 'UPDATE `members` SET key_number="' + key_number + '" WHERE member_id=' + str(member_id)
            db.execute(q)
            db.execute('commit;')
            flash('New key number: ' + key_number + ' saved. Now pushing to the door controllers.....')
            return render_template('member/home.html',member_record=g.user,now=now)

    q = 'SELECT member_id,firstname,lastname FROM `members` ORDER BY firstname'
    db.execute(q)
    member_names = db.fetchall()
    return render_template('member/add_keycard.html',
                           member_names=member_names,
                           now=now)
    

######################################################################

@bp.route('/reprint_membership_forms', methods=('GET', 'POST'))
def reprint_membership_forms():
    now=str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    db = get_db()

    q = 'SELECT lastname,firstname,nickname,mailing_address,city,' +\
        'province,postal_code,email,phone,application_date ' +\
        'FROM members WHERE member_id = "' + str(g.user[0]) + '"'
    db.execute(q)

    myself = db.fetchone()
    if myself is None:
        flash('member_id: {} not found.'.format(member_id))

    else:
#        import pyfpdf
#
#        filename = 'ams_records.' + today + '.pdf'
#
#        pdf = FPDF('P','in','Letter')
#        pdf.add_page()
#        pdf.set_font('Courier','',10)
#        pdf.set_margins(1.0,1.0,1.0)
#        pdf.set_autopagebreak('on',1.0)
#
#        kline = 0
#
#        for line in req.form.getfirst("output"):
#            line = line.replace('|',' ')
#            if ((line.substr(21,2) == 'RF') or (line.substr(21,2) == 'RM')):
#	        line = line.substr(0,46)
#
#        pdf.cell(0,0.16,line,0,1,'L',0)
#        kline = kline + 1
#
#        if (kline >= 55):
#	    pdf.add_page('P','Letter')
#	    kline = 0
#
#        pdf.output(filename,'I')
#
        return render_template('member/reprint_membership_forms.html',
                               lastname=myself[0],
                               firstname=myself[1],
                               nickname=myself[2],
                               mailing_address=myself[3],
                               city=myself[4],
                               province=myself[5],
                               postal_code=myself[6],
                               email=myself[7],
                               phone=myself[8],
                               application_date=myself[9],
                               now=now)

    return render_template('member/home.html',
                           member_record=g.user,
                           now=now)

######################################################################

@bp.route('/add_email', methods=('GET', 'POST'))
def add_email():
    now=str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    if request.method == 'POST':
        if request.form['ActionButton'] is not None:
            if 'new_email' not in request.form:
                flash('No new email address given.')
            else:
                q = 'INSERT INTO `email_addresses` VALUES (' + str(g.user[0]) + ', "' + request.form['new_email'] + '")'
            db = get_db()
            db.execute(q)
            db.execute('commit')

            flash('Email address: "' + request.form['new_email'] + '" has been saved.')
            return render_template('member/home.html',
                                   member_record=g.user,
                                   now=now)
            
    return render_template('member/add_email.html',now=now)


######################################################################

@bp.route('/edit_member', methods=('GET', 'POST'))
def edit_member():
    now=str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    if request.method == 'POST':
        if request.form['ActionButton'] is not None:
            q = 'UPDATE `members` SET '
            for field in ('firstname','lastname','nickname','mailing_address','city',
                          'province','postal_code','email','phone','emergency_contact',
                          'emergency_contact_phone'):
                if request.form[field] != '':
                    q += field + '="' + request.form[field] + '",'

            if 'member_is_minor' in request.form:
                q += 'birthdate="' + request.form['birthdate'] + '",' +\
                                 'guardian_name="' + request.form['guardian_name'] + '",'

            q = q.rstrip(',') + ' WHERE member_id = "' + str(g.user[0]) + '"'

            db = get_db()
            db.execute(q)
            db.execute('commit')
            
            flash('My vital statistics have been updated.')
            return render_template('member/home.html',now=now)
            
    return render_template('member/edit_member.html',now=now)


######################################################################

@bp.route('/new_membership_record', methods=('GET', 'POST'))
def new_membership_record():
    now=str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    if request.method == 'POST':
        if 'ActionButton' in request.form:
            q = 'INSERT INTO `membership_records` member_id,member_type,start_date,end_date,notes'

            flash('A new membership record has been created for: ' + str(g.user[1]))
            return render_template('member/home.html',
                                   submenu='Membership',
                                   now=now)
            
    return render_template('member/new_membership_record.html',now=now)
