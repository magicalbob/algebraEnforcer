#!/usr/bin/python

from model import model
import os

DATABASE = '/opt/algebra/database/results.db'

def doneToday(model):
  chkToday=model.isResultForDay('2015-11-03')  
  if chkToday == True:
    print "YES"
  else:
    print "NO"
    os.system("salt 'tc600' cmd.run 'route delete 0.0.0.0'")

model = model(DATABASE)
doneToday(model)
