

import sys

if __name__ == "__main__":
        rdp_port=sys.argv[1] if len(sys.argv)>1 else 3389
        rdp_port=int(rdp_port) if rdp_port.isdigit() else 3389
        #print port
	#rdp_port=3340
        adminPass="123456"
        chg_Rdp="""net user administrator %(adminPass)s\nREG ADD HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal\" \"Server\\Wds\\rdpwd\\Tds\\tcp /v PortNumber /t REG_DWORD /d  %(PortNumber)d /f \nREG ADD HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal\" \"Server\\WinStations\\RDP-Tcp /v PortNumber /t REG_DWORD /d  %(PortNumber)d /f \nnetsh firewall add portopening tcp %(PortNumber)d remote\n""" % {"adminPass": adminPass,"PortNumber":rdp_port}
	print chg_Rdp
 
