#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
__author__="Lorenzo Carbonell"
__date__ ="$28-jul-2012$"
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
import types
from gi.repository import GConf

CASTSFROM = {
GConf.ValueType.BOOL:   GConf.Value.get_bool,
GConf.ValueType.INT:    GConf.Value.get_int,
GConf.ValueType.FLOAT:  GConf.Value.get_float,
GConf.ValueType.STRING: GConf.Value.get_string,
GConf.ValueType.LIST:   GConf.Value.get_list
}	

CASTSTO = {
bool: GConf.Client.set_bool,
int:     GConf.Client.set_int,
float:   GConf.Client.set_float,
str:  GConf.Client.set_string
}
'''
types.ListType:    GConf.Client.set_list,
types.TupleType:   GConf.Client.set_list,
set:               GConf.Client.set_list}
'''

class GConfManager(object):
	def __init__(self):
		self.client = GConf.Client.get_default()

	def get_keys(self,key):
		keys = []
		for entry in self.client.all_entries(key):
			keys.append(entry.key)
		return keys

	def get_dirs(self,key):
		directories = []
		for directory in self.client.all_dirs(key):
			 directories.append(directory)
		return directories
	def add_directory(self,key,directory):
		if not key.endswith('/'):
			key += '/'+directory
		else:
			key += directory
		self.set_value(key,'')
		
	def has_dirs(self,key):
		return len(self.client.all_dirs(key))>0
		
	def get_dirs_recursive(self,key):
		directories = []
		for directory in self.client.all_dirs(key):
			 directories.append(directory)			 
			 if self.has_dirs(directory):
				 directories+=self.get_dirs_recursive(directory)
		return directories
		
	def get_keys_recursive(self,key):		
		keys = []
		for directory in self.get_dirs_recursive(key):
			keys+=self.get_keys_recursive(directory)
		return keys
		
	def get_value(self,key):
		gval = self.client.get(key)
		if gval == None:
			return None
		if gval.type == GConf.ValueType.LIST:
			string_list = [item.get_string() for item in gval.get_list()]
			return string_list
		else:
			return CASTSFROM[gval.type](gval)
			
	def set_value(self,key,value):
		if type(value) in (list, tuple, set):
			string_value = [str(item) for item in value]
			CASTSTO[type(value)](self.client, key,
				GConf.ValueType.STRING, string_value)
		else:
			CASTSTO[type(value)](self.client, key, 
				value)

if __name__ == '__main__':
	def get_shortcuts():		
		gcm = GConfManager()
		keys = []
		keys+=gcm.get_keys('/apps/compiz/general/allscreens/options')
		keys+=gcm.get_keys('/apps/metacity/global_keybindings')
		keys+=gcm.get_keys('/apps/metacity/window_keybindings')
		for directory in gcm.get_dirs('/desktop/gnome/keybindings'):
			for key in gcm.get_keys(directory):
				if key.endswith('/binding'):
					keys.append(key)
		values = []
		for key in keys:
			value = gcm.get_value(key)
			if value != 'disabled':
				values.append(value)
		return values
	print(get_shortcuts())
	gcm = GConfManager()
	gcm.set_value('/desktop/gnome/keybindings/touchpad-indicator/action','')
	gcm.set_value('/desktop/gnome/keybindings/touchpad-indicator/binding','')
	gcm.set_value('/desktop/gnome/keybindings/touchpad-indicator/name','')

