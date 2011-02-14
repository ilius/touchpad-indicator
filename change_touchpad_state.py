#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
#
__author__='atareao'
__date__ ='$21/11/2010'
#
# Change state of Touchpad-Indicator
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
import dbus
import gconf
import pynotify
import locale
import gettext

APP = 'touchpad-indicator'
DIR = '/usr/share/locale-langpack'

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext

 
bus = dbus.SessionBus()
icon_enabled = '/usr/share/pixmaps/touchpad-indicator.svg'
icon_disabled = '/usr/share/pixmaps/touchpad-indicator-disabled.svg'
gconf_touchpad_enabled = '/desktop/gnome/peripherals/touchpad/touchpad_enabled'

def get_touch_enabled():
	gconfi = gconf.client_get_default()
	touch_enabled = gconfi.get_value(gconf_touchpad_enabled)
	return touch_enabled

def set_touch_enabled(enabled):
	gconfi = gconf.client_get_default()
	gconfi.set_value(gconf_touchpad_enabled,enabled)

def change_state():
	is_touch_enabled = not get_touch_enabled()
	set_touch_enabled(is_touch_enabled)
	if is_touch_enabled==True:
		notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Enabled'),icon_enabled)
	else:
		notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Disabled'),icon_disabled)
	notification.show()	


try:
	touchpad_indicator_service = bus.get_object('es.atareao.touchpad_indicator_service', '/es/atareao/touchpad_indicator_service')
	change_state = touchpad_indicator_service.get_dbus_method('change_state', 'es.atareao.touchpad_indicator_service')
	change_state()
except dbus.exceptions.DBusException,argument:
	if str(argument).find('es.atareao.touchpad_indicator_service'):
		change_state()
exit(0)
