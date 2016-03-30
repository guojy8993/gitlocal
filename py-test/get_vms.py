#! /usr/bin/python

import MySQLdb
import os

mysql_host = "10.160.0.108"
mysql_db = "nova"
mysql_user = "nova"
mysql_passwd = "87da3417bb3a42ee"
mysql_port = 3306
mysql_charset = "utf8"

def get_host():
    return os.environ['HOSTNAME']

def query_db_of_local_vms():
    """ query controller node db for information about vms running on local host """
    conn = None
    try:
        conn = MySQLdb.connect(host=mysql_host,
                               user=mysql_user,
                               passwd=mysql_passwd,
                               db=mysql_db,
                               port=mysql_port,
                               charset=mysql_charset)
    except Exception as e:
        #LOG.error("Fail to connect mysql .")
        raise e
    else:
        #LOG.info("Connect to mysql .")
        print "*****"

    local_compute_name = get_host()
    sql = "SELECT vcpus,uuid FROM instances WHERE host='%s' AND deleted=0"%local_compute_name
    vms = {}
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        for item in result:
            vms.update({item[1]:item[0]})
    except Exception as ex:
        #LOG.error("Exception happens while querying mysql.")
        raise ex
    else:
        return vms

if __name__ == "__main__":
	result = query_db_of_local_vms()
        print result
