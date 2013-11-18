#!/usr/bin/env python
#encoding:utf-8

##Author:maorui
##Date  :2012-11-13
##Modify：weiweina  2013-2-21
##Filename:  exam_ticket_scalper.py
##content：向计数器发送订单信息，判断是否黄牛订单
##
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import threading
import os
from ConfigParser import RawConfigParser
from ConfigParser import *
import logging
import logging.config

sys.path.append('../lib')
from data_access_object import DataObject
from db_factory import DBFactory

#定义IP addr的映射表 其中对应于数据库中的use_ip_addr_history2
IP_ID_LIST = []


class IdentifyTelphoneRecharge(object):
	
	def __init__(self, conf_path = '..'):
		'''
		初始化配置文件
		'''
		#数据库、redis等配置
		self.conncfg = '%s/conf/connect.cfg' % (conf_path)
		#日志文件配置 
		self.logcfg = '%s/conf/logger.conf' % (conf_path)
		logging.config.fileConfig(self.logcfg)
		self.logger = logging.getLogger('Request')
		#sql语句配置
		self.sqlcfg = '%s/conf/sql.cfg' % (conf_path)

		self.config = RawConfigParser()
		self.config.read(self.conncfg)
		self.con_lock = threading.Lock()
		self.sqlfig = RawConfigParser()
		self.sqlfig.read(self.sqlcfg)		

		self.custid_ip_count = 0
		self.ip_in_db = 0
		self.tel_in_spamlist = 0
		self.permid_custid_count = 0
		self.tel_total = 0
		self.tel_custid_count = 0
		
		#self.get_threshold_value('threshold_value')

	def dbserver_conn(self, section = 'antifraud_conn'):
		'''
		连接历史成功订单数据库
		'''
		
		dbserver = None
		try:
			dbtype = self.config.get(section, 'dbtype')
			host = self.config.get(section, 'host')
			port = self.config.get(section, 'port')
			user = self.config.get(section, 'user')
			password = self.config.get(section, 'password')
			database = self.config.get(section, 'database')

			dbserver = DBFactory.Connect(dbtype = dbtype, host = host, database = database, charset = 'utf8',user = user, password = password, port = port)
		
		except Exception, ex:
			self.logger.error(ex)
			raise Exception, ex
		return dbserver
	
	def get_data_from_DB(self, section = 'SELECT', sql_str = 'get_ip_addr'):
		'''
		获取IP addr对应的映射表到IP_ID_LIST中
		'''
		try:
			dbserver = self.dbserver_conn()
			sql = self.sqlfig.get(section, sql_str)
			dbserver.execute(sql)
			
			while True:

				records = dbserver.fetchmany(1000)
				if not records:
					break
				if len(records) == 0:
					break
			
				for record in records:
					id = record[0]
					beg_ip = record[1]
					IP_ID_LIST.insert(id-1, beg_ip)		
		except Exception, ex:
			self.logger.error(ex)
			raise Exception, ex
		finally:
			if dbserver:
				dbserver.close()
	
	def tel_in_hisDB(self,section='SELECT', sql_str='get_ip_in_his',tel = '',  custid = ''):
		'''
			在历史数据库中则返回0， 不在则返回1
		'''
		flag = 0
		try:
			dbserver = self.dbserver_conn()
			sql = self.sqlfig.get(section, sql_str)
			sql = sql % (custid, tel)
			
			dbserver.execute(sql)
			
			records = dbserver.fetchmany(10)
			if len(records) == 0:
				flag = 1
			for record in records :
				print record[0]
		except Exception, ex:
			print ex
		finally:
			if dbserver:
				dbserver.close()
		return flag

	def tel_in_spam(self, database, tel):
		'''
		手机号是否在黑名单中，在则返回1， 不在则返回0
		'''
		return 0
		
	def ip_mapping_custid(self, tel):
		'''
		ip对应的custid数，若大于2返回1， 否则返回0
		'''
		return 0
	
	def permid_mapping_custid(self, permid):
		'''
		permid对应的custid数，若大于2返回1， 否则返回0
		'''
		return 0

	def tel_total(self, tel):
		'''
		tel在900s内充值金额是否大于500，若是返回1，否则返回0
		'''
		return 0

	def tel_mapping_custid(self, tel):
		'''
		tel在900s内对应的独立cust_id数是否大于2， 若是返回1， 否则返回0
		'''
		return 0

	def identify_process(self, ip = '', tel = '', permid = '', custid = '', total = 0):
		'''
		判定入口函数
		total为本次充值金额
		若拦截返回1，否则通过返回0
		'''
		ip = ip.strip()
		tel = tel.strip()
		permid = permid.strip()
		custid = custid.strip()

		if tel == '' or custid == '' :
			return 1
	
		if self.tel_in_hisDB(tel = tel, custid = custid) == 1:
			return 1
		
		if self.tel_in_spam(tel = tel) == 1:
			return 1
		
		if self.ip_mapping_custid(ip = ip) == 1:
			return 1
					
		if self.permid_mapping_custid(permid = permid) == 1:
			return 1

		if self.tel_total(tel = tel) == 1:
			return 1
		
		if self.tel_mapping_custid(tel = tel) == 1:
			return 1
							
	
		return 0



def test():
	item = IdentifyTelphoneRecharge()
	#db = item.dbserver_conn(section = 'antifraud_conn')
	flag = item.identify_process(tel = '13557170212', custid = '1000410')
	if flag == 1:
		print 'it is intreasting'
	else:
		print 'oh, my god'

if __name__ == '__main__':
	test()
