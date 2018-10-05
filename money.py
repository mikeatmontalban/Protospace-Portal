import functools

from datetime import date

import time
from time import strftime,localtime

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('money', __name__, url_prefix='/admin/money')


######################################################################

@bp.route('/take_cash', methods=('GET', 'POST'))
def take_cash():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    member_list = {}
    db = get_db()
    q = 'SELECT member_id,lastname,firstname FROM `members`'
    db.execute(q)
    row = db.fetchone()
    while row is not None:
        name = row[2] + ' ' + row[1]
        member_list[name] = row[0]
        row = db.fetchone()

    html_member_list = '<option value="0" selected>Select a Member</option>' + "\n"
    for name,id in sorted(member_list.iteritems()):
        html_member_list += '<option value="' + str(id) + '">' + name + '</option>' + "\n"

    if request.method == 'POST':
        if request.form['ActionButton'] is not None:
            return render_template('admin/money/cash_taken.html',
                                   date = request.form['date'],
                                   account = request.form['account'],
                                   refnum = request.form['refnum'],
                                   memberbox = request.form['memberbox'],
                                   paidby = request.form['paidby'],
                                   amount = request.form['amount'],
                                   category = request.form['category'],
                                   months = request.form['months'],
                                   memo = request.form['memo'],
                                   now=now)
        
    
    return render_template('admin/money/take_cash.html',member_list=html_member_list,now=now)


######################################################################

@bp.route('/cash_report', methods=('GET', 'POST'))
def cash_report():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    if request.method == 'POST':
        pass

    return render_template('admin/money/cash_report.html',now=now)


######################################################################

@bp.route('/all_transactions', methods=('GET', 'POST'))
def all_transactions():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    q = 'SELECT * FROM transactions ORDER BY date'

    db = get_db()
    db.execute(q)
    rows = db.fetchall()
    transactions = []

    for row in rows:
        (date,member_id,amount,mth,description,transid,receipt,method) = row
        q = 'SELECT firstname,lastname FROM `members` WHERE member_id=' + str(member_id)
        db.execute(q)
        row = db.fetchone()
        if row is None:
            flash('Name not found for member_id: ' + str(member_id))
            name = ''
        else:
            name = row[0] + ' ' + row[1]
        entry = [date,name,amount,mth,description,transid,receipt,method]
        transactions.append(entry)
              
    return render_template('admin/money/all_transactions.html',
                           transactions=transactions,
                           now=now)


######################################################################

@bp.route('/new_ipns', methods=('GET', 'POST'))
def new_ipns():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    if request.method == 'POST':
        pass

    return render_template('admin/money/new_ipns.html',now=now)


######################################################################

@bp.route('/ipn_review', methods=('GET', 'POST'))
def ipn_review():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    if request.method == 'POST':
        pass

    return render_template('admin/money/ipn_review.html',now=now)


######################################################################

@bp.route('/no_match_ipn', methods=('GET', 'POST'))
def no_match_ipn():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    if request.method == 'POST':
        pass

    return render_template('admin/money/no_match_ipn.html',now=now)


######################################################################

@bp.route('/create_paypal_link', methods=('GET', 'POST'))
def create_paypal_link():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    if request.method == 'POST':
        pass

    return render_template('admin/money/create_paypal_link.html',now=now)


######################################################################

@bp.route('/replay_missed_payload', methods=('GET', 'POST'))
def replay_missed_payload():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    if request.method == 'POST':
        pass

    return render_template('admin/money/replay_missed_payload.html',now=now)


######################################################################

@bp.route('/all_member_cash_journal', methods=('GET', 'POST'))
def all_member_cash_journal():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    balance = 0.0
    journal = []

    q = 'SELECT date,transaction,description,amount,category FROM journal ORDER BY date'
    db = get_db()
    db.execute(q)
    rows = db.fetchall()
    
    for row in rows:
        (date,transaction,description,amount,category) = row
        balance = balance + float(amount)
        entry = [date,transaction,description,amount,'{0:.2f}'.format(balance),category]
        journal.append(entry)
              
    return render_template('admin/money/all_member_cash_journal.html',
                           journal=journal,
                           now=now)

