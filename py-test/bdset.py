import MySQLdb
import os
import signal
import shlex
import subprocess
from eventlet.green import subprocess as green_subprocess
from eventlet import greenthread
import logging
import string
import time


mysql_host = "10.160.0.101"
mysql_db = "nova"
mysql_user = "nova"
mysql_passwd = "29ef61f5f8a443d7"
mysql_port = 3306
mysql_charset = "utf8"

public_interface = "ens160"

LOG = logging.getLogger(__name__)

def create_process(cmd, root_helper=None, addl_env=None):
    if root_helper:
        cmd = shlex.split(root_helper) + cmd
    cmd = map(str, cmd)
    LOG.debug(("Running command: %s"), cmd)
    env = os.environ.copy()
    if addl_env:
        env.update(addl_env)
    obj = subprocess_popen(cmd, shell=False,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=env)
    return obj, cmd

def execute(cmd, root_helper=None, process_input=None, addl_env=None,
            check_exit_code=True, return_stderr=False):
    try:
        obj, cmd = create_process(cmd, root_helper=root_helper,
                                  addl_env=addl_env)
        _stdout, _stderr = (process_input and
                            obj.communicate(process_input) or
                            obj.communicate())
        obj.stdin.close()
        m = ("\nCommand: %(cmd)s\nExit code: %(code)s\nStdout: %(stdout)r\n"
              "Stderr: %(stderr)r") % {'cmd': cmd, 'code': obj.returncode,
                                       'stdout': _stdout, 'stderr': _stderr}
        LOG.debug(m)
        if obj.returncode and check_exit_code:
            raise RuntimeError(m)
    finally:
        greenthread.sleep(0)
    return return_stderr and (_stdout, _stderr) or _stdout


def _subprocess_setup():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def subprocess_popen(args, stdin=None, stdout=None, stderr=None, shell=False,
                     env=None):
    return green_subprocess.Popen(args, shell=shell, stdin=stdin, stdout=stdout,
                            stderr=stderr, preexec_fn=_subprocess_setup,
                            close_fds=True, env=env)


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
        LOG.info("Connect to mysql .")
    local_compute_name = get_host()

    sql = "select fi.address as ip,it.rxtx_factor as bandwidth from instances as i,instance_types as it, \
           fixed_ips as fi where i.host='%s' and i.deleted=0 and i.instance_type_id=it.id and it.deleted=0 \
           and fi.instance_uuid=i.uuid and fi.deleted=0 and fi.network_id=3 "%local_compute_name

    retv = {}
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        for item in result:
            retv.update({item[0]:item[1]})
    except Exception as ex:
        #LOG.error("Exception happens while querying mysql.")
        raise ex
    else:
        return retv

def reset_tc():
    try:
        reset_root_del = "tc qdisc del dev %s root handle 1: cbq avpkt 1000 bandwidth 1024Mbit"%public_interface
        execute(reset_root_del,root_helper=None)
    except Exception as e:
        pass
    reset_root_add = "tc qdisc add dev %s root handle 1: cbq avpkt 1000 bandwidth 1024Mbit"%public_interface
    execute(reset_root_add,root_helper=None)

def get_host():
    return os.environ['HOSTNAME']

def apply_tc(vmDetails):
    reset_tc()
    for ip,bandwidth in vmDetails.iteritems():
        tmpip = "".join(ip.split("."))
        classid = tmpip[len(tmpip)-5:len(tmpip)-1]
        print ip,classid
        qclassAdd = "tc class add dev %s parent 1: classid 1:%s cbq rate %dMbit \
                    allot 1500 prio 5 bounded isolated"%(public_interface,classid,bandwidth)
        print qclassAdd

        qfilterAdd = "tc filter add dev %s parent 1: protocol ip prio 16 u32  \
                     match ip src %s flowid 1:%s"%(public_interface,ip,classid)
        print qfilterAdd

        qdiscAdd = "tc qdisc add dev %s parent 1:%s sfq perturb 10"%(public_interface,classid)
        print qdiscAdd



if __name__ == "__main__":
	vms = query_db_of_local_vms()
        apply_tc(vms)
