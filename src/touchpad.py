#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# touchpad.py
#
# Copyright (C) 2010,2011
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
# Miguel Angel Santamaría Rogado <leibag@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
import shlex, subprocess
import time
import com

TOUCHPADS = ['touchpad','glidepoint','fingersensingpad','bcm5974']

def ejecuta(comando):
	args = shlex.split(comando)
	p = subprocess.Popen(args, bufsize=10000, stdout=subprocess.PIPE)
	valor = p.communicate()[0]
	return valor

def search_touchpad(where):
	where = where.lower()
	for touchpad in TOUCHPADS:
		if where.find(touchpad) != -1:
			return True
	return False

class Touchpad(object):
	def __init__(self):
		self.ids = self._get_ids()
	
	def _get_all_ids(self):
		ids = []
		lines = ejecuta('xinput --list')
		for line in lines.split('\n'):
			if line.find('id=')!=-1:
				ids.append(int(line.split('=')[1].split('[')[0].strip()))
		return ids
		
	def _is_touchpad(self,id):
		comp = ejecuta(('xinput --list-props %s') % (id))
		return search_touchpad(comp)
		
	def is_there_touchpad(self):
		comp = ejecuta('xinput --list-props %s')
		return search_touchpad(comp)
		
	'''		
	def _get_ids(self):
		ids = []
		lines = ejecuta('xinput list')
		for line in lines.split('\n'):
			if line.lower().find('touchpad')!=-1:
				ids.append(int(line.split('=')[1].split('[')[0].strip()))
			if line.lower().find('glidepoint')!=-1:
				ids.append(int(line.split('=')[1].split('[')[0].strip()))
		return ids
	'''
	def _get_ids(self):
		ids = []
		for id in self._get_all_ids():
			if self._is_touchpad(id):
				ids.append(id)
		return ids
	
	
	def set_touchpad_enabled(self,id):
		ejecuta(('xinput set-prop %s "Device Enabled" 1')%id)		
	
	def set_touchpad_disabled(self,id):
		ejecuta(('xinput set-prop %s "Device Enabled" 0')%id)
		#gconfi = GConf()
		#gconfi.set_key('/desktop/gnome/peripherals/touchpad/touchpad_enabled',False)		

	def is_touchpad_enabled(self,id):
		lines = ejecuta('xinput --list-props %s'%id)
		for line in lines.split('\n'):
			if line.lower().find('device enabled')!=-1:
				if line.split(':')[1].strip() == '1':
					return True
		return False

	def disable_all_touchpads(self):
		for id in self.ids:
			self.set_touchpad_disabled(id)
			time.sleep(1)
		return not self.all_touchpad_enabled()

	def enable_all_touchpads(self):
		for id in self.ids:
			self.set_touchpad_enabled(id)
			time.sleep(1)
		return self.all_touchpad_enabled()

	def all_touchpad_enabled(self):
		for id in self.ids:
			if self.is_touchpad_enabled(id) == False:
				return False
		return True
		

if __name__ == '__main__':
	tp = Touchpad()
	for id in tp._get_all_ids():
		print id
		print ('El device %s es Touchpad %s')%(id,tp._is_touchpad(id))
	tp.enable_all_touchpads()
	print tp.all_touchpad_enabled()
	#tp.disable_all_touchpads()
	print tp.all_touchpad_enabled()
	tp.enable_all_touchpads()
	print tp.is_there_touchpad()
