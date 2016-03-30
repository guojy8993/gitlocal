#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
        adminPass="123456"
        port=9876
	passwd="""net user administrator %(adminPass)s\nREG ADD HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal\" \"Server\\Wds\\rdpwd\\Tds\\tcp /v PortNumber /t REG_DWORD /d %(port)d /f \n""" %{"adminPass":adminPass,"port":port}
        #
	print passwd
