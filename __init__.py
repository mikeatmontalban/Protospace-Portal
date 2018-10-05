import os

from flask import Flask, render_template, url_for, flash, redirect

from flaskext.mysql import MySQL

import time
from time import strftime,localtime

mysql = MySQL()

from flaskr.db import get_db

test_config = None

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

app.config['MYSQL_DATABASE_USER'] = '<obliterated>'
app.config['MYSQL_DATABASE_PASSWORD'] = '<obliterated>'
app.config['MYSQL_DATABASE_DB'] = '<obliterated>'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8'

mysql.init_app(app)


if test_config is None:
# load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
# load the test config if passed in
    app.config.from_mapping(test_config)

try:
    os.makedirs(app.instance_path)
except OSError:
        pass
    
######################################################################

@app.route('/')
@app.route('/home')
def home():

    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    class_list = []
    
    db = get_db()
    class_q = 'SELECT class_id,course_id,class_date_time,confirmed,available FROM `class_history` WHERE `class_date_time` >= CURDATE()'
    db.execute(class_q)
    classes = db.fetchall()
    for row in classes:
        q = 'SELECT course_title FROM `courses` where `course_id` ="' + str(row[1]) + '"'
        db.execute(q)
        course = db.fetchone()
        if course is None:
            flash('course_id: ' + course_id + ' not found.')
        else:
            class_list.append([str(course[0]),row[0],row[1],str(row[2]),row[3],row[4]])
            
    return(render_template('training/show_upcoming_classes.html',
                           role='',
                           now=now,
                           class_list=class_list))
        
######################################################################

@app.route('/access_info')
def access_info():
    now = str(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

    return(render_template('access_info.html',now=now))


from . import db
db.init_app(app)

from . import auth
app.register_blueprint(auth.bp)

from . import member
app.register_blueprint(member.bp)

from . import admin
app.register_blueprint(admin.bp)

from . import training
app.register_blueprint(training.bp)

from . import membership
app.register_blueprint(membership.bp)

from . import money
app.register_blueprint(money.bp)

if __name__ == "__main__":
    app.run()
