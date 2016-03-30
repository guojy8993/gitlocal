#! /usr/bin/python
# -*- coding:utf-8 -*-

from oslo.config import cfg

OPTS = [
	cfg.StrOpt('host',default='10.160.0.101',help=("remote database ip addr")),
	cfg.IntOpt('port',default=3306,help=("port that database service listens to. e.g 3306 for mysql,1521 for oracle")),
	cfg.StrOpt('user',default='nova',help=("database user")),
	cfg.StrOpt('passwd',default='',help=("database passwd for $user"),secret=True),
	cfg.StrOpt('dbname',help=("database name")),
	cfg.ListOpt('db_restrain_keys',default=['unique','primary',],help=("db_restrain_keys")),
	cfg.BoolOpt('debug',default=False,help=("whether run in debug mode"))
]

ROOT_HELPER_OPTS = [
	cfg.StrOpt('root_helper', default='sudo',help=('Root helper application.'))
]

def main():

        try:
		cfg.CONF(host='10.160.0.108')
	except Exception:
		print "Opts not registered"
		
	cfg.CONF.register_opts(OPTS)
	cfg.CONF.set_default(name='dbname',default='mysql')
        print cfg.CONF.debug
	cfg.CONF.host='10.160.0.119'
        print cfg.CONF.host
	print cfg.CONF.dbname
	print cfg.CONF.db_restrain_keys
        			
	cfg.CONF.register_opts(ROOT_HELPER_OPTS,'Agent')
	print cfg.CONF.Agent.root_helper
	

if __name__ == "__main__":
	main()
