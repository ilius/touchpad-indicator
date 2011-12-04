#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# device_list.py
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
import os
import machine_information
import com
try:
	import pyudev
except:
	print('Error: no pyudev installed.')

FILEOUTPUT = os.path.join(os.environ['HOME'],'device_list.txt')

	def print_device_attrib(Device, fileoutput=None):
	print('------------------------------------------------------')
	print(u'sys_name: ' + unicode(Device.sys_name))
	for attrName, attrValue in Device.iteritems():
		print(attrName + ': ' + str(attrValue))
	if fileoutput != None:
		fileoutput.write('------------------------------------------------------\n')
		fileoutput.write('sys_name: ' + Device.sys_name+'\n')
		for attrName, attrValue in Device.iteritems():
			fileoutput.write(attrName + ': ' + str(attrValue)+'\n')

def print_devices(kind, context, fileoutput=None):
	if kind == 'MOUSE':
		search = '---------------MICE----------------'
		devices_list = context.list_devices(subsystem='input', ID_INPUT_MOUSE=True)
	elif kind == 'TOUCHPAD':
		search = '-------------TOUCHPADS-------------'
		devices_list = context.list_devices(subsystem='input', ID_INPUT_TOUCHPAD=True)
	else:
		search = '-----------OTHER DEVICES-----------'
		devices_list = context.list_devices(subsystem='input')
	print('\n\n')
	print search
	for device in devices_list:
		print('device: ' + device.sys_name)
		try:
			print('parent name: ' + device.parent['NAME'])
			print('parent attributes:')
			print_device_attrib(device.parent)
		except:
			print(device.sys_name + ' has no parent')
		print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		print('device atributes:')
		print_device_attrib(device)
	if fileoutput != None:
		fileoutput.write('\n\n')
		fileoutput.write(search+'\n')
		for device in devices_list:
			fileoutput.write('device: ' + device.sys_name+'\n')
			try:
				fileoutput.write('parent name: ' + device.parent['NAME']+'\n')
				fileoutput.write('parent attributes:\n')
				print_device_attrib(device.parent,fileoutput)
			except:
				fileoutput.write(device.sys_name + ' has no parent\n')
			fileoutput.write('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
			fileoutput.write('device atributes:\n')
			print_device_attrib(device,fileoutput)

def header(fileoutput):
	fileoutput.write('#####################################################\n')
	fileoutput.write(machine_information.get_information())
	fileoutput.write('Touchpad-Indicator version: %s\n'%com.VERSION)
	fileoutput.write('#####################################################\n')

def list():
	context = pyudev.Context()
	fileoutput = open(FILEOUTPUT,'w')
	header(fileoutput)
	print_devices('MOUSE',context,fileoutput)
	print_devices('TOUCHPAD',context,fileoutput)
	print_devices('OTHER',context,fileoutput)
	fileoutput.close()

if __name__ == "__main__":	
	list()
	print(unicode(chr(255)))
	exit(0)
