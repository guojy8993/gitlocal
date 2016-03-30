#! /usr/bin/python

import base64

#metadata = {"rdp":64500}
#adminPass = "admin"

#port = metadata.pop("rdp") if "rdp" in metadata else 3389 
#port = port if port is not None and port.isdigit() else "3389"
#port = '4007'
#adminPass = '12345'
#passwd = \
#'rem cmd\r\nnet user administrator %(adminPass)s\r\nREG ADD HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\Wds\\rdpwd\\Tds\\tcp /v PortNumber /t REG_DWORD /d %(PortNumber)s /f \r\nREG ADD HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp /v PortNumber /t REG_DWORD /d  %(PortNumber)s /f \n' % {'adminPass': adminPass,'PortNumber':port}
#user_data = base64.b64encode(passwd.encode('utf-8'))
#print passwd



#print user_data
#print "***********"

#pass2 = base64.encodestring(user_data)
#print pass2
#pass3 = base64.b64encode(user_data)
#print pass3

#print "+++++++++++++"

#a = '1'*1024
#print a
#print base64.encodestring(a)


#encoded="cmVtIGNtZA0KbmV0IHVzZXIgYWRtaW5pc3RyYXRvciAxcWF6eHN3MiMNCm5ldHNoIGludGVyZmFjZSBpcCBzZXQgYWRkcmVzcyAiV0FOIiBzdGF0aWMgMTIyLjExNC4yNTUuNSAyNTUuMjU1LjI1NS4wIDEyMi4xMTQuMjU1LjEgMQ0KbmV0c2ggaW50ZXJmYWNlIGlwIHNldCBkbnMgIldBTiIgc3RhdGljIDguOC44LjgNCm5ldHNoIGludGVyZmFjZSBpcCBzZXQgYWRkcmVzcyAiTEFOIiBzdGF0aWMgMTAuMTIyLjI1NS4yMCAyNTUuMjU1LjAuMA0KbmV0c2ggaW50ZXJmYWNlIGlwdjYgc2V0IHByaXZhY3kgZGlzYWJsZWQNCm5ldHNoIGludGVyZmFjZSBpcHY2IGFkZCBhZGRyZXNzIFdBTiBubw0KbmV0c2ggaW50ZXJmYWNlIGlwdjYgYWRkIHJvdXRlIHByZWZpeD1uby9ubyBpbnRlcmZhY2U9V0FOIG5leHRob3A9bm8NCnJvdXRlIGFkZCAtcCAxMC4wLjAuMCBtYXNrIDI1NS4wLjAuMCAxMC4xMjIuMTI0LjENCnNodXRkb3duIC9zIC90IDMwMA=="
#decode = base64.b64decode(encoded)
#print decode

asd="REG ADD HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal\" \"Server\\WinStations\\RDP-Tcp /v PortNumber /t REG_DWORD /d  3456 /f"
print asd






