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

import codecs
import os
import json

import comun

class Configuration(object):
	def __init__(self):
		self.params = comun.PARAMS
		self.read()
	
	def get(self,key):
		try:
			return self.params[key]
		except KeyError:
			self.params[key] = comun.PARAMS[key]
			return self.params[key]
		
	def set(self,key,value):
		self.params[key] = value
	
	def set_defaults(self):
		self.params = comun.PARAMS
		self.save()
	
	def read(self):		
		try:
			f=codecs.open(comun.CONFIG_FILE,'r','utf-8')
		except IOError:
			self.save()
			f=codecs.open(comun.CONFIG_FILE,'r','utf-8')
		try:
			self.params = json.loads(f.read())
		except ValueError:
			self.save()
		f.close()

	def save(self):
		if not os.path.exists(comun.CONFIG_APP_DIR):
			os.makedirs(comun.CONFIG_APP_DIR)
		f=codecs.open(comun.CONFIG_FILE,'w','utf-8')
		f.write(json.dumps(self.params,encoding ='utf-8'))
		f.close()
