#! /usr/bin/python

from wsgiref.simple_server import make_server
import json
import os
import threading
from subprocess import Popen,PIPE

reserved_ip = "10.160.0.108"
reserved_http_method = "POST"
resv_file = "/etc/hosts"
bash_file = "/root/client-key.sh"
ip_file = "/root/IP"
puppet_site = "/etc/puppet/manifests/site.pp"
init_ha_IP = "/etc/puppet/modules/haproxy/files/haproxy/IP"
mysql_pp_dir = "/etc/puppet/manifests/node/db/"
mysql_bash = "/etc/puppet/modules/mariadb/files/db.sh"
web_pp_dir = "/etc/puppet/manifests/node/apache/"
nginx_dir = "/etc/puppet/manifests/node/nginx/"
HA_INC_IPs = "/etc/puppet/modules/haproxy-inc/files/haproxy/IP"
web_zip = "/webroot/"

def log(msg=None):
	f = open("/var/log/puppetmaster.log","a")
        if msg is None:
		msg = ""
	f.write("%s\n"%msg)
	f.close()	

def get_local():
	f = open("/etc/hostname","r")
	tmp = f.read()
        f.close()
        return tmp.strip()

def unzip():
	web_files = os.listdir(web_zip)
        log(web_files)
	web_files = [file for file in web_files if not file.startswith(".") and "tar" in file]
	if len(web_files) == 0:
		return
	path = "%s%s"%(web_zip,web_files[0])       
        zip_type = None
        unzip_params = None
	if os.path.exists(path):
		if path.endswith(".tar.gz"):
			zip_type = "tar"
                        unzip_params = " -zxvf "
		elif path.endswith(".tar.bz2"):
			zip_type = "tar"
                        unzip_params = " -jxvf "
        log("start unzipping ...")
       	os.system(" %s %s %s -C %s"%(zip_type,unzip_params,path,web_zip))
        log("unzipping done.")	



class Jobs(object):
        """ test """
	def hello(self,**args):
        	name = args.pop("name")
               	return "Hello!%s"%name

        """ check running state of clouinit hostname-injection """
        def whoiam(self,**args):
            	return "i'm %s"%get_local()
     
        """ fast deployment  """
        def fast_deploy(self,**args):

		print "Fast Deployment: %s "%args
        	mysql_need_deploy = False
        	web_need_deploy = False
        	ha_need_deploy = False
        	puppet_agents = []
        	"""  check servers: """
        	for name,value in args.iteritems():
            		if "mysql" in name:
                		mysql_need_deploy = True
            		elif "web" in name:
                		web_need_deploy = True
            		elif "haproxy" in name:
                		ha_need_deploy = True

            		""" check out non-puppetmaster servers"""
            		if value.count(".") == 3 and "puppetmaster" not in name:
                		puppet_agents.append(value)
        	""" just do deploy !! """
        	if mysql_need_deploy:
            		self.config_mysql(**args)
        	if web_need_deploy:
            		self.config_apache(**args)
        	if ha_need_deploy:
            		self.config_haproxy(**args)

        	""" trigger `puppet agent -t` for all puppet_agents """
        	self.send_puppet_command(**args)
        	""" restore puppet_site to initial status """ 
        	self.__annotate_import()
        	return "%s"%args
        
        """OK!!"""
        def __annotate_import(self):
        	fopener = open(puppet_site,"r")
        	site_pps = fopener.readlines()
        	fopener.close()
        	fwriter = open(puppet_site,"w")
        	for line in site_pps:
            		if line.startswith("import"):
                		fwriter.write("#%s"%line)
            		else:
                		fwriter.write("%s"%line)
        	fwriter.close()

        """ OK!!"""
        def __de_annotate_import(self,sign_str):
        	fopener = open(puppet_site,"r")
        	site_pps = fopener.readlines()
        	fopener.close()
        	fwriter = open(puppet_site,"w")       
        	for line in site_pps:
            		if line.startswith("#") and sign_str in line:
                		tmp_line = line[1:]
            		else:
                		tmp_line = line
            		fwriter.write("%s"%tmp_line)
        	fwriter.close()

        """ OK !!!"""
        def config_resolve(self,**args):
                resolves = "\n"
                """ read out old resolves"""
                resv_reader = open(resv_file,"r") 
                tmp = {}
                content = resv_reader.read()                
                resv_reader.close()
                for resv in content.split("\n"):
                        if len(resv.strip()) == 0:
                                continue
                        ip = resv.split()[0].strip()
                        host = resv.split()[1].strip()
                        tmp[ip]=host

                """ update old records with new resolves"""
                tmp.update(args)
                for ip,name in tmp.iteritems():
                        resolves = "%s\n%s %s"%(resolves,ip,name)
                #print resolves                
                f = open(resv_file,"w")
                f.write(resolves)
                f.close()
		print "hosts write finished"

                """ write fresh ip(s) to /root/IP to config sshkeys and config puppet-clients"""
                type ="w" if os.path.exists(ip_file) else "a+"
                #print type
                f = open(ip_file,type)
                ips = ""
                local = get_local()
                for k,v in args.iteritems():
                        if local in v:
                                continue
                        ips = "%s%s %s\n"%(ips,k,v)
                f.write(ips)
                f.close()
		print "IP write finished"
               
     
 
                """ do gen-sshkeys,ssh-copy-id,scp-hosts,and puppet agents auth.."""
                os.system("sh -x %s"%bash_file)
		print "Authorized distribution finished"
                return tmp


        """OK!!"""
	def config_haproxy(self,**args):
        	ha_server = None        
        	web_servers = []
        	""" check out haproxy server"""
        	""" check out all web-servers"""
        	for name,ip in args.iteritems():
            		if "haproxy" in name:
                		ha_server = ip
            		if name.startswith("web"):
                		web_servers.append(ip)
        	print "Config Haproxy: HA-Server %s and Web-Servers %s"%(ha_server,web_servers)
        	""" write the web-servers to  init_ha_IP file """
        	fopener = open(init_ha_IP,"w")
        	for ip in web_servers:
            		fopener.write("%s\n"%ip)
        	fopener.close()
        	""" de-annotate the import `node/lbs/*.pp` in `puppet_site` file """
        	self.__de_annotate_import("lbs/*")


  	"""OK!!"""
    	def __set_mysqlInfo_forBash(self,**args):
        	db_user = args["db_user"]
        	db_passwd = args["db_passwd"]
        	db_name = args["db_name"]

        	bash_lines = []
        	freader = open(mysql_bash,"r")
        	tmp_lines = freader.readlines()
        	freader.close()
        	for line in tmp_lines:
            		if "user=" in line:
                		bash_lines.append("user=%s"%db_user)
            		elif "database=" in line:
                		bash_lines.append("database=%s"%db_name)
            		elif "password=" in line:
                		bash_lines.append("password=%s"%db_passwd)
            		else:
                		bash_lines.append(line)
        	fwriter = open(mysql_bash,"w")
        	for line in bash_lines:
            		fwriter.write("%s\n"%line.strip())
        	fwriter.close()


        """ OK!! """
	def config_mysql(self,**args):
        	mysql_server = None
        	server_name = None
        	""" check out mysql server"""
        	for name,ip in args.iteritems():
            		if "mysql" in name:
                		mysql_server = ip
                		server_name = name
        	print "Config mysql: Mysql-Server %s %s"%(mysql_server,server_name)
        	""" rm *.pp"""
        	self.__clear_pps_fordir(mysql_pp_dir)

        	""" read mysql template into mysql.db.cn.pp"""
        	self.__copy_template_to_pp(server_name,mysql_pp_dir)
        	""" de-annotate the import `node/db/*.pp` in `puppet_site` file """
        	self.__de_annotate_import("db/*")
        	""" modify user/passwd/dbname in file `mysql_bash` """
        	self.__set_mysqlInfo_forBash(**args)
        	""" by default,we believe that db file already ftp-uploaded.Then Done.Waiting for 'puppet agent -t' commands .."""        
         
        
        """ OK!! """
    	def __clear_pps_fordir(self,pp_dir):
        	pp_files = os.listdir(pp_dir)
        	for pp_file in pp_files:
            		abs_pp_file = "%s%s%s"%(pp_dir,os.sep,pp_file)
            		if pp_file.endswith(".pp") and os.path.isfile(abs_pp_file):
                		os.remove(abs_pp_file)

        
        """ OK!! """
    	def __copy_template_to_pp(self,node_name,pp_dir):
        	freader = open("%s%s%s"%(pp_dir,os.sep,"template"),"r")
        	pp = freader.read()
        	freader.close()
        	pp = node_name.join(pp.split("template"))
        	fwriter = open("%s%s%s%s"%(pp_dir,os.sep,node_name,".pp"),"a+")
        	fwriter.write(pp)
        	fwriter.close()        


        """ OK!!! """
        def config_apache(self,**args):

                """ set default values for `web_pp_path` and `web_node_site_flag` """
                web_pp_path = web_pp_dir
                web_node_site_flag = "apache/*"
                http_mode = args["http_mode"]
                if "nginx" in http_mode:
               		web_pp_path = nginx_dir
                	web_node_site_flag = "nginx/*"
                """ tomcat deployment not implemented yet """
                if "tomcat" in http_mode:
			return
                
        	""" clear *.pp in `web_pp_path` """
        	self.__clear_pps_fordir(web_pp_path)
        	""" read template into web{N}.web.cn.pp  file(s)"""
        	freader = open("%s%s%s"%(web_pp_path,os.sep,"template"),"r")
        	tmp_webpp = freader.read()
        	freader.close()        
        	for node,ip in args.iteritems():
            		if node.startswith("web"):
                		self.__copy_template_to_pp(node,web_pp_path)
        	""" de-annotate the import `node/apache/*.pp` in `puppet_site` file"""
        	self.__de_annotate_import(web_node_site_flag)
        	""" by default,we believe that webapp file already ftp-uploaded.Then Done. Waiting for 'puppet agent -t' commands .."""
                unzip()
                """ un-Archive apache files in /webroot/ """
	
	def __notify_agent_to_sync(self,ip):
        	cmd_template = "ssh root@%s 'puppet agent -t -d -v ' "
	        try:
                	print "Pre-executing: ssh root@%s 'puppet agent -t'"%ip
                	os.system(cmd_template%ip)
                	print "Post-executing: ssh root@%s 'puppet agent -t'"%ip
                except Exception as e:
                	print "Error-executing: ssh root@%s 'puppet agent -t'"%ip
                	pass			

        """OK!!"""
        def send_puppet_command(self,**args):
        	puppet_agents = []
        	for node,ip in args.iteritems():
            		if ip.count(".") == 3 and "puppetmaster" not in node:
                		puppet_agents.append(ip)
		tasks = []
        	for ip in puppet_agents:
			task = threading.Thread(target=self.__notify_agent_to_sync,args=(ip,))
			task.start()
			tasks.append(task)
		for task in tasks:
			task.join()			
        	print "Puppet Agents %s Starts Synchronizing Data from PuppetMaster."%puppet_agents
	
                
        """ to test """
	def add_extra_nodes(self,**args):
        	""" clear /root/IP to Ensure only newly-added web nodes configed """
        	if os.path.exists(ip_file):
                	os.remove(ip_file)
            	""" config resolve"""
            	self.config_extra_resolve(**args)      
            	""" config puppet : web nodes resources """
            	self.config_apache(**args)
            	""" config extra WEB nodes in haproxy"""
            	self.config_haproxy_inc(**args)
            	""" notify puppet agents: starting synchronizing data."""
            	self.send_puppet_command(**args)
            	""" annotate all `import *` """
            	self.__annotate_import()
            	return args
         
        """ to test """
        def config_extra_resolve(self,**args):
            resolves = "\n"
            """ read out old resolves"""
            resv_reader = open(resv_file,"r") 
            tmp = {}
            content = resv_reader.read()                
            resv_reader.close()
            for resv in content.split("\n"):
                    if len(resv.strip()) == 0:
                            continue
                    ip = resv.split()[0].strip()
                    host = resv.split()[1].strip()
                    tmp[host]=ip

            """ update old records with new resolves"""
            tmp.update(args)
            for name,ip in tmp.iteritems():
                    if "http_mode" in name:
       	    		continue
                    resolves = "%s\n%s %s"%(resolves,ip,name)
            #print resolves                
            f = open(resv_file,"w")
            f.write(resolves)
            f.close()

            """ write fresh ip(s) to /root/IP to config sshkeys and config puppet-clients"""
            type ="w" if os.path.exists(ip_file) else "a+"
            #print type
            f = open(ip_file,type)
            ips = ""
            local = get_local()
            for k,v in args.iteritems():
                    if local in k or "http_mode" in k or "haproxy.cn" in k:
                            continue
                    ips = "%s%s %s\n"%(ips,v,k)
            f.write(ips)
            f.close()
            
            """ do gen-sshkeys,ssh-copy-id,scp-hosts,and puppet agents auth.."""
            os.system("sh %s"%bash_file)
            return tmp
	
	""" OK!!  """
        def config_haproxy_inc(self,**args):      
        	web_servers = []
            	""" check out all web-servers"""
            	for name,ip in args.iteritems():
                	if name.startswith("web"):
                        	web_servers.append(ip)
                print "Config new Web-Servers %s"%web_servers
            	""" write the web-servers to  HA_INC_IPs file """
            	fopener = open(HA_INC_IPs,"w")
            	for ip in web_servers:
                	fopener.write("%s\n"%ip)
            	fopener.close()
            	""" de-annotate the import `node/lbs/*.pp` in `puppet_site` file """
            	self.__de_annotate_import("lbs-inc/*")
        
        """ OK!!  """
        def dealloc(self,**args):
                web_servers = []
                """ check out all web-servers"""
                for name,ip in args.iteritems():
                        if name.startswith("web"):
                                web_servers.append(name)
		""" dealloc puppet cert(s) from the nodes to be removed """
		template = "puppet cert -c %s"
		for puppet_agent in web_servers:
			dealloc_retv = Popen(template%puppet_agent,shell=True,stdout=PIPE).stdout.read()
			log("Deallloc web node %s and get response: %s"%(puppet_agent,dealloc_retv))
		return web_servers
                                
       		                       
 	def check_extra_nodes_status(self,**args):
		""" check out status of newly-added nodes .As they are not sshkey-authorized yet, 
		    the check style changes to `ping` ,not `ssh` ."""
		extra_web_nodes = {k:args[k] for k in args.keys() if "web" in k}
		template = "ping -c 1 %s"
		result = ""
		for node,ip in extra_web_nodes.iteritems():
			pingres = Popen(template%ip,shell=True,stdout=PIPE).stdout.read()
			status = "down" if "100% packet loss" in pingres else "up"
			result = "%s-%s:%s"%(result,node,status)
		return result
	 
        def check_slave_service(self,**args):
		""" check out hosts that need checks """
		result = ""
		for node,ip in args.iteritems():
			if node.startswith("web") and ip.count(".") == 3:
				http_mode = "httpd" if args["http_mode"] == "apache" else args["http_mode"]
				result = "%s-%s:%s"%(result,node,self.__check_remote_service(ip,http_mode))
			elif node.startswith("haproxy") and ip.count(".") == 3:
				result = "%s-%s:%s"%(result,node,self.__check_remote_service(ip,"haproxy"))
			elif node.startswith("mysql") and ip.count(".") == 3:
				result = "%s-%s:%s"%(result,node,self.__check_remote_service(ip,"mysql"))
		        else:
				pass
		return result
		          	
        def __check_remote_service(self,remote_host,service_keyword):
	       	""" check out services running on `remote_host` """
        	list_services = "ssh root@%s 'ps -A' "%remote_host
        	services = Popen(list_services,stdout=PIPE,shell=True).stdout.read()
		result = ""
        	if len(services) > 0 and services.count(service_keyword) > 0:
                	result = "%s|active_server|up"%service_keyword
        	elif len(services) > 0 and services.count(service_keyword) == 0:
                	result = "%s|inactive_server|up"%service_keyword
        	else:
                	result = "%s|inactive_server|down"%service_keyword	        	
		return result
	
		         	

	
	

def app(environ, start_response):
	source_ip = environ['REMOTE_ADDR']
    	request_method = environ['REQUEST_METHOD']
	
        if request_method != reserved_http_method:
        	status = '405 Method Not Allowed'
        	headers = [('Content-type', 'application/json')]
        	start_response(status, headers)
        	return ['{"msg":"Method Not Allowed"}']
        
        print "App: try parse params from environ ...."
                
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	request_body = environ['wsgi.input'].read(request_body_size)
	request_body = json.loads(request_body)
        
        print "App: environ params got - %s"%request_body
        func = request_body.pop("action")
        jobs = Jobs()
        retv = getattr(jobs,func)(**request_body)
        status = '200 OK' # Not Allowed 
        headers = [('Content-type', 'application/json')]
        start_response(status, headers)
        return ['{"msg":"%s"}'%str(retv)]


httpd = make_server('', 9999, app)
print "start listening 0.0.0.0:9999"
httpd.serve_forever()

"""

if __name__ == "__main__":
	unzip("/webroot/123.tar.gz")

"""
