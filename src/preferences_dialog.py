#! /usr/bin/python
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
from preferences import Preferences
import com

import locale
import gettext


locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext

class PreferencesDialog(Gtk.Dialog):

	def __init__(self):
		#
		self.preferences = Preferences()
		Gtk.Dialog.__init__(self, 'Touchpad Indicator | '+_('Preferences'),None,Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.set_size_request(500, 230)
		self.connect('close', self.close_application)
		self.set_icon_from_file(com.ICON)
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
		table1 = Gtk.Table(9,4,True)
		self.vbox2.add(table1)
		#
		self.label11 = Gtk.Label.new(_('Shortcut')+':')
		self.label11.set_alignment(0,0.5)
		table1.attach(self.label11,0,1,0,1)
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
		table1.attach(self.checkbutton3,0,2,3,4)
		#
		self.checkbutton4 = Gtk.CheckButton.new_with_label(_('Enable touchpad on start'))
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
		self.respuesta = self.run()
		if self.respuesta == Gtk.ResponseType.ACCEPT:
			self.close_ok()
		self.destroy()
		
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
			self.key = keyval

	def load_preferences(self):
		self.preferences.read()
		self.checkbutton1.set_active(self.preferences.autostart)
		self.checkbutton2.set_active(self.preferences.on_mouse_plugged)
		self.checkbutton3.set_active(self.preferences.enable_on_exit)
		self.checkbutton4.set_active(self.preferences.enable_on_start)
		self.checkbutton5.set_active(self.preferences.start_hidden)
		self.checkbutton6.set_active(self.preferences.show_notifications)
		key = self.preferences.shortcut
		if key.find('ctrl')>-1:
			self.ctrl.set_active(True)
		if key.find('alt')>-1:
			self.alt.set_active(True)
		self.entry11.set_text(key[-1:])
		option = self.preferences.theme
		if option == '0':
			self.radiobutton0.set_active(True)
		elif option == '1':
			self.radiobutton1.set_active(True)
		else:
			self.radiobutton2.set_active(True)

	def save_preferences(self):
		key=''
		if self.ctrl.get_active() == True:
			key+='ctrl+'
		if self.alt.get_active() == True:
			key+='alt+'
		key += self.entry11.get_text()
		key = key.lower().strip()
		theme = '0'
		if self.radiobutton1.get_active() == True:
			theme = '1'
		elif self.radiobutton2.get_active() == True:
			theme = '2'
		self.preferences.autostart = self.checkbutton1.get_active()
		self.preferences.on_mouse_plugged = self.checkbutton2.get_active()
		self.preferences.enable_on_exit = self.checkbutton3.get_active()
		self.preferences.enable_on_start = self.checkbutton4.get_active()
		self.preferences.start_hidden = self.checkbutton5.get_active()
		self.preferences.show_notifications = self.checkbutton6.get_active()
		self.preferences.shorcut = key
		self.preferences.theme = theme
		self.preferences.save()
		
if __name__ == "__main__":
	cm = PreferencesDialog()
	exit(0)
