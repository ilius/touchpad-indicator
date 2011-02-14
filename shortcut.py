#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       shortcut.py
#       
#       Copyright 2010 Lorenzo Carbonell <atareao@zorita>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os
import gtk
import gobject
import gconf
import locale
from gconf import ValueType
import gettext


APP = 'touchpad-indicator'
DIR = '/usr/share/locale-langpack'
KEY = '/desktop/gnome/keybindings/touchpad_indicator/'

locale.setlocale(locale.LC_ALL, '')
#locale.setlocale(locale.LC_ALL, 'de_DE')
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext

def search_for_keys(gconfi,chain):
	keys=[]
	for key in gconfi.get_all_keys(chain):
		if key.get_value().type == gconf.VALUE_STRING:
			if (key.get_value().get_string().find('<Control>')!=-1) and (key.get_value().get_string().find('<Alt>')!=-1):
				k=key.get_value().get_string()
				k=k[k.rfind('>')+1:]
				if len(k)==1:
					keys.append(k)
	return keys

def get_combination_keys():
	gconfi = GConf()
	keys=search_for_keys(gconfi,'/apps/compiz/general/allscreens/options')
	keys+=search_for_keys(gconfi,'/apps/metacity/global_keybindings')
	keys+=search_for_keys(gconfi,'/apps/metacity/window_keybindings')
	for dire in gconfi.get_all_dirs('/desktop/gnome/keybindings'):
		keys+=search_for_keys(gconfi,dire)
	return keys


gconf_touchpad_enabled = '/desktop/gnome/peripherals/touchpad/touchpad_enabled'

class Keybindings():
	def __init__(self,combination_key,action):
		self.combination_key = combination_key
		self.action = action

	def get_combination_key(self):
		return self.combination_key
	
	def get_action(self):
		return self.action
		
class GConf():
	def __init__(self):
		self.client = gconf.client_get_default()

	def get_key(self, key):
		return self.client.get_string(key)

	def set_key(self, key, val):
		self.client.set_string(key, str(val))
	
	def get_all_keys(self,folder):
		return self.client.all_entries(folder)

	def get_all_dirs(self,folder):
		return self.client.all_dirs(folder)
	

class Shortcut():
	def __init__(self):
		#
		self.builder = gtk.Builder()
		self.builder.add_from_file('/usr/share/touchpad-indicator/shortcut.glade')
		#
		self.window = self.builder.get_object('dialog1')
		self.label1 = self.builder.get_object('label1')
		self.entry1 = self.builder.get_object('entry1')
		self.button1 = self.builder.get_object('button1')
		self.button2 = self.builder.get_object('button2')
		#
		# Language
		#
		self.window.set_title(_('Touchpad-Indicator'))
		self.label1.set_label(_('Set shortcut for Touchpad-Indicator:'))
		self.button1.set_label(_('Ok'))
		self.button2.set_label(_('Cancel'))
		#
		self.window.show_all()
		#
		gconfi = GConf()
		k=gconfi.get_key(KEY+'binding')
		if k!=None and len(k)>0:
			k=k[k.rfind('>')+1:]
			self.entry1.set_text(k)
			self.key=k
		# Magia :P
		self.builder.connect_signals(self)
		#
		self.window.run()

	def on_button1_clicked(self,widget):
		gconfi = GConf()
		gconfi.set_key(KEY+'action','/usr/share/touchpad-indicator/change_touchpad_state.py')
		gconfi.set_key(KEY+'name','modify_touchpad_status')
		if len(self.entry1.get_text())>0:
			gconfi.set_key(KEY+'binding','<Control><Alt>'+self.entry1.get_text())			
		else:
			gconfi.set_key(KEY+'binding','')
		self.window.hide()
		
	def on_button2_clicked(self,widget):
		self.window.hide()
	
	def on_entry1_key_release_event(self,widget,event):
		key=event.keyval
		# numeros / letras mayusculas / letras minusculas
		if ((key>47) and (key<58)) or ((key > 64) and (key < 91)) or ((key > 96) and (key < 123)):
			if gtk.gdk.keyval_is_upper(event.keyval):
				keyval=gtk.gdk.keyval_name(gtk.gdk.keyval_to_lower(event.keyval))
			else:
				keyval=gtk.gdk.keyval_name(event.keyval)
			if keyval in get_combination_keys() and keyval!=self.key:
				dialog = gtk.MessageDialog(None,gtk.DIALOG_MODAL,type=gtk.MESSAGE_WARNING,buttons=gtk.BUTTONS_OK)
				msg = _('La combinacion <Control> + <Alt> + ')+keyval+_(' ya esta asignada')
				dialog.set_property('title', 'Error')
				dialog.set_property('text', msg)				
				dialog.run()
				dialog.destroy()
				self.entry1.set_text(self.key)
			else:
				self.entry1.set_text(keyval)
				self.key = keyval
	
	def get_key(self):
		return self.key
if __name__ == '__main__':
	shortcut=Shortcut()
	#get_combination_keys()
