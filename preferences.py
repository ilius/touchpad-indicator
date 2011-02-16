#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
#
__author__="atareao"
__date__ ="$29-ene-2011$"
#
# <from numbers to letters.>
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
import os
import gtk
import locale
import gettext
import gconf
import com

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext

APPDIR = com.APPDIR

#KEY = '/desktop/gnome/keybindings/touchpad_indicator/'

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
	
class Preferences(gtk.Dialog):
	def __init__(self):
		#
		gtk.Dialog.__init__(self)
		self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.set_title('Touchpad Indicator | '+_('Preferences'))
		self.set_default_size(400, 150)
		self.connect('destroy', self.close_application)
		#
		self.vbox1 = gtk.VBox(spacing = 5)
		self.vbox1.set_border_width(5)
		self.get_content_area().add(self.vbox1)
		#
		self.frame1 = gtk.Frame()
		self.vbox1.add(self.frame1)
		#***************************************************************
		table1 = gtk.Table(3,2,True)
		self.frame1.add(table1)
		#
		self.label11 = gtk.Label(_('Set shortcut for Touchpad-Indicator:'))
		table1.attach(self.label11,0,1,0,1)
		#
		self.entry11 = gtk.Entry()
		self.entry11.set_editable(False)
		self.entry11.connect('key-release-event',self.on_entry11_key_release_event)
		table1.attach(self.entry11,1,2,0,1)
		#
		self.checkbutton1 = gtk.CheckButton(_('Autostart'))
		table1.attach(self.checkbutton1,0,2,1,2)
		#
		self.checkbutton2 = gtk.CheckButton(_('Disable touchpad when mouse plugged'))
		table1.attach(self.checkbutton2,0,2,2,3)

		
		#***************************************************************
		table2 = gtk.Table(1,2,True)
		self.vbox1.add(table2)
		#
		self.button1 = gtk.Button(_('Ok'))
		self.button1.connect('clicked',self.close_ok)
		table2.attach(self.button1,0,1,0,1)
		#
		self.button2 = gtk.Button(_('Cancel'))
		self.button2.connect('clicked',self.close_cancel)
		table2.attach(self.button2,1,2,0,1)
		#***************************************************************		
		if os.path.exists(os.path.join(os.getenv("HOME"),".config/autostart/touchpad-indicator.py.desktop")):
			self.checkbutton1.set_active(True)
		self.on_mouse_plugged = 'disable'
		gconfi = GConf()
		try:
			self.on_mouse_plugged = gconfi.get_key('/apps/touchpad-indicator/options/on_mouse_plugged')
		except ValueError:
			gconfi.set_key('/apps/touchpad-indicator/options/on_mouse_plugged','disable')
		if self.on_mouse_plugged == 'disable':
			self.checkbutton2.set_active(True)
		else:
			self.checkbutton2.set_active(False)

		k=gconfi.get_key('/desktop/gnome/keybindings/touchpad_indicator/binding')
		if k!=None and len(k)>0:
			k=k[k.rfind('>')+1:]
			self.entry11.set_text(k)
			self.key=k		
		#
		self.show_all()
		#
		#
		#
	def close_application(self, widget, event, data=None):
		self.ok = False
		self.hide()
		
	def close_ok(self,widget):
		gconfi = GConf()
		gconfi.set_key('/desktop/gnome/keybindings/touchpad_indicator/action','/usr/share/touchpad-indicator/change_touchpad_state.py')
		gconfi.set_key('/desktop/gnome/keybindings/touchpad_indicator/name','modify_touchpad_status')
		if len(self.entry11.get_text())>0:
			gconfi.set_key('/desktop/gnome/keybindings/touchpad_indicator/binding','<Control><Alt>'+self.entry11.get_text())			
		else:
			gconfi.set_key('/desktop/gnome/keybindings/touchpad_indicator/binding','')
		#
		#
		filestart = os.path.join(os.getenv("HOME"),".config/autostart/touchpad-indicator.py.desktop")
		if self.checkbutton1.get_active():
			if not os.path.exists(filestart):
				os.symlink('/usr/share/touchpad-indicator/touchpad-indicator.py.desktop',filestart)
		else:		
			if os.path.exists(filestart):
				os.remove(filestart)
		#
		#
		if self.checkbutton2.get_active():
			gconfi.set_key('/apps/touchpad-indicator/options/on_mouse_plugged','disable')
		else:
			gconfi.set_key('/apps/touchpad-indicator/options/on_mouse_plugged','none')
		
		#
		#
		self.ok = True
		self.hide()

	def close_cancel(self,widget):
		self.latitude = None
		self.longitude = None
		self.location = None
		self.temperature = None
		self.ok = False
		self.hide()

	def on_exit_activate(self,widget):
		self.hide()

	def on_entry11_key_release_event(self,widget,event):
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
				self.entry11.set_text(self.key)
			else:
				self.entry11.set_text(keyval)
				self.key = keyval
	
	def get_key(self):
		return self.key
if __name__ == "__main__":	
	cm = Preferences()
	cm.run()
	exit(0)
