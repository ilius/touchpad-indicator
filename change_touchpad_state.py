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
import pynotify
from touchpad import Touchpad
import locale
import gettext
import com

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext

 
bus = dbus.SessionBus()

def get_touch_enabled():
	touchpad = Touchpad()
	return touchpad.all_touchpad_enabled()

def set_touch_enabled(enabled):
	touchpad = Touchpad()
	if enabled == True:
		touchpad.enable_all_touchpads()
	else:
		touchpad.disable_all_touchpads()

def change_state():
	is_touch_enabled = not get_touch_enabled()
	set_touch_enabled(is_touch_enabled)
	if is_touch_enabled==True:
		notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Enabled'),com.ICON_ENABLED)
	else:
		notification = pynotify.Notification ('Touchpad-Indicator',_('Touchpad Disabled'),com.ICON_DISABLED)
	notification.show()	

try:
	touchpad_indicator_service = bus.get_object('es.atareao.touchpad_indicator_service', '/es/atareao/touchpad_indicator_service')
	change_state = touchpad_indicator_service.get_dbus_method('change_state', 'es.atareao.touchpad_indicator_service')
	change_state()
except dbus.exceptions.DBusException,argument:
	if str(argument).find('es.atareao.touchpad_indicator_service'):
		change_state()
exit(0)
