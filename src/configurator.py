#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
#
__author__='Lorenzo Carbonell'
__date__ ='$22/05/2012'
#
#
# Copyright (C) 2012 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
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

import ConfigParser
import com
import os
import shutil

DEFAULTS = {
			'autostart':'no',
			'on_mouse_plugged':'no',
			'enable_on_exit':'no',
			'enable_on_start':'yes',
			'start_hidden':'no',
			'show_notifications':'yes',
			'theme':'light',
			'shortcut':'ctrl+alt+f'
			}

def check_autostart_dir():
	if not os.path.exists(com.AUTOSTART_DIR):
		os.makedirs(com.AUTOSTART_DIR)

def create_or_remove_autostart(create):
	check_autostart_dir()
	if create == True:
		if not os.path.exists(com.FILE_AUTO_START):
			shutil.copyfile('/usr/share/touchpad-indicator/touchpad-indicator-autostart.desktop',com.FILE_AUTO_START)
	else:
		if os.path.exists(com.FILE_AUTO_START):
			os.remove(com.FILE_AUTO_START)

class Configuration(object):
	
	def __init__(self):
		self.config = ConfigParser.RawConfigParser()
		self.conf = DEFAULTS
		if not os.path.exists(com.CONFIG_FILE):
			self.create()
			self.save()
		self.read()
	'''
	####################################################################
	Config Functions
	####################################################################
	'''
		 
	def _get(self,key):
		try:
			value = self.config.get('Configuration',key)
		except ConfigParser.NoOptionError:
			value = DEFAULTS[key]
		if value == 'None':
			value = None
		return value
		
	def set(self, key, value):
		if key in self.conf.keys():
			self.conf[key] = value
			return value
		return None
			
	def get(self,key):
		if key in self.conf.keys():
			return self.conf[key]
		return None

	'''
	####################################################################
	Operations
	####################################################################
	'''
	def read(self):
		self.config.read(com.CONFIG_FILE)
		for key in self.conf.keys():
			self.conf[key] =  self._get(key)
		

	def create(self):
		if not self.config.has_section('Configuration'):
			self.config.add_section('Configuration')
		self.set_defaults()
	
	def set_defaults(self):
		self.conf = {}
		for key in DEFAULTS.keys():
			self.conf[key] = DEFAULTS[key]
		self.password = ''

	def save(self):
		for key in self.conf.keys():
			self.config.set('Configuration', key, self.conf[key])
		if not os.path.exists(com.CONFIG_APP_DIR):
			os.makedirs(com.CONFIG_APP_DIR)
		self.config.write(open(com.CONFIG_FILE, 'w'))
		

if __name__=='__main__':
	configuration = Configuration()
	#configuration.set('password','armadillo')
	#configuration.save()
	print '############################################################'
	print configuration.get('autostart')
	print configuration.get('theme')
	print configuration.set('theme','dark')
	print configuration.get('theme')
