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
import shlex
import subprocess
import gtk
import appindicator
import gconf
import pynotify
import locale
import gettext
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from shortcut import Shortcut
import glib



APP = 'touchpad-indicator'
DIR = '/usr/share/locale-langpack'

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext


icon_enabled = '/usr/share/pixmaps/touchpad-indicator.svg'
icon_disabled = '/usr/share/pixmaps/touchpad-indicator-disabled.svg'
gconf_touchpad_enabled = '/desktop/gnome/peripherals/touchpad/touchpad_enabled'

def ejecuta(comando):
	args = shlex.split(comando)
	p = subprocess.Popen(args, bufsize=10000, stdout=subprocess.PIPE)
	valor = p.communicate()[0]
	return valor


class TouchpadIndicator(dbus.service.Object):
	def __init__(self):
		self.gconf = gconf.client_get_default()
		self.touch_enabled = self.gconf.get_value(gconf_touchpad_enabled)		
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
		try:
			k=self.gconf.get_value('/desktop/gnome/keybindings/touchpad_indicator/binding')
			if k!=None and len(k)>0:
				k=k[k.rfind('>')+1:]
				self.key=k
			else:
				self.key = ''
		except ValueError:
			self.gconf.set_value('/desktop/gnome/keybindings/touchpad_indicator/binding','')
			self.key = ''
		#
		self.set_menu()
		#
		#
		#
		bus_name = dbus.service.BusName('es.atareao.touchpad_indicator_service', bus=dbus.SessionBus())
		dbus.service.Object.__init__(self, bus_name, '/es/atareao/touchpad_indicator_service')
		#
		glib.timeout_add_seconds(1, self.work)

	def work(self):
		print ejecuta('lsusb')
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
		self.touch_enabled = self.gconf.get_value(gconf_touchpad_enabled)
		return self.touch_enabled
	
	def set_touch_enabled(self,enabled):
		self.gconf.set_value(gconf_touchpad_enabled,enabled)
	
	def set_menu(self):
		self.menu = gtk.Menu()
		#
		self.menu_enabled_touchpad=gtk.MenuItem(_('Disable Touchpad'))
		self.menu_shortcut=gtk.MenuItem(_('Shortcut'))
		self.menu_exit=gtk.MenuItem(_('Exit'))
		self.menu_separator1=gtk.MenuItem()
		self.menu_about=gtk.MenuItem(_('About...'))
		#
		self.submenu = gtk.Menu()
		self.submenu_set_shortcut=gtk.MenuItem(_('Set shortcut'))
		self.submenu_del_shortcut=gtk.MenuItem(_('Remove shortcut'))
		self.submenu.append(self.submenu_set_shortcut)
		self.submenu.append(self.submenu_del_shortcut)
		self.menu_shortcut.set_submenu(self.submenu)
		self.submenu_set_shortcut.show()
		self.submenu_del_shortcut.show()
		self.submenu_set_shortcut.connect('activate', self.submenu_set_shortcut_response)
		self.submenu_del_shortcut.connect('activate', self.submenu_del_shortcut_response)
		#
		self.menu.append(self.menu_enabled_touchpad)
		self.menu.append(self.menu_shortcut)
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
		self.menu_shortcut.show()
		self.menu_exit.show()
		self.menu_separator1.show()
		self.menu_about.show()
		#
		self.menu_enabled_touchpad.connect('activate', self.menu_touchpad_enabled_response)
		self.menu_exit.connect('activate', self.menu_exit_response)
		self.menu_about.connect('activate', self.menu_about_response)
		#menu.show()
		self.indicator.set_menu(self.menu)
		
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

	def submenu_set_shortcut_response(self,widget):
		shortcut=Shortcut()
	
	def submenu_del_shortcut_response(self,widget):
		self.gconf.set_value('/desktop/gnome/keybindings/touchpad_indicator/binding','')

	def menu_exit_response(self,widget):
		exit(0)

	def menu_about_response(self,widget):
		ad=gtk.AboutDialog()
		ad.set_name('Touchpad-Indicator')
		ad.set_version('0.7.0')
		ad.set_copyright('Copyrignt (c) 2011\nLorenzo Carbonell')
		ad.set_comments(_('An indicator for the Touchpad'))
		ad.set_license(_(''+
		'This program is free software: you can redistribute it and/or modify it\n'+
		'under the terms of the GNU General Public License as published by the\n'+
		'Free Software Foundation, either version 3 of the License, or (at your option)\n'+
		'any later version.\n\n'+
		'This program is distributed in the hope that it will be useful, but\n'+
		'WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY\n'+
		'or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for\n'+
		'more details.\n\n'+
		'You should have received a copy of the GNU General Public License along with\n'+
		'this program.  If not, see <http://www.gnu.org/licenses/>.'))		
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
