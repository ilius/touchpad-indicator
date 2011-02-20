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
# Copyright (C) 2010 Lorenzo Carbonell
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
import gobject
import gtk
import appindicator
import pynotify
import locale
import gettext
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from preferences import Preferences
from configurator import GConf
import devices
import glib
import com

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext


icon_enabled = '/usr/share/pixmaps/touchpad-indicator.svg'
icon_disabled = '/usr/share/pixmaps/touchpad-indicator-disabled.svg'
gconf_touchpad_enabled = '/desktop/gnome/peripherals/touchpad/touchpad_enabled'

class TouchpadIndicator(dbus.service.Object):
	def __init__(self):
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
		self.indicator.set_icon(icon_enabled)
		self.indicator.set_attention_icon(icon_disabled)
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
		glib.timeout_add_seconds(1, self.work)

	def read_preferences(self):
		gconfi = GConf()
		
		self.touch_enabled = gconfi.get_key(gconf_touchpad_enabled)		
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
			if self.get_touch_enabled():
				for device in self.devices:
					for el in devices.get_devices():
						if device == el:
							self.change_state()
			else:
				esta = False
				for device in self.devices:
					if device in devices.get_devices():
						esta = True
						break
				if not esta:
					self.change_state()			
		return True

	@dbus.service.method('es.atareao.touchpad_indicator_service')
	def change_state(self):
		is_touch_enabled = not self.get_touch_enabled()
		self.set_touch_enabled(is_touch_enabled)
		if is_touch_enabled==True:
			self.menu_enabled_touchpad.set_label(_('Disable Touchpad'))
			self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Enabled'),icon_enabled)
			self.indicator.set_status(appindicator.STATUS_ACTIVE)
		else:
			self.menu_enabled_touchpad.set_label(_('Enable Touchpad'))
			self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Disabled'),icon_disabled)
			self.indicator.set_status(appindicator.STATUS_ATTENTION)
		self.notification.show()
		
		
	def get_touch_enabled(self):
		gconfi = GConf()
		self.touch_enabled = gconfi.get_key(gconf_touchpad_enabled)
		return self.touch_enabled
	
	def set_touch_enabled(self,enabled):
		gconfi = GConf()
		gconfi.set_key(gconf_touchpad_enabled,enabled)
	
	def set_menu(self):
		self.menu = gtk.Menu()
		#
		self.menu_enabled_touchpad=gtk.MenuItem(_('Disable Touchpad'))
		self.menu_preferences=gtk.MenuItem(_('Preferences'))
		self.menu_exit=gtk.MenuItem(_('Exit'))
		self.menu_separator1=gtk.MenuItem()
		self.menu_about=gtk.MenuItem(_('About...'))
		#
		self.menu.append(self.menu_enabled_touchpad)
		self.menu.append(self.menu_preferences)
		self.menu.append(self.menu_exit)
		self.menu.append(self.menu_separator1)
		self.menu.append(self.menu_about)	
		#	
		if self.get_touch_enabled()==True:
			self.indicator.set_status (appindicator.STATUS_ACTIVE)
		else:
			self.menu_enabled_touchpad.set_label(_('Enable Touchpad'))
			self.indicator.set_status (appindicator.STATUS_ATTENTION)
		#
		self.menu_enabled_touchpad.show()
		self.menu_preferences.show()
		self.menu_exit.show()
		self.menu_separator1.show()
		self.menu_about.show()
		#
		self.menu_enabled_touchpad.connect('activate', self.menu_touchpad_enabled_response)
		self.menu_preferences.connect('activate',self.menu_preferences_response)
		self.menu_exit.connect('activate', self.menu_exit_response)
		self.menu_about.connect('activate', self.menu_about_response)
		#menu.show()
		self.indicator.set_menu(self.menu)
	
	def menu_preferences_response(self,widget):
		preferences = Preferences()
		preferences.run()
		self.read_preferences()
		
	def menu_touchpad_enabled_response(self,widget):
		is_touch_enabled = not self.get_touch_enabled()
		self.set_touch_enabled(is_touch_enabled)
		if is_touch_enabled==True:
			self.menu_enabled_touchpad.set_label(_('Disable Touchpad'))
			self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Enabled'),icon_enabled)
			self.indicator.set_status(appindicator.STATUS_ACTIVE)
		else:
			self.menu_enabled_touchpad.set_label(_('Enable Touchpad'))
			self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Disabled'),icon_disabled)
			self.indicator.set_status(appindicator.STATUS_ATTENTION)
		self.notification.show()

	def menu_exit_response(self,widget):
		exit(0)

	def menu_about_response(self,widget):
		ad=gtk.AboutDialog()
		ad.set_name('Touchpad-Indicator')
		ad.set_version('0.7.0')
		ad.set_copyright('Copyrignt (c) 2011\nLorenzo Carbonell')
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
		#ad.set_logo(logo)
		#ad.set_logo_icon_name(icon_name)
		ad.set_program_name('Touchpad-Indicator')
		ad.run()
		ad.hide()

if __name__ == "__main__":
	DBusGMainLoop(set_as_default=True)
	tpi=TouchpadIndicator()
	gtk.main()
