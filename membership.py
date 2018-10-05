from flaskr.db import get_db

import functools

from datetime import date

import time
from time import strftime,localtime

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('membership', __name__, url_prefix='/membership')

@bp.route('/', methods=('GET', 'POST'))
def membership():
    return render_template('membership/home.html',now=now)


######################################################################

@bp.route('/member_list', methods=('GET', 'POST'))
def member_list():
    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
    db = get_db()
    q = 'SELECT member_id,firstname,lastname FROM `members`'
    db.execute(q)
    members = db.fetchall()

    return render_template('membership/member_list.html',
                           members=members,
                           now=now)


######################################################################

@bp.route('/member_count', methods=('GET', 'POST'))
def member_count():
    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    status = [238,5,209,29,55,83]
    summary = [[4,40.00],[43,1435.00],[192,10220.00]]
    details = [[4,10.00,40.00],[14,30.00,420.00],[29,35.00,1015.00],[68,50.00,3400.00],[124,55.00,6820.00]]
    seniors = [['May 29, 2009',112,'Craig Mclean'],
               ['May 29, 2009',87,'John Jardine'],
               ['November 23, 2009',21,'Kirk Werklund'],
               ['February 23, 2010',102,'Alan Ferguson'],
               ['February 1, 2011',41,'Matt Freund'],
               ['February 15, 2011',50,'Tony Grimes'],
               ['March 15, 2011',89,'Brian Queen'],
               ['November 29, 2011',81,'Jamie Frost'],
               ['January 19, 2012',46,'Calvenn Tsuu'],
               ['January 24, 2012',51,'Thomas Terashima']]
    history = [['2018-07',240,45.35,4,44,192],
               ['2018-06',246,46.18,4,44,198],
               ['2018-05',247,44.78,4,44,199],
               ['2018-04',250,46.90,4,46,200],
               ['2018-03',251,45.23,4,48,199],
               ['2018-02',243,44.31,5,46,192],
               ['2018-01',236,44.24,5,40,191],
               ['2017-12',222,45.38,5,40,177],
               ['2017-11',225,45.82,4,44,177],
               ['2017-10',227,46.03,5,44,178]]


    return render_template('membership/member_count.html',now=now,
                           payment_status=status,
                           rate_summary=summary,
                           rate_details=details,
                           senior_members=seniors,
                           membership_history=history)
