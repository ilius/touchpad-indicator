#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
#
__author__="atareao"
__date__ ="$19-feb-2011$"
#
# Configurator for access to gconf
#
# Copyright (C) 2011 Lorenzo Carbonell
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
import gconf
import types

class GConf():
	def __init__(self):
		self.client = gconf.client_get_default()

	def set_key(self,key,value):
		casts = {types.BooleanType: gconf.Client.set_bool,
                 types.IntType:     gconf.Client.set_int,
                 types.FloatType:   gconf.Client.set_float,
                 types.StringType:  gconf.Client.set_string}
		casts[type(value)](self.client,key, value)		

	def get_key(self,key):
		casts = {gconf.VALUE_BOOL:   gconf.Value.get_bool,
                 gconf.VALUE_INT:    gconf.Value.get_int,
                 gconf.VALUE_FLOAT:  gconf.Value.get_float,
                 gconf.VALUE_STRING: gconf.Value.get_string}		
		value = self.client.get(key)
		return casts[value.type](value)

	def set_string_list(self,key,values):
		self.client.set_list(key,gconf.VALUE_STRING,values)
	
	def get_string_list(self,key):
		return self.client.get_list(key,gconf.VALUE_STRING)

	def get_all_keys(self,folder):
		return self.client.all_entries(folder)

	def get_all_dirs(self,folder):
		return self.client.all_dirs(folder)
