import functools

import re
# http://www.rhyous.com/2010/06/15/regular-expressions-in-cincluding-a-new-comprehensive-email-pattern/
email_pattern = re.compile("^[\w!#$%&'*+\-/=?\^_`{|}~]+(\.[\w!#$%&'*+\-/=?\^_`{|}~]+)*@((([\-\w]+\.)+[a-zA-Z]{2,4})|(([0-9]{1,3}\.){3}[0-9]{1,3}))$")
username_pattern = re.compile("^[\w\-_~]+\.{1}[\w\-_~]+")

from datetime import date

import time
from time import strftime,localtime

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        email = request.form['email']
        if not firstname:
            flash('First Name is required: ',firstname)
        if not lastname:
            flash('Last Name is required: ',lastname)
        elif not email:
            flash('Email is required: ',email)
        elif mail_pattern.match(email) is None:
            flash('Invalid email address: {}. Please try again.')
        else:

            db = get_db()

            q = 'SELECT member_id FROM members WHERE lastname = "' + lastname + '" AND firstname = "' + firstname + '" AND email = "' + email + '"'
#            print(' 1 q: ' + q)
            
            db.execute(q)

            if db.fetchone() is not None:
                flash('{} {} is already signed up.'.format(firstname, lastname))

            else:
                username = re.sub('[\' ]','',firstname.lower() + '.' + lastname.lower())
                
                q = 'INSERT INTO members (username,lastname,firstname,email,mailing_address,city,province,postal_code,' + \
                    'phone,emergency_contact,emergency_contact_phone,membership_class,application_date)' + \
                    'VALUES ("' + username + '","' + lastname + '","' + firstname + '","' + email + '","' + \
                    request.form['mailing_address'] + '","' + \
                    request.form['city'] + '","' + \
                    request.form['province'] + '","' + \
                    request.form['postal_code'] + '","' + \
                    request.form['phone'] + '","' + \
                    request.form['emergency_contact'] + '","' + \
                    request.form['emergency_contact_phone'] + '","' + \
                    request.form['membership_class'] + '","' + \
                    str(date.today()) + '")'
                
                db.execute(q)
                db.execute('commit')
                return redirect(url_for('auth.login'))

    return render_template('auth/register.html',now=now)


@bp.route('/set_password', methods=('GET', 'POST'))
def set_password():
    i_am = request.form['identifier']
    if i_am is not None:
        if (i_am == mail_pattern.match(i_am)) is not None:
            db = get_db()
            db.execute('SELECT member_id FROM members where email = "' + i_am + '"')
            member_id = db.fetchone()
            if member_id is None:
                if (i_am == username_pattern.match(i_am)) is not None:
                    (firstname,lastname) = i_am.split(' ')
                    q = 'SELECT member_id FROM members where firstname = "' + firstname + '" AND lastname = "' + lastname + '"'
#                    print('q: ' + q)
                    db.execute(q)
                    member_id = db.fetchone()

                    if member_id is None:
                        flash('{} not found.'.format(i_am))
                    else:
                        q = 'SELECT password FROM passwords WHERE member_id = "' + str(member_id[0]) + '"'
#                        print('q: ' + q)
                        db.execute(q)
                        if db.fetchone() is not None:
                            flash('Your password is already set.')
                        else:
                            password = request.form['password']
                            password2 = request.form['password2']
                            if password != password2:
                                flash('Passwords are not equal. Please re-enter them.')
                            else:
                                q = 'INSERT INTO passwords (member_id,password)' + \
                                    ' VALUES ("' + str(member_id[0]) + '","' + generate_password_hash(password) + '")'
#                                print('member_id: ' + str(member_id[0]) + ' password: ' + password + ' q: ' + q)
                                db.execute(q)
                                db.execute('commit')
                        
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        db = get_db()

        username = request.form['username']
        if username_pattern.match(username) is None:
            flash('Invalid username format. It must be "firstname.lastname", all lowercase. Please re-enter.')
        else:
            db.execute('SELECT * FROM members WHERE username = "' + username + '"')
            member_id = db.fetchone()
            if member_id is None:
                flash('Username: ' + username + ' not found. Please re-enter.')
            else:
                member_id = str(member_id[0])
                db.execute('SELECT password FROM passwords WHERE member_id = "' + member_id + '"')
                password = db.fetchone()
                if password is None:
                    flash(username + ': password not found.')
                else:
                    if not check_password_hash(password[0],request.form['password']):
                        flash('Incorrect password: {}'.format(password[0]))
                    else:
                        session.clear()
                        session['member_id'] = member_id
                        return redirect(url_for('member.member'))

    return render_template('auth/login.html',now=now)


@bp.before_app_request
def load_logged_in_user():
    member_id = session.get('member_id')

    if member_id is None:
        g.user = None
    else:
        db = get_db()
        q = 'SELECT * FROM members WHERE member_id="' + member_id + '"'
        db.execute(q)
        g.user = db.fetchone()
#        print('q: ' + q + ' g.user: ' + str(g.user) + ' session: ' + str(session))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

