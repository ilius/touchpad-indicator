#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Name: config
Description: Modulo que permite copiar la configuracion a las cuentas de los usuarios en el equipo
Version:0.1
License: GPLv3
Copyright: Copyright (C) 2009  Ernesto Nadir Crespo Avila <ecrespo@debianvenezuela.org>
Author: Ernesto Nadir Crespo Avila
Email: ecrespo@debianvenezuela.org
"""
import com
from commands import getstatusoutput

class GConfKeybinding():
	def __init__(self):
		pass
		
	def create_schema(self):
		ans = getstatusoutput('gconftool-2 --load=%s'%com.GCONFXML)
		return ans[0]==0
	
	def exits_keybinding(self):
		ans = getstatusoutput('gconftool-2 -R /desktop/gnome/keybindings')
		return ans[1].find('touchpad-indicator')>-1
	
	def set_shortcut(self,shortcut):
		ans = getstatusoutput('gconftool-2 --type string --set /desktop/gnome/keybindings/touchpad-indicator/binding --set %s'%shortcut)
		return ans[0]==0
	
	def get_shortcut(self):
		ans = getstatusoutput('gconftool-2 --get /desktop/gnome/keybindings/touchpad-indicator/binding')
		print ans
		return ans[1]
		
if __name__ == '__main__':
	gck = GConfKeybinding()
	print gck.exits_keybinding()
	print gck.create_schema()
	print gck.get_shortcut()
