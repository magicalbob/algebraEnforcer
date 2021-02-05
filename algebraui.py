#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Algebra Tester
    ~~~~~~~~~~~~~~

    Torture by algebra.

"""

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
from algebra import Algebra
import os
import syslog
import datetime
from model import model
import pickle
from checkDone import doneToday
import yaml

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

#@app.teardown_appcontext
#def close_app(exception):
#  pass

@app.route('/',methods=['GET','POST'])
def start_up():
  if request.method == 'GET':
    syslog.syslog("Algebra: Request for '/' from %s" % (request.environ['REMOTE_ADDR']))
    return render_template('start_up.html')
  else:
    session['_q_count']=1
    session['_timestamp']=str(datetime.datetime.now())[:19]
    print("DEBUG 1")
    model.create_results(request.environ['REMOTE_ADDR'],session['_timestamp'])
    return redirect(url_for('show_question'))

def makeQ(new_quest):
    if new_quest == True:
      xAlg = Algebra()
      xAlg.makeQuestion()
      session['_alg_obj']=pickle.dumps(xAlg,-1)
    else:
      xAlg = pickle.loads(session['_alg_obj'])

    if xAlg.q_type == 1:
      syslog.syslog("Algebra: New simultaneous equations { Q1: %s, Q2: %s, X = %s, Y = %s } from %s" % (xAlg.disp1, xAlg.disp2, xAlg.x, xAlg.y, request.environ['REMOTE_ADDR']))
      print("Q1: %s" % (xAlg.disp1))
      print("Q2: %s" % (xAlg.disp2))
      print("X: %s" % (xAlg.x))
      print("Y: %s" % (xAlg.y))
    elif xAlg.q_type == 2:
      syslog.syslog("Algebra: New expand / simplify { Q: %s, X^2 = %s, XY = %s, Y^2 = %s } from %s" % (xAlg.expQuestion, xAlg.x_squared, xAlg.x_y, xAlg.y_squared, request.environ['REMOTE_ADDR']))
      print("Q: %s" % (xAlg.expQuestion))
      print("X^2: %s" % (xAlg.x_squared))
      print("XY: %s" % (xAlg.x_y))
      print("Y^2: %s" % (xAlg.y_squared))
    elif xAlg.q_type == 3:
      syslog.syslog("Algebra: New heron { (%d,%d,%d), p = %f, A = %s } from %s" % (xAlg.side[0], xAlg.side[1], xAlg.side[2], xAlg.perm, xAlg.heron, request.environ['REMOTE_ADDR']))

    return xAlg

@app.route('/checkstat',methods=['GET'])
def check_down():
  if doneToday(model):
    return render_template('algebra_done.html')
  else:
    return render_template('algebra_not_done.html')

@app.route('/question',methods=['GET'])
def show_question():
    xAlg = makeQ(True)   
    if xAlg.q_type == 1: 
      return render_template('show_question.html',
                             qNum=session['_q_count'],
                             formula_1=xAlg.disp1,
                             formula_2=xAlg.disp2)
    elif xAlg.q_type == 2:
      return render_template('show_expand.html',
                             qNum=session['_q_count'],
                             unexpanded=xAlg.expQuestion)
    elif xAlg.q_type == 3:
      return render_template('show_heron.html',
                             qNum=session['_q_count'],
                             side_a=xAlg.side[0],
                             side_b=xAlg.side[1],
                             side_c=xAlg.side[2])

@app.route('/question',methods=['POST'])
def show_answer():
  error = None
  xAlg = pickle.loads(session['_alg_obj'])
  isRight=False
  if xAlg.q_type == 1:
    if (str(request.form['answerX']) == str(xAlg.x) and 
        str(request.form['answerY']) == str(xAlg.y)):
      isRight=True
  elif xAlg.q_type == 2:
    try:
      if (str(int(request.form['sign1'])*int(request.form['answerX2'])) == 
          str(xAlg.x_squared) and
          str(int(request.form['sign2'])*int(request.form['answerXY'])) == 
          str(xAlg.x_y) and
          str(int(request.form['sign3'])*int(request.form['answerY2'])) == 
          str(xAlg.y_squared)):
        isRight=True
    except:
      pass
  elif xAlg.q_type == 3:
    print("DEBUG HERON: %.4f" % (float(request.form['answerA'])))
    if (("%.4f" % (float(request.form['answerA']))) == xAlg.heron):
      isRight=True

  if isRight == True: 
    if session['_q_count'] == 1:
      print("DEBUG 2")
      model.q1_right(request.environ['REMOTE_ADDR'],
                     session['_timestamp'],
                     datetime.datetime.now(),
                     xAlg.q_type
                    )
    elif session['_q_count'] == 2:
      print("DEBUG 3")
      model.q2_right(request.environ['REMOTE_ADDR'],
                     session['_timestamp'],
                     datetime.datetime.now(),
                     xAlg.q_type
                    )
    elif session['_q_count'] == 3:
      print("DEBUG 4")
      model.q3_right(request.environ['REMOTE_ADDR'],
                     session['_timestamp'],
                     datetime.datetime.now(),
                     xAlg.q_type
                    )
    else:
      syslog("Just got answer for question %s ... something is wrong!" %
             (session['_q_count']))
    session['_q_count']+=1 
    if session['_q_count'] > 3:
      session['_q_count']=1
      os.system(INTERNET_RESTORE)
      syslog.syslog("Algebra: Internet restored by %s" % (request.environ['REMOTE_ADDR']))
      return render_template('well_done.html')
    else:
      xAlg = makeQ(True)   
      flash("Well done that's right. Here's another one.")
  else:
    if session['_q_count'] == 1:
      print("DEBUG 5")
      model.q1_wrong(request.environ['REMOTE_ADDR'],
                     session['_timestamp'],
                     xAlg.q_type
                    )
    elif session['_q_count'] == 2:
      print("DEBUG 6")
      model.q2_wrong(request.environ['REMOTE_ADDR'],
                     session['_timestamp'],
                     xAlg.q_type
                    )
    elif session['_q_count'] == 3:
      print("DEBUG 7")
      model.q3_wrong(request.environ['REMOTE_ADDR'],
                     session['_timestamp'],
                     xAlg.q_type
                    )
    else:
      syslog("Just got question %s wrong ... something is really wrong!" %
             (session['_q_count']))
    xAlg = makeQ(False)    
    flash("Oops! That is wrong. Try again.")
  
  if xAlg.q_type == 1: 
    return render_template('show_question.html',
                           qNum=session['_q_count'],
                           error=error,
                           formula_1=xAlg.disp1,
                           formula_2=xAlg.disp2)
  elif xAlg.q_type == 2:
    return render_template('show_expand.html',
                           qNum=session['_q_count'],
                           error=error,
                           unexpanded=xAlg.expQuestion)
  elif xAlg.q_type == 3:
    return render_template('show_heron.html',
                           qNum=session['_q_count'],
                           side_a=xAlg.side[0],
                           side_b=xAlg.side[1],
                           side_c=xAlg.side[2])

if __name__ == '__main__':
    model = model(app.config['DATABASE'])
    model.init_db(app.open_resource(DB_SCHEMA, mode='r'))
    app.run(host='0.0.0.0',port=5001)
