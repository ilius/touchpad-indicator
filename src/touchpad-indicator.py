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
import subprocess
import watchdog

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext

def add2menu(menu, text = None, icon = None, conector_event = None, conector_action = None):
	if text != None and icon == None:
		menu_item = gtk.MenuItem(text)
	elif text == None and icon != None:
		menu_item = gtk.ImageMenuItem()
		image = gtk.Image()
		image.set_from_file(icon)
		menu_item.set_image(image)
	elif text != None and icon != None:
		menu_item = gtk.ImageMenuItem(text)
		image = gtk.Image()
		image.set_from_file(icon)
		menu_item.set_image(image)
		menu_item.set_always_show_image(True)
	elif icon == None:
		menu_item = gtk.MenuItem(text)
	else:
		menu_item = gtk.SeparatorMenuItem()
	if conector_event != None and conector_action != None:				
		menu_item.connect(conector_event,conector_action)
	menu_item.show()
	menu.append(menu_item)
	return menu_item

class TouchpadIndicator(dbus.service.Object):
	def __init__(self):
		if dbus.SessionBus().request_name('es.atareao.touchpad_indicator') != dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER:
			print "application already running"
			exit(0)
		self.indicator = appindicator.Indicator ('Touchpad-Indicator', 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
		#
		bus_name = dbus.service.BusName('es.atareao.touchpad_indicator_service', bus=dbus.SessionBus())
		dbus.service.Object.__init__(self, bus_name, '/es/atareao/touchpad_indicator_service')
		#
		self.icon_theme =  gtk.icon_theme_get_default()
		self.icon_theme.prepend_search_path(com.IMGDIR)
		#
		self.touchpad = Touchpad()
		self.is_working = True
		#
		self.the_watchdog = None
		#
		self.read_preferences()
		#
		self.set_menu()

	def set_touch_enabled(self,enabled):
		if enabled == True and self.touchpad.all_touchpad_enabled() == False:
			self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Enabled'),com.ICON_ENABLED)
			self.notification.show()
			self.touchpad.enable_all_touchpads()
		elif enabled == False and self.touchpad.all_touchpad_enabled() == True:
			self.notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Disabled'),com.ICON_DISABLED)
			self.notification.show()
			self.touchpad.disable_all_touchpads()
		if self.touchpad.all_touchpad_enabled() == True:
			self.menu_enabled_touchpad.set_label(_('Disable Touchpad'))
			self.indicator.set_icon(com.ICON_ENABLED)
		else:
			self.menu_enabled_touchpad.set_label(_('Enable Touchpad'))
			self.indicator.set_icon(com.ICON_DISABLED)
		return True

	@dbus.service.method('es.atareao.touchpad_indicator_service')
	def on_mouse_detected_plugged(self):
		if self.on_mouse_plugged == True:
			self.menu_enabled_touchpad.set_sensitive(False)
			self.set_touch_enabled(False)

	@dbus.service.method('es.atareao.touchpad_indicator_service')
	def on_mouse_detected_unplugged(self):
		if self.on_mouse_plugged == True:
			self.menu_enabled_touchpad.set_sensitive(True)
			self.set_touch_enabled(True)

	@dbus.service.method('es.atareao.touchpad_indicator_service')
	def is_working(self):
		return self.is_working
		
	@dbus.service.method('es.atareao.touchpad_indicator_service')
	def change_state(self):
		if self.on_mouse_plugged == False or watchdog.is_mouse_plugged() == False:
			is_touch_enabled = not self.touchpad.all_touchpad_enabled()
			self.set_touch_enabled(is_touch_enabled)

	def read_preferences(self):
		gconfi = GConf()
		self.key = ''
		self.on_mouse_plugged = False
		self.on_start_enabled = False
		try:
			self.on_mouse_plugged = gconfi.get_key('/apps/touchpad-indicator/options/on_mouse_plugged')
		except ValueError:
			gconfi.set_key('/apps/touchpad-indicator/options/on_mouse_plugged',False)
		try:
			self.on_start_enabled = gconfi.get_key('/apps/touchpad-indicator/options/on_start_enabled')
		except ValueError:
			gconfi.set_key('/apps/touchpad-indicator/options/on_start_enabled',False)
		if self.on_mouse_plugged == True:
			if self.the_watchdog == None:
				self.the_watchdog = subprocess.Popen(com.WATCHDOG)
		else:
			if self.the_watchdog != None:
				self.the_watchdog.kill()
				self.the_watchdog = None
		try:
			k=gconfi.get_key('/desktop/gnome/keybindings/touchpad_indicator/binding')
			if k!=None and len(k)>0:
				k=k[k.rfind('>')+1:]
				self.key=k
			else:
				self.key = ''
		except ValueError:
			gconfi.set_key('/desktop/gnome/keybindings/touchpad_indicator/binding','')

	def menu_touchpad_enabled_response(self,widget):
		self.change_state()

	def get_help_menu(self):
		help_menu =gtk.Menu()
		#		
		add2menu(help_menu,text = _('Application Web...'),conector_event = 'activate',conector_action = self.on_menu_project_clicked)
		add2menu(help_menu,text = _('Get help online...'),conector_event = 'activate',conector_action = self.on_menu_help_online_clicked)
		add2menu(help_menu,text = _('Translate this application...'),conector_event = 'activate',conector_action = self.on_menu_translations_clicked)
		add2menu(help_menu,text = _('Report a bug...'),conector_event = 'activate',conector_action = self.on_menu_bugs_clicked)
		add2menu(help_menu)
		add2menu(help_menu,text = _('About'),conector_event = 'activate',conector_action = self.menu_about_response)
		#
		help_menu.show()
		#
		return help_menu

	def set_menu(self):
		self.menu = gtk.Menu()
		#
		self.menu_enabled_touchpad=add2menu(self.menu,text = _('Disable Touchpad'),conector_event = 'activate',conector_action = self.menu_touchpad_enabled_response)
		add2menu(self.menu,text = _('Preferences'),conector_event = 'activate',conector_action = self.menu_preferences_response)
		add2menu(self.menu)
		self.menu_help = add2menu(self.menu,text = _('Help'))
		self.menu_help.set_submenu(self.get_help_menu())
		add2menu(self.menu)
		self.menu_separator2=gtk.MenuItem()
		add2menu(self.menu,text = _('Exit'),conector_event = 'activate',conector_action = self.menu_exit_response)
		#
		self.menu.show()
		self.indicator.set_menu(self.menu)
		self.indicator.set_status(appindicator.STATUS_ACTIVE)
		#			
		if self.on_mouse_plugged == True and watchdog.is_mouse_plugged() == True:
			if self.touchpad.all_touchpad_enabled()==True:
				self.set_touch_enabled(False)
			self.menu_enabled_touchpad.set_sensitive(False)
		else:
			if self.on_start_enabled == True and self.touchpad.all_touchpad_enabled()==False:
				self.set_touch_enabled(True)
			self.menu_enabled_touchpad.set_sensitive(True)
		if self.touchpad.all_touchpad_enabled() == True:
			self.menu_enabled_touchpad.set_label(_('Disable Touchpad'))
			self.indicator.set_icon(com.ICON_ENABLED)
		else:
			self.menu_enabled_touchpad.set_label(_('Enable Touchpad'))
			self.indicator.set_icon(com.ICON_DISABLED)			

	def menu_preferences_response(self,widget):
		widget.set_sensitive(False)
		preferences = Preferences()
		self.read_preferences()
		self.set_menu()
		widget.set_sensitive(True)

	def menu_exit_response(self,widget):
		self.is_working = False
		if self.the_watchdog != None:
			self.the_watchdog.kill()
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
		ad.set_authors(['Lorenzo Carbonell <https://launchpad.net/~lorenzo-carbonell>','Miguel Angel Santamaría Rogado <https://launchpad.net/~gabiel>'])
		ad.set_documenters(['Lorenzo Carbonell <https://launchpad.net/~lorenzo-carbonell>'])
		ad.set_translator_credits(''+
		'Ander Elortondo <https://launchpad.net/~ander-elor>\n'+
		'anyone28 <https://launchpad.net/~b4025475>\n'+
		'Candido Fernandez <https://launchpad.net/~candidinho>\n'+
		'Fitoschido <https://launchpad.net/~fitoschido>\n'+
		'Giorgi Maghlakelidze <https://launchpad.net/~dracid>\n'+
		'ipadro <https://launchpad.net/~ivan-patfran>\n'+
		'Javier García Díaz <https://launchpad.net/~jgd>\n'+
		'Jiri Grönroos <https://launchpad.net/~jiri-gronroos>\n'+
		'José Roitberg <https://launchpad.net/~roitberg>\n'+
		'Lorenzo Carbonell <https://launchpad.net/~lorenzo-carbonell>\n'+
		'Mantas Kriaučiūnas <https://launchpad.net/~mantas>\n'+
		'Marek Tyburec <https://launchpad.net/~marek-tyburec>\n'+
		'Miguel Anxo Bouzada <https://launchpad.net/~mbouzada>\n'+
		'Montes Morgan <https://launchpad.net/~montes-morgan>\n'+
		'Nur Kholis Majid <https://launchpad.net/~kholis>\n'+
		'pibe <https://launchpad.net/~pibe>\n'+
		'rodion <https://launchpad.net/~rodion-samusik>\n'+
		'Velikanov Dmitry <https://launchpad.net/~velikanov-dmitry>\n'+
		'XsLiDian <https://launchpad.net/~xslidian>\n'+
		'Yared Hufkens <https://launchpad.net/~w38m4570r>\n')
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
