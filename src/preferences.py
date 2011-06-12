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
import com
import shutil
import gconf
from configurator import GConf
import devices
import time

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext

gconfi = GConf()

def set_key(key,value):
	gconfi.set_key(key,value)

def get_key(key,value):
	try:
		value = gconfi.get_key(key)
	except ValueError:
		gconfi.set_key(key,value)
	return value

def search_for_keys(chain):
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
	keys=search_for_keys('/apps/compiz/general/allscreens/options')
	keys+=search_for_keys('/apps/metacity/global_keybindings')
	keys+=search_for_keys('/apps/metacity/window_keybindings')
	for dire in gconfi.get_all_dirs('/desktop/gnome/keybindings'):
		keys+=search_for_keys(dire)
	return keys

class Keybindings():
	def __init__(self,combination_key,action):
		self.combination_key = combination_key
		self.action = action

	def get_combination_key(self):
		return self.combination_key
	
	def get_action(self):
		return self.action	
	
class Preferences(gtk.Dialog):
	def __init__(self):
		#
		gtk.Dialog.__init__(self, 'Touchpad Indicator | '+_('Preferences'),None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.set_size_request(500, 180)
		self.connect('close', self.close_application)
		self.set_icon_from_file(com.ICON)
		#
		self.vbox1 = gtk.VBox(spacing = 5)
		self.vbox1.set_border_width(5)
		self.get_content_area().add(self.vbox1)
		#
		self.frame1 = gtk.Frame()
		self.vbox1.add(self.frame1)
		#***************************************************************
		self.vbox2 = gtk.VBox(spacing = 5)
		self.vbox2.set_border_width(5)
		self.frame1.add(self.vbox2)
		table1 = gtk.Table(4,2,True)
		self.vbox2.add(table1)
		#
		self.label11 = gtk.Label(_('Shortcut')+': <Ctrl> + <Alt> +')
		table1.attach(self.label11,0,1,0,1)
		#
		self.entry11 = gtk.Entry()
		self.entry11.set_editable(False)
		self.entry11.set_width_chars(4)
		self.entry11.connect('key-release-event',self.on_entry11_key_release_event)
		table1.attach(self.entry11,1,2,0,1)
		#
		self.checkbutton1 = gtk.CheckButton(_('Autostart'))
		table1.attach(self.checkbutton1,0,2,1,2)
		#
		self.checkbutton2 = gtk.CheckButton(_('Disable touchpad when mouse plugged'))
		table1.attach(self.checkbutton2,0,2,2,3)
		#
		self.checkbutton3 = gtk.CheckButton(_('Enable touchpad at start'))
		table1.attach(self.checkbutton3,0,2,3,4)
		#***************************************************************		
		#
		self.load_preferences()
		#
		self.show_all()
		#
		#
		#
		self.respuesta = self.run()
		print self.respuesta
		if self.respuesta == gtk.RESPONSE_ACCEPT:
			self.close_ok()
		self.destroy()
		
	def close_application(self, widget, event):
		self.destroy()
	
	def messagedialog(self,title,message):
		dialog = gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,buttons=gtk.BUTTONS_OK)
		dialog.set_markup("<b>%s</b>" % title)
		dialog.format_secondary_markup(message)
		dialog.run()
		dialog.destroy()
		
	def close_ok(self):
		set_key('/desktop/gnome/keybindings/touchpad_indicator/action','/usr/share/touchpad-indicator/change_touchpad_state.py')
		set_key('/desktop/gnome/keybindings/touchpad_indicator/name','modify_touchpad_status')
		if len(self.entry11.get_text())>0:
			set_key('/desktop/gnome/keybindings/touchpad_indicator/binding','<Control><Alt>'+self.entry11.get_text())			
		else:
			set_key('/desktop/gnome/keybindings/touchpad_indicator/binding','')
		#
		#
		filestart = os.path.join(os.getenv("HOME"),".config/autostart/touchpad-indicator-autostart.desktop")
		if self.checkbutton1.get_active():
			if not os.path.exists(filestart):
				shutil.copyfile('/usr/share/touchpad-indicator/touchpad-indicator-autostart.desktop',filestart)
		else:		
			if os.path.exists(filestart):
				os.remove(filestart)
		#
		#
		set_key('/apps/touchpad-indicator/options/on_mouse_plugged',self.checkbutton2.get_active())	
		set_key('/apps/touchpad-indicator/options/on_start_enabled',self.checkbutton3.get_active())	

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
				msg = _('This shortcut <Control> + <Alt> + ')+keyval+_(' is assigned')
				dialog.set_property('title', 'Error')
				dialog.set_property('text', msg)				
				dialog.run()
				dialog.destroy()
				self.entry11.set_text(self.key)
			else:
				self.entry11.set_text(keyval)
				self.key = keyval
			
	def load_preferences(self):
		if os.path.exists(os.path.join(os.getenv("HOME"),".config/autostart/touchpad-indicator-autostart.desktop")):
			self.checkbutton1.set_active(True)
		self.key = ''
		self.on_start_enabled = False
		self.on_mouse_plugged = False
		self.devices = []
		self.on_mouse_plugged = get_key('/apps/touchpad-indicator/options/on_mouse_plugged',False)
		self.checkbutton2.set_active(self.on_mouse_plugged)		
		self.on_start_enabled = get_key('/apps/touchpad-indicator/options/on_start_enabled',False)
		self.checkbutton3.set_active(self.on_start_enabled)		
		k=get_key('/desktop/gnome/keybindings/touchpad_indicator/binding','')
		if k!=None and len(k)>0:
			k=k[k.rfind('>')+1:]
			self.key=k
		else:
			self.key = ''
		self.entry11.set_text(self.key)		
		
if __name__ == "__main__":	
	cm = Preferences()
	exit(0)
