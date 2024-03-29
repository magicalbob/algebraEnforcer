#!/usr/bin/env python3
""" module to support db model for algebra questions """

from sqlite3 import dbapi2 as sqlite3
import syslog

class Model():
    """ db model for algebra questions """
    def __init__(self, db_name):
        """ open db """
        self.db_name = db_name
        self.sqlite_db = None
        self.get_db()

    def get_db(self):
        """Opens a new database connection if there is none yet for the
        current application context.
        """
        if self.sqlite_db is None:
            sqlite_db = sqlite3.connect(self.db_name,check_same_thread=False)
            sqlite_db.row_factory = sqlite3.Row
            self.sqlite_db = sqlite_db

    def init_db(self, schema):
        """Creates the database tables."""
        self.sqlite_db.cursor().executescript(schema.read())
        self.sqlite_db.commit()

    def close_db_connection(self):
        """Closes the database again at the end of the request."""
        if self.sqlite_db is not None:
            self.sqlite_db.close()
            self.sqlite_db = None

    def is_result_for_day(self, the_day):
        """ check if done for today or not """
        self.get_db()
        cur = self.sqlite_db.execute(
            'select count(1) from results where timestamp >= ? and question_cnt = 3',
            [the_day])
        cur_result = cur.fetchall()
        if len(cur_result) < 1:
            return False

        if cur_result[0][0] == 0:
            return False

        return True

    def create_results(self,ip_addr,timestamp):
        """ create results for ip in database """
        self.get_db()
        self.sqlite_db.execute(
            'insert into results (ip_addr, '      + \
            '                     timestamp, '    + \
            '                     question_cnt, ' + \
            '                     q1_wrong_cnt, ' + \
            '                     q2_wrong_cnt, ' + \
            '                     q3_wrong_cnt) ' + \
            '            values (?, ?, 0, 0, 0, 0)',
            [ip_addr, timestamp])
        self.sqlite_db.commit()

    def q1_wrong(self,ip_addr,timestamp,q_type):
        """ answer 1 was wrong, record it """
        self.get_db()
        syslog.syslog("update results question_cnt=1, "         + \
                      " set q1_wrong_cnt = q1_wrong_cnt + 1, "  + \
       " q1_type = %s where ip_addr = '%s' and  timestamp = '%s'" % (q_type, ip_addr, timestamp))
        self.sqlite_db.execute("update results set question_cnt=1, " + \
        "   q1_wrong_cnt = q1_wrong_cnt + 1, " + \
        "   q1_type = %s where ip_addr = '%s' and    timestamp = '%s'" % (
                                                        q_type,
                                                        ip_addr,
                                                        timestamp
                                                       )
                              )
        self.sqlite_db.commit()

    def q2_wrong(self,ip_addr,timestamp, q_type):
        """ answer 2 was wrong, record it """
        self.get_db()
        self.sqlite_db.execute("update results set question_cnt=2, "    + \
        "q2_wrong_cnt = q2_wrong_cnt + 1, "      + \
        "q2_type = %s where ip_addr = '%s' and timestamp = '%s'" % (q_type, ip_addr, timestamp))
        self.sqlite_db.commit()

    def q3_wrong(self,ip_addr,timestamp, q_type):
        """ answer 3 was wrong, record it """
        self.get_db()
        self.sqlite_db.execute("update results set question_cnt=3, " + \
        "q3_wrong_cnt = q3_wrong_cnt + 1, " + \
        "q3_type = %s where ip_addr = '%s' and timestamp = '%s'" % (
                                                     q_type,
                                                     ip_addr,
                                                     timestamp
                                                    )
                              )
        self.sqlite_db.commit()

    def q1_right(self,ip_addr,timestamp, q1_timestamp, q_type):
        """ answer 1 was right, record it """
        self.get_db()
        self.sqlite_db.execute("update results set question_cnt=1, " + \
        "q1_timestamp = '%s', q1_type = %s where ip_addr = '%s' and timestamp = '%s'" % (
         q1_timestamp,
         q_type,
         ip_addr,
         timestamp
        ))
        self.sqlite_db.commit()

    def q2_right(self,ip_addr,timestamp, q2_timestamp, q_type):
        """ answer 2 was right, record it """
        self.get_db()
        self.sqlite_db.execute("update results set question_cnt=3, " + \
        "q2_timestamp = '%s', q2_type = %s where ip_addr = '%s' and timestamp = '%s'" % (
         q2_timestamp, q_type, ip_addr, timestamp))
        self.sqlite_db.commit()

    def q3_right(self,ip_addr,timestamp, q3_timestamp, q_type):
        """ answer 3 was right, record it """
        self.get_db()
        self.sqlite_db.execute("update results set question_cnt=3, " + \
        "q3_timestamp = '%s', q3_type = %s where ip_addr = '%s' and timestamp = '%s'" % (
         q3_timestamp, q_type, ip_addr, timestamp))
        self.sqlite_db.commit()
