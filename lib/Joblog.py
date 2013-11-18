#!/usr/bin/env python
#encoding=utf8

import MySQLdb;

class Joblog:
    def __init__(self, host, uid, pwd, db):
        '''Host, user id, password, db name is required.'''
        if not host or not uid or not pwd or not db:
            raise Exception(self.__init__.__doc__);
        self.host = host;
        self.uid = uid;
        self.pwd = pwd;
        self.db = db;
        self.conn = None;

    def _connect(self):
        self.conn = MySQLdb.connect(self.host, self.uid, self.pwd, self.db);


    def _exec_cmd(self, sql, *params):
        '''Internal method to execute a sql.'''
        cursor = None;
        try:
            self._connect();
            cursor = self.conn.cursor();
            cursor.execute(sql, tuple(params));
            self.conn.commit()
            return cursor.rowcount;
        except:
            raise Exception, 'Operational Error';
        finally:
            if cursor: cursor.close();
            if self.conn: self.conn.close();
        return 0;


    def insert_start_record(self, job_id, job_type, running_ip):
        '''Insert/updates record at job beginning'''
        sql='INSERT INTO job_log (job_id,job_type,start_time,running_ip,last_processed_time,last_okay_processed_record_count,last_failed_processed_record_count) VALUES (%s, %s, now(), %s, now(), 0, 0) ON DUPLICATE KEY UPDATE start_time=now(),last_processed_time=now(),last_okay_processed_record_count=0,last_failed_processed_record_count=0'
        return self._exec_cmd(sql, job_id, job_type, running_ip)


    def update_end_record(self, job_id, ok_count, fail_count):
        '''Updates record after job finishes'''
        sql='UPDATE job_log SET last_processed_time=now(),last_okay_processed_record_count=%s,last_failed_processed_record_count=%s WHERE job_id=%s'
        self._exec_cmd(sql, ok_count, fail_count, job_id)
        sql='replace into job_log_history(job_id, job_type, start_time, running_ip, last_processed_time, \
            last_okay_processed_record_count, last_failed_processed_record_count) select job_id, job_type, start_time, running_ip, last_processed_time, \
            %s, %s from job_log where job_id = %s' 
        return self._exec_cmd(sql, ok_count, fail_count, job_id)



#Test
if __name__=='__main__':
    print 'initing joblog...';
    joblog = Joblog('10.255.255.22', 'writeuser', 'ddbackend', 'joblog');
    #joblog = Joblog('localhost', 'root', 'password', 'joblog');
    print 'insert start record...';
    cnt = joblog.insert_start_record(111111, 1, '192.168.101.151');
    print cnt;
    if not cnt:
        print 'insert failed.';
    else:print 'ok';
    print 'update end record...';
    if not joblog.update_end_record(111111, 10, 0):
        print 'update failed.';
    else:print 'ok';
