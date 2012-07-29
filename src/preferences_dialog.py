#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# preferences_dialog.py
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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from configurator import Configuration
from gconfigurator import GConfManager
import os
import shutil
import comun
import locale
import gettext


locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(comun.APP, comun.LANGDIR)
gettext.textdomain(comun.APP)
_ = gettext.gettext

def check_autostart_dir():
	if not os.path.exists(comun.AUTOSTART_DIR):
		os.makedirs(comun.AUTOSTART_DIR)

def create_or_remove_autostart(create):
	check_autostart_dir()
	if create == True:
		if not os.path.exists(comun.FILE_AUTO_START):
			shutil.copyfile('/usr/share/touchpad-indicator/touchpad-indicator-autostart.desktop',comun.FILE_AUTO_START)
	else:
		if os.path.exists(comun.FILE_AUTO_START):
			os.remove(comun.FILE_AUTO_START)

def exist_touchpad_shortcut():
	gcm = GConfManager()
	for directory in gcm.get_dirs('/desktop/gnome/keybindings'):
		print directory
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

class PreferencesDialog(Gtk.Dialog):

	def __init__(self):
		#
		Gtk.Dialog.__init__(self, 'Touchpad Indicator | '+_('Preferences'),None,Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.set_size_request(500, 230)
		self.connect('close', self.close_application)
		self.set_icon_from_file(comun.ICON)
		#
		self.vbox1 = Gtk.VBox(spacing = 5)
		self.vbox1.set_border_width(5)
		self.get_content_area().add(self.vbox1)
		#
		self.frame1 = Gtk.Frame()
		self.vbox1.add(self.frame1)
		#***************************************************************
		self.vbox2 = Gtk.VBox(spacing = 5)
		self.vbox2.set_border_width(5)
		self.frame1.add(self.vbox2)
		table1 = Gtk.Table(9,5,True)
		self.vbox2.add(table1)
		#
		self.checkbutton0 = Gtk.CheckButton.new_with_label(_('Shortcut'))
		table1.attach(self.checkbutton0,0,1,0,1)
		#
		self.ctrl = Gtk.ToggleButton('Ctrl')
		table1.attach(self.ctrl,1,2,0,1)
		#
		self.alt = Gtk.ToggleButton('Alt')
		table1.attach(self.alt,2,3,0,1)
		#
		self.entry11 = Gtk.Entry()
		self.entry11.set_editable(False)
		self.entry11.set_width_chars(4)
		self.entry11.connect('key-release-event',self.on_entry11_key_release_event)
		table1.attach(self.entry11,3,4,0,1)
		#
		self.checkbutton1 = Gtk.CheckButton.new_with_label(_('Autostart'))
		table1.attach(self.checkbutton1,0,2,1,2)
		#
		self.checkbutton2 = Gtk.CheckButton.new_with_label(_('Disable touchpad when mouse plugged'))
		table1.attach(self.checkbutton2,0,2,2,3)
		#
		self.checkbutton3 = Gtk.CheckButton.new_with_label(_('Enable touchpad on exit'))
		self.checkbutton3.connect('clicked',self.on_checkbutton3_activate)
		table1.attach(self.checkbutton3,0,2,3,4)
		#
		self.checkbutton4 = Gtk.CheckButton.new_with_label(_('Disable touchpad on exit'))
		self.checkbutton4.connect('clicked',self.on_checkbutton4_activate)
		table1.attach(self.checkbutton4,0,2,4,5)
		#
		self.checkbutton5 = Gtk.CheckButton.new_with_label(_('Start hidden'))
		table1.attach(self.checkbutton5,0,2,5,6)
		#
		self.checkbutton6 = Gtk.CheckButton.new_with_label(_('Show notifications'))
		table1.attach(self.checkbutton6,0,2,6,7)
		#
		label1 = Gtk.Label.new(_('Select icon theme')+':')
		label1.set_alignment(0,0.5)
		table1.attach(label1,0,3,7,8)
		self.radiobutton0 = Gtk.RadioButton.new_with_label_from_widget(None,_('Normal'))
		table1.attach(self.radiobutton0,0,1,8,9)
		self.radiobutton1 = Gtk.RadioButton.new_with_label_from_widget(self.radiobutton0,_('Light'))
		table1.attach(self.radiobutton1,1,2,8,9)
		self.radiobutton2 = Gtk.RadioButton.new_with_label_from_widget(self.radiobutton0,_('Dark'))
		table1.attach(self.radiobutton2,2,3,8,9)
		#***************************************************************
		#
		self.load_preferences()
		#
		self.show_all()
		#
		#
		#
	def on_checkbutton3_activate(self,widget):
		if self.checkbutton3.get_active() and self.checkbutton4.get_active():
			self.checkbutton4.set_active(False)

	def on_checkbutton4_activate(self,widget):
		if self.checkbutton3.get_active() and self.checkbutton4.get_active():
			self.checkbutton3.set_active(False)

	def close_application(self, widget, event):
		self.destroy()
	
	def messagedialog(self,title,message):
		dialog = Gtk.MessageDialog(None,Gtk.DialogFlags.MODAL,Gtk.MessageType.INFO,buttons=Gtk.ButtonsType.OK)
		dialog.set_markup("<b>%s</b>" % title)
		dialog.format_secondary_markup(message)
		dialog.run()
		dialog.destroy()
		
	def close_ok(self):
		self.save_preferences()

	def on_entry11_key_release_event(self,widget,event):
		key=event.keyval
		# numeros / letras mayusculas / letras minusculas
		if ((key>47) and (key<58)) or ((key > 64) and (key < 91)) or ((key > 96) and (key < 123)):
			if Gdk.keyval_is_upper(event.keyval):
				keyval=Gdk.keyval_name(Gdk.keyval_to_lower(event.keyval))
			else:
				keyval=Gdk.keyval_name(event.keyval)
			self.entry11.set_text(keyval)
			print keyval
			print get_shortcuts()
			key=''
			if self.ctrl.get_active() == True:
				key+='<Primary>'
			if self.alt.get_active() == True:
				key+='<Alt>'
			key += self.entry11.get_text()
			print key
			print key in get_shortcuts()
			if key in get_shortcuts() and keyval!=self.key:
				dialog = Gtk.MessageDialog(	parent = self,
										flags = Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
										type = Gtk.MessageType.ERROR,
										buttons = Gtk.ButtonsType.OK_CANCEL,
										message_format = _('This shortcut <Control> + <Alt> + ')+keyval+_(' is assigned'))
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
		configuration = Configuration()
		first_time = configuration.get('first-time')
		version = configuration.get('version')
		if first_time or version != comun.VERSION:
			configuration.set_defaults()
			configuration.read()
		self.checkbutton0.set_active(configuration.get('shortcut_enabled'))
		self.checkbutton1.set_active(configuration.get('autostart'))
		self.checkbutton2.set_active(configuration.get('on_mouse_plugged'))
		self.checkbutton3.set_active(configuration.get('enable_on_exit'))
		self.checkbutton4.set_active(configuration.get('disable_on_exit'))
		self.checkbutton5.set_active(configuration.get('start_hidden'))
		self.checkbutton6.set_active(configuration.get('show_notifications'))
		key = configuration.get('shortcut')
		print key
		if key.find('<Primary>')>-1:
			self.ctrl.set_active(True)
		if key.find('<Alt>')>-1:
			self.alt.set_active(True)
		self.key = key[-1:]
		self.entry11.set_text(self.key)
		option = configuration.get('theme')
		if option == 'normal':
			self.radiobutton0.set_active(True)
		elif option == 'light':
			self.radiobutton1.set_active(True)
		else:
			self.radiobutton2.set_active(True)

	def save_preferences(self):
		configuration = Configuration()
		configuration.set('first-time',False)
		configuration.set('version',comun.VERSION)
		key=''
		if self.ctrl.get_active() == True:
			key+='<Primary>'
		if self.alt.get_active() == True:
			key+='<Alt>'
		key += self.entry11.get_text()		
		if self.radiobutton0.get_active() == True:
			theme = 'normal'
		elif self.radiobutton1.get_active() == True:
			theme = 'light'
		elif self.radiobutton2.get_active() == True:
			theme = 'dark'
		configuration.set('shortcut_enabled',self.checkbutton0.get_active())
		configuration.set('autostart',self.checkbutton1.get_active())
		create_or_remove_autostart(self.checkbutton1.get_active())
		configuration.set('on_mouse_plugged',self.checkbutton2.get_active())
		configuration.set('enable_on_exit',self.checkbutton3.get_active())
		configuration.set('disable_on_exit',self.checkbutton4.get_active())
		configuration.set('start_hidden',self.checkbutton5.get_active())
		configuration.set('show_notifications',self.checkbutton6.get_active())
		configuration.set('shortcut',key)
		configuration.set('theme',theme)
		configuration.save()
		gcm = GConfManager()
		gcm.set_value('/desktop/gnome/keybindings/touchpad-indicator/action','/usr/share/touchpad-indicator/change_touchpad_state.py')
		gcm.set_value('/desktop/gnome/keybindings/touchpad-indicator/name','Touchpad-Indicator')
		if self.checkbutton0.get_active():
			shortcut = key
		else:
			shortcut = ''
		gcm.set_value('/desktop/gnome/keybindings/touchpad-indicator/binding',shortcut)
		

if __name__ == "__main__":
	cm = PreferencesDialog()
	if 	cm.run() == Gtk.ResponseType.ACCEPT:
			cm.close_ok()
	cm.hide()
	cm.destroy()
	exit(0)
