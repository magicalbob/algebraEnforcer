#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Algebra Tester
    ~~~~~~~~~~~~~~

    Torture by algebra.

"""

import datetime
import syslog
import os
import pickle
import yaml
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash
from algebra import Algebra
from model import Model
from checkDone import doneToday

# configuration
DB_SCHEMA = 'schema.sql'
with open('algebra.yaml', 'r') as confile:
    conf = yaml.safe_load(confile)
DATABASE = conf['database']
SECRET_KEY = conf['secret_key']
INTERNET_RESTORE = conf['internet_restore']

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/',methods=['GET','POST'])
def start_up():
    """ fuction to start up site """
    if request.method == 'GET':
        syslog.syslog("Algebra: Request for '/' from %s" % (request.environ['REMOTE_ADDR']))
        return render_template('start_up.html')

    session['_q_count']=1
    session['_timestamp']=str(datetime.datetime.now())[:19]
    model.create_results(request.environ['REMOTE_ADDR'],session['_timestamp'])
    return redirect(url_for('show_question'))

def make_q(new_quest):
    """ need a new question, make one """
    if new_quest:
        x_alg = Algebra()
        x_alg.make_question()
        session['_alg_obj']=pickle.dumps(x_alg,-1)
    else:
        x_alg = pickle.loads(session['_alg_obj'])

    if x_alg.q_type == 1:
        syslog.syslog(
            "Algebra: New simultaneous equations { Q1: %s, Q2: %s, X = %s, Y = %s } from %s" % (
                x_alg.disp1,
                x_alg.disp2,
                x_alg.var_x,
                x_alg.var_y,
                request.environ['REMOTE_ADDR']
               )
        )
        syslog.syslog("Q1: %s" % (x_alg.disp1))
        syslog.syslog("Q2: %s" % (x_alg.disp2))
        syslog.syslog("X: %s" % (x_alg.var_x))
        syslog.syslog("Y: %s" % (x_alg.var_y))
    elif x_alg.q_type == 2:
        syslog.syslog(
            "Algebra: New expand / simplify { Q: %s, X^2 = %s, XY = %s, Y^2 = %s } from %s" % (
                x_alg.exp_question,
                x_alg.var_x_squared,
                x_alg.var_x_y,
                x_alg.var_y_squared,
                request.environ['REMOTE_ADDR']
              )
        )
        syslog.syslog("Q: %s" % (x_alg.exp_question))
        syslog.syslog("X^2: %s" % (x_alg.var_x_squared))
        syslog.syslog("XY: %s" % (x_alg.var_x_y))
        syslog.syslog("Y^2: %s" % (x_alg.var_y_squared))
    elif x_alg.q_type == 3:
        syslog.syslog(
            "Algebra: New heron { (%d,%d,%d), p = %f, A = %s } from %s" % (
                x_alg.side[0],
                x_alg.side[1],
                x_alg.side[2],
                x_alg.perm,
                x_alg.heron,
                request.environ['REMOTE_ADDR']
            )
        )

    return x_alg

@app.route('/checkstat',methods=['GET'])
def check_down():
    """ check whether algebra has been done or not """
    if doneToday(model):
        return render_template('algebra_done.html')

    return render_template('algebra_not_done.html')

@app.route('/question',methods=['GET'])
def show_question():
    """ display the question """
    x_alg = make_q(True)
    if x_alg.q_type == 1:
        return render_template('show_question.html',
                               qNum=session['_q_count'],
                               formula_1=x_alg.disp1,
                               formula_2=x_alg.disp2)

    if x_alg.q_type == 2:
        return render_template('show_expand.html',
                               qNum=session['_q_count'],
                               unexpanded=x_alg.exp_question)

    if x_alg.q_type == 3:
        return render_template('show_heron.html',
                               qNum=session['_q_count'],
                               side_a=x_alg.side[0],
                               side_b=x_alg.side[1],
                               side_c=x_alg.side[2])

    return render_template('start_up.html')

def record_is_right(is_right,
                   q_type):
    """ function to update db with right answer """
    if is_right:
        if session['_q_count'] == 1:
            model.q1_right(request.environ['REMOTE_ADDR'],
                           session['_timestamp'],
                           datetime.datetime.now(),
                           q_type
                          )

        if session['_q_count'] == 2:
            model.q2_right(request.environ['REMOTE_ADDR'],
                           session['_timestamp'],
                           datetime.datetime.now(),
                           q_type
                          )

        if session['_q_count'] == 3:
            model.q3_right(request.environ['REMOTE_ADDR'],
                           session['_timestamp'],
                           datetime.datetime.now(),
                           q_type
                          )

def record_is_wrong(q_type):
    """ function to update db with wrong answer """
    if session['_q_count'] == 1:
        model.q1_wrong(request.environ['REMOTE_ADDR'],
                       session['_timestamp'],
                       q_type
                      )

    if session['_q_count'] == 2:
        model.q2_wrong(request.environ['REMOTE_ADDR'],
                       session['_timestamp'],
                       q_type
                      )

    if session['_q_count'] == 3:
        model.q3_wrong(request.environ['REMOTE_ADDR'],
                       session['_timestamp'],
                       q_type
                      )

def check_is_right(x_alg):
    """ check if the answer is right """
    is_right=False
    if x_alg.q_type == 1:
        if (str(request.form['answerX']) == str(x_alg.var_x) and
            str(request.form['answerY']) == str(x_alg.var_y)):
            is_right=True

    if x_alg.q_type == 2:
        try:
            if (str(int(request.form['sign1'])*int(request.form['answerX2'])) ==
                str(x_alg.var_x_squared) and
                str(int(request.form['sign2'])*int(request.form['answerXY'])) ==
                str(x_alg.var_x_y) and
                str(int(request.form['sign3'])*int(request.form['answerY2'])) ==
                str(x_alg.var_y_squared)):
                is_right=True
        except ValueError as an_exception:
            syslog.syslog("ValueError %s" % (an_exception))
        except ZeroDivisionError as an_exception:
            syslog.syslog("ValueError %s" % (an_exception))

    if x_alg.q_type == 3:
        syslog.syslog("HERON: %.4f" % (float(request.form['answerA'])))
        if ("%.4f" % (float(request.form['answerA']))) == x_alg.heron:
            is_right=True

    return is_right

@app.route('/question',methods=['POST'])
def show_answer():
    """ show the answer """
    error = None
    x_alg = pickle.loads(session['_alg_obj'])
    is_right = check_is_right(x_alg)

    record_is_right(is_right,
                   x_alg.q_type)

    if is_right:
        session['_q_count']+=1
        if session['_q_count'] > 3:
            session['_q_count']=1
            os.system(INTERNET_RESTORE)
            syslog.syslog("Algebra: Internet restored by %s" % (request.environ['REMOTE_ADDR']))
            return render_template('well_done.html')

        x_alg = make_q(True)
        flash("Well done that's right. Here's another one.")
    else:
        record_is_wrong(x_alg.q_type)

        x_alg = make_q(False)
        flash("Oops! That is wrong. Try again.")

    if x_alg.q_type == 1:
        return render_template('show_question.html',
                               qNum=session['_q_count'],
                               error=error,
                               formula_1=x_alg.disp1,
                               formula_2=x_alg.disp2)

    if x_alg.q_type == 2:
        return render_template('show_expand.html',
                               qNum=session['_q_count'],
                               error=error,
                               unexpanded=x_alg.exp_question)

    if x_alg.q_type == 3:
        return render_template('show_heron.html',
                               qNum=session['_q_count'],
                               side_a=x_alg.side[0],
                               side_b=x_alg.side[1],
                               side_c=x_alg.side[2])

    return render_template('start_up.html')

if __name__ == '__main__':
    model = Model(app.config['DATABASE'])
    model.init_db(app.open_resource(DB_SCHEMA, mode='r'))
    app.run(host='0.0.0.0',port=5002)
