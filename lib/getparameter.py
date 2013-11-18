#!/usr/bin/evn python
#encoding = utf8

##Author  : maorui
##Date    : 2012-07-26
##File    : getparameter.py


import sys
from getopt import getopt
from ConfigParser import RawConfigParser
from ConfigParser import *
import logging
import logging.config

from Joblog import Joblog

def get_path():
    
    """
    get opt parameter
    """
    try:
        opts, val = getopt(sys.argv[1:], 'c:', ['path='])
    except getopt.GetoptError , ex:
        sys.stderr.write('%s' % ex)
    conf_path = ''
    for opt, var in opts:
        if opt in ['-c']:
            conf_path = var
        if opt in ['--path']:
            conf_path = var
    if not conf_path:
        print "you should input -c conf_path or --path conf_path"
        return
    return conf_path   

def get_monitor(conf_path,title):
    """
    get monitor object
    """
    connfile = '%s/conf/connect.cfg' % (conf_path)    
    config = RawConfigParser()  
    config.read(connfile)
    joblog = None
    try: 
        host   = config.get(title, 'host')
        uid    = config.get(title, 'user')
        pwd    = config.get(title, 'password')
        db     = config.get(title, 'database')
        joblog = Joblog(host, uid, pwd, db)
        
    except (NoSectionError,NoOptionError,IOError), ex:  
        sys.stderr.write('%s' % ex)  
        return 
    
    return joblog

    asdfasdf
