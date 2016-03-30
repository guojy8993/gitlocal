#! /usr/bin/python

def get_host():
    """ read content from /etc/hostname file"""
    df = open("/etc/hostname")
    content = df.read()
    return content.strip()

def get_ip():
    """ parse /etc/hosts to get local ip"""
    df = open("/etc/hosts")
    hosts = df.readlines()
    hostname = get_host()
    host_rec = [line for line in hosts if hostname in line][0]
    return host_rec.split()[0].strip()

if __name__ == "__main__":
	print get_ip()
