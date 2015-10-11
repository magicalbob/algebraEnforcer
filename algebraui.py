#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Algebra Tester
    ~~~~~~~~~~~~~~

    Tortue by algebra.

"""

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
from algebra import Algebra
import os
import syslog
import datetime
from model import model

# configuration
DEBUG = True
SECRET_KEY = 'development key'
DATABASE = '/opt/algebra/database/results.db'
DB_SCHEMA = 'schema.sql'

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
    model.create_results(request.environ['REMOTE_ADDR'],session['_timestamp'])
    return redirect(url_for('show_question'))

def makeQ(new_quest):
    xAlg = Algebra()
    if new_quest == True:
      xAlg.makeQuestion()
      session['_alg_disp_1']=xAlg.disp1
      session['_alg_disp_2']=xAlg.disp2
      session['_alg_x']=xAlg.x
      session['_alg_y']=xAlg.y
    else:
      xAlg.disp1=session['_alg_disp_1']
      xAlg.disp2=session['_alg_disp_2']
      xAlg.x=session['_alg_x']
      xAlg.y=session['_alg_y']
    syslog.syslog("Algebra: New question { Q1: %s, Q2: %s, X = %s, Y = %s } from %s" % (session['_alg_disp_1'], session['_alg_disp_2'], session['_alg_x'], session['_alg_y'], request.environ['REMOTE_ADDR']))
    print "Q1: %s" % (session['_alg_disp_1'])
    print "Q2: %s" % (session['_alg_disp_2'])
    print "X: %s" % (session['_alg_x'])
    print "Y: %s" % (session['_alg_y'])

    return xAlg

@app.route('/question',methods=['GET'])
def show_question():
    xAlg = makeQ(True)    
    return render_template('show_question.html',qNum=session['_q_count'],formula_1=xAlg.disp1,formula_2=xAlg.disp2)

@app.route('/question',methods=['POST'])
def show_answer():
  error = None
  if (str(request.form['answerX']) == str(session['_alg_x']) and 
      str(request.form['answerY']) == str(session['_alg_y'])):
    if session['_q_count'] == 1:
      model.q1_right(request.environ['REMOTE_ADDR'],
                     session['_timestamp'],
                     datetime.datetime.now()
                    )
    elif session['_q_count'] == 2:
      model.q2_right(request.environ['REMOTE_ADDR'],
                     session['_timestamp'],
                     datetime.datetime.now()
                    )
    elif session['_q_count'] == 3:
      model.q3_right(request.environ['REMOTE_ADDR'],
                     session['_timestamp'],
                     datetime.datetime.now()
                    )
    else:
      syslog("Just got answer for question %s ... something is wrong!" %
             (session['_q_count']))
    xAlg = makeQ(True)   
    session['_q_count']+=1 
    if session['_q_count'] > 3:
      session['_q_count']=1
      os.system("salt 'tc600' cmd.run 'route add 0.0.0.0 mask 0.0.0.0 192.168.2.1'")
      syslog.syslog("Algebra: Internet restored by %s" % (request.environ['REMOTE_ADDR']))
      return render_template('well_done.html')
    else:
      flash("Well done that's right. Here's another one.")
  else:
    if session['_q_count'] == 1:
      model.q1_wrong(request.environ['REMOTE_ADDR'],
                     session['_timestamp']
                    )
    elif session['_q_count'] == 2:
      model.q2_wrong(request.environ['REMOTE_ADDR'],
                     session['_timestamp']
                    )
    elif session['_q_count'] == 3:
      model.q3_wrong(request.environ['REMOTE_ADDR'],
                     session['_timestamp']
                    )
    else:
      syslog("Just got question %s wrong ... something is really wrong!" %
             (session['_q_count']))
    xAlg = makeQ(False)    
    flash("Oops! That is wrong. Try again.")

  return render_template('show_question.html',qNum=session['_q_count'],error=error,formula_1=xAlg.disp1,formula_2=xAlg.disp2)

if __name__ == '__main__':
    model = model(app.config['DATABASE'])
    model.init_db(app.open_resource(DB_SCHEMA, mode='r'))
    app.run(host='0.0.0.0',port=5001)
