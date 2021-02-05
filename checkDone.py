#!/usr/bin/env python3

from model import model
import os
import time

DATABASE = '/opt/algebra/database/results.db'

def doneToday(model):
  chkToday=model.isResultForDay(time.strftime("%Y-%m-%d"))  
  if chkToday == True:
    print("YES")
    return True
  else:
    print("NO")
    return False

if __name__ == '__main__':
  model = model(DATABASE)
  if doneToday(model):
    print("OK")
  else:
    print("INTERNET OFF!")
    os.system("salt 'tc600' cmd.run 'route delete 0.0.0.0'")

