#! /usr/bin/python
# -*- coding: utf-8 -*-
#
#
# Configurator for access to gconf
#
# Copyright (C) 2010,2011
# Miguel Angel Santamaría Rogado <leibag@gmail.com>
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio
from gi.repository import GLib
import types

class Configurator():
	def __init__(self,base_key):
		print base_key
		self.settings = Gio.Settings.new(base_key)

	def get(self,key):
		casts = { 'b': GLib.Variant.get_boolean,
				  'i': GLib.Variant.get_int16,
				  'd': GLib.Variant.get_double,
				  's': GLib.Variant.get_string}
		try:
			res = self.settings.get_value(key)
			tip = res.get_type_string()
			return casts[tip](res)
		except AttributeError:
			return None

	def set(self,key,value):
		casts = {types.BooleanType: Gio.Settings.set_boolean,
				types.IntType:      Gio.Settings.set_int,
				types.FloatType:    Gio.Settings.set_double,
				types.StringType:   Gio.Settings.set_string,
				types.UnicodeType:  Gio.Settings.set_string}
		try:
			if casts[type(value)](self.settings,key,value) == True:
				self.settings.sync()
				return True
		except AttributeError:
			pass
		return False
		
if __name__ == '__main__':
	configurator = Configurator('org.gwibber.preferences')
	print configurator.get('autostart')
	configurator.set('autostart',True)
	print configurator.get('autostart')
	exit(0)
