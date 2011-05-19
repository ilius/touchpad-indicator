#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
#
__author__='atareao'
__date__ ='$30/10/2010'
#
# Touchpad-Indicator
# An indicator to show the status of the touchpad
#
# Adding keybiding
#
# Copyright (C) 2010-2011 Lorenzo Carbonell
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
import gobject
import gtk
import appindicator
import pynotify
import locale
import gettext
import webbrowser
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from preferences import Preferences
from configurator import GConf
import devices
import glib
from touchpad import Touchpad
import com

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext

class TouchpadIndicator(dbus.service.Object):
	def __init__(self):
		if dbus.SessionBus().request_name('es.atareao.touchpad_indicator') != dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER:
			print "application already running"
			exit(0)
		
		'''
		Categorias:
		* CATEGORY_APPLICATION_STATUS
		* CATEGORY_COMMUNICATIONS
		* CATEGORY_SYSTEM_SERVICES
		* CATEGORY_HARDWARE
		* CATEGORY_OTHER
		'''
		self.indicator = appindicator.Indicator ('Touchpad-Indicator', 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
		'''
		Estados:
		* STATUS_PASSIVE : The icon is hidden
		* STATUS_ACTIVE : The icon is visible
		* STATUS_ATTENTION : The icon changes to the attention icon, requesting some kind of interaction with the user
		'''	
		#
		#
		#
		self.indicator.set_status(appindicator.STATUS_ACTIVE)
		self.indicator.set_icon(com.ICON_ENABLED)
		#
		self.read_preferences()
		#
		self.set_menu()
		#
		#
		#
		bus_name = dbus.service.BusName('es.atareao.touchpad_indicator_service', bus=dbus.SessionBus())
		dbus.service.Object.__init__(self, bus_name, '/es/atareao/touchpad_indicator_service')
		#
		self.manual = False
		glib.timeout_add_seconds(1, self.work)

	def read_preferences(self):
		gconfi = GConf()
		touchpad = Touchpad()
		self.touch_enabled = self.get_touch_enabled()	
		self.key = ''
		self.on_mouse_plugged = False
		self.devices = []
		try:
			self.on_mouse_plugged = gconfi.get_key('/apps/touchpad-indicator/options/on_mouse_plugged')
		except ValueError:
			gconfi.set_key('/apps/touchpad-indicator/options/on_mouse_plugged',False)
		try:
			self.devices = gconfi.get_string_list('/apps/touchpad-indicator/options/devices')
		except ValueError:
			gconfi.set_string_list('/apps/touchpad-indicator/options/devices',[])
		
		try:
			k=gconfi.get_key('/desktop/gnome/keybindings/touchpad_indicator/binding')
			if k!=None and len(k)>0:
				k=k[k.rfind('>')+1:]
				self.key=k
			else:
				self.key = ''
		except ValueError:
			gconfi.set_key('/desktop/gnome/keybindings/touchpad_indicator/binding','')
	def work(self):
		if self.on_mouse_plugged:		
			for device in self.devices:
				for el in devices.get_devices():
					if device == el:
						if self.get_touch_enabled():
							self.menu_enabled_touchpad.set_visible(False)
							self.automatic_change_state(False)
							break
			else:
				esta = False
				for device in self.devices:
					if device in devices.get_devices():
						esta = True
						break
				if not esta and not self.manual:
					self.menu_enabled_touchpad.set_visible(True)
					self.automatic_change_state(True)
					
		return True

	@dbus.service.method('es.atareao.touchpad_indicator_service')
	def change_state(self):
		self.manual = True
		is_touch_enabled = not self.get_touch_enabled()
		if self.set_touch_enabled(is_touch_enabled) == True:
			if is_touch_enabled==True:
				self.menu_enabled_touchpad.set_label(_('Disable Touchpad'))
				self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Enabled'),com.ICON_ENABLED)
				self.indicator.set_icon(com.ICON_ENABLED)
			else:
				self.menu_enabled_touchpad.set_label(_('Enable Touchpad'))
				self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Disabled'),com.ICON_DISABLED)
				self.indicator.set_icon(com.ICON_DISABLED)
			self.notification.show()
		
	def automatic_change_state(self,state):
		self.manual = False
		if state != self.get_touch_enabled():
			is_touch_enabled = not self.get_touch_enabled()
			if self.set_touch_enabled(is_touch_enabled) == True:
				if is_touch_enabled==True:
					self.menu_enabled_touchpad.set_label(_('Disable Touchpad'))
					self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Enabled'),com.ICON_ENABLED)
					self.indicator.set_icon(com.ICON_ENABLED)
				else:
					self.menu_enabled_touchpad.set_label(_('Enable Touchpad'))
					self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Disabled'),com.ICON_DISABLED)
					self.indicator.set_icon(com.ICON_DISABLED)
				self.notification.show()
		
	def get_touch_enabled(self):
		touchpad = Touchpad()
		return touchpad.all_touchpad_enabled()
	
	def set_touch_enabled(self,enabled):
		touchpad = Touchpad()
		if enabled == True:
			return touchpad.enable_all_touchpads()
		else:
			return touchpad.disable_all_touchpads()

	def get_help_menu(self):
		help_menu =gtk.Menu()
		#		
		menu_project = gtk.MenuItem(_('Application Web...'))
		menu_help_online = gtk.MenuItem(_('Get help online...'))
		menu_translations = gtk.MenuItem(_('Translate this application...'))
		menu_bugs = gtk.MenuItem(_('Report a bug...'))
		menu_separator_help_menu=gtk.SeparatorMenuItem()
		menu_about=gtk.MenuItem(_('About'))
		#
		menu_project.connect('activate',self.on_menu_project_clicked)
		menu_help_online.connect('activate',self.on_menu_help_online_clicked)
		menu_translations.connect('activate',self.on_menu_translations_clicked)
		menu_bugs.connect('activate',self.on_menu_bugs_clicked)
		menu_about.connect('activate',self.menu_about_response)
		#
		menu_project.show()
		menu_help_online.show()
		menu_translations.show()
		menu_bugs.show()
		menu_separator_help_menu.show()
		menu_about.show()
		#
		help_menu.append(menu_project)
		help_menu.append(menu_help_online)
		help_menu.append(menu_translations)
		help_menu.append(menu_bugs)
		help_menu.append(menu_separator_help_menu)
		help_menu.append(menu_about)
		#
		help_menu.show()
		#
		return help_menu

	def set_menu(self):
		self.menu = gtk.Menu()
		#
		self.menu_enabled_touchpad=gtk.MenuItem(_('Disable Touchpad'))
		self.menu_preferences=gtk.MenuItem(_('Preferences'))
		self.menu_separator1=gtk.MenuItem()
		self.menu_help = gtk.MenuItem(_('Help'))
		self.menu_help.set_submenu(self.get_help_menu())
		self.menu_separator2=gtk.MenuItem()
		self.menu_exit=gtk.MenuItem(_('Exit'))
		#
		self.menu_enabled_touchpad.connect('activate', self.menu_touchpad_enabled_response)
		self.menu_preferences.connect('activate',self.menu_preferences_response)
		self.menu_exit.connect('activate', self.menu_exit_response)
		#
		self.menu_enabled_touchpad.show()
		self.menu_preferences.show()
		self.menu_separator1.show()
		self.menu_help.show()
		self.menu_separator2.show()
		self.menu_exit.show()		
		#
		self.menu.append(self.menu_enabled_touchpad)
		self.menu.append(self.menu_preferences)
		self.menu.append(self.menu_separator1)
		self.menu.append(self.menu_help)
		self.menu.append(self.menu_separator2)
		self.menu.append(self.menu_exit)
		#
		self.menu.show()
		self.indicator.set_menu(self.menu)
		self.indicator.set_status(appindicator.STATUS_ACTIVE)
		#	
		if self.get_touch_enabled()==True:
			self.indicator.set_icon(com.ICON_ENABLED)
		else:
			self.menu_enabled_touchpad.set_label(_('Enable Touchpad'))
			self.indicator.set_icon(com.ICON_DISABLED)
	
	def menu_preferences_response(self,widget):
		widget.set_sensitive(False)
		preferences = Preferences()
		self.read_preferences()
		widget.set_sensitive(True)
		
	def menu_touchpad_enabled_response(self,widget):
		self.manual = True
		is_touch_enabled = not self.get_touch_enabled()
		if self.set_touch_enabled(is_touch_enabled) == True:
			if is_touch_enabled==True:
				self.menu_enabled_touchpad.set_label(_('Disable Touchpad'))
				self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Enabled'),com.ICON_ENABLED)
				self.indicator.set_icon(com.ICON_ENABLED)
			else:
				self.menu_enabled_touchpad.set_label(_('Enable Touchpad'))
				self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Disabled'),com.ICON_DISABLED)
				self.indicator.set_icon(com.ICON_DISABLED)
			self.notification.show()

	def menu_exit_response(self,widget):
		exit(0)
		
	def on_menu_project_clicked(self,widget):
		webbrowser.open('https://launchpad.net/touchpad-indicator')
		
	def on_menu_help_online_clicked(self,widget):
		webbrowser.open('https://answers.launchpad.net/touchpad-indicator')
	
	def on_menu_translations_clicked(self,widget):
		webbrowser.open('https://translations.launchpad.net/touchpad-indicator')
	
	def on_menu_bugs_clicked(self,widget):
		webbrowser.open('https://bugs.launchpad.net/touchpad-indicator')		
			
	def menu_about_response(self,widget):
		widget.set_sensitive(False)
		ad=gtk.AboutDialog()
		ad.set_name(com.APPNAME)
		ad.set_version(com.VERSION)
		ad.set_copyright('Copyrignt (c) 2010-2011\nLorenzo Carbonell')
		ad.set_comments(_('An indicator for the Touchpad'))
		ad.set_license(''+
		'This program is free software: you can redistribute it and/or modify it\n'+
		'under the terms of the GNU General Public License as published by the\n'+
		'Free Software Foundation, either version 3 of the License, or (at your option)\n'+
		'any later version.\n\n'+
		'This program is distributed in the hope that it will be useful, but\n'+
		'WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY\n'+
		'or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for\n'+
		'more details.\n\n'+
		'You should have received a copy of the GNU General Public License along with\n'+
		'this program.  If not, see <http://www.gnu.org/licenses/>.')
		ad.set_website('http://www.atareao.es')
		ad.set_website_label('http://www.atareao.es')
		ad.set_authors(['Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
		ad.set_documenters(['Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
		ad.set_translator_credits(''+
		'Daniel Tao <https://launchpad.net/~danieltaoys-gmail>\n'+
		'Daniele "OpenNingia" Simonetti <https://launchpad.net/~oppifjellet>\n'+
		'Giorgi Maghlakelidze <https://launchpad.net/~dracid>\n'+
		'Javier García Díaz <https://launchpad.net/~jgd>\n'+
		'Jiri Grönroos <https://launchpad.net/~jiri-gronroos>\n'+
		'Lorenzo Carbonell <https://launchpad.net/~lorenzo-carbonell>\n'+
		'Luca Ferretti <https://launchpad.net/~elle.uca>\n'+
		'Mantas Kriaučiūnas <https://launchpad.net/~mantas>\n'+
		'Martino Barbon <https://launchpad.net/~martins999>\n'+
		'Montes Morgan <https://launchpad.net/~montes-morgan>\n'+
		'Nur Kholis Majid <https://launchpad.net/~kholis>\n'+
		'pibe <https://launchpad.net/~pibe>\n'+
		'Sergey Sedov <https://launchpad.net/~serg-sedov>\n'+
		'Velikanov Dmitry <https://launchpad.net/~velikanov-dmitry>\n'+
		'XsLiDian <https://launchpad.net/~xslidian>\n')
		ad.set_icon_from_file(com.ICON)
		ad.set_logo(gtk.gdk.pixbuf_new_from_file(com.ICON))
		ad.set_program_name(com.APPNAME)
		ad.run()
		ad.destroy()
		widget.set_sensitive(True)

if __name__ == "__main__":
	DBusGMainLoop(set_as_default=True)
	tpi=TouchpadIndicator()
	gtk.main()
	exit(0)
