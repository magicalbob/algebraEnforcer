#!/usr/bin/env python3
""" a module to check whether algebra has been done today """

import time
import yaml
from model import Model

# configuration
with open('algebra.yaml', 'r') as confile:
    conf = yaml.safe_load(confile)
DATABASE = conf['database']

def done_today(db_model):
    """ check whether todays's algebra has been done """
    chk_today=db_model.is_result_for_day(time.strftime("%Y-%m-%d"))
    if chk_today:
        print("YES")
        return True

    print("NO")
    return False

if __name__ == '__main__':
    model = Model(DATABASE)
    if done_today(model):
        print("OK")
    else:
        print("INTERNET OFF!")
