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
 
bus = dbus.SessionBus()

if __name__ == '__main__':
	try:
		touchpad_indicator_service = bus.get_object('es.atareao.touchpad_indicator_service', '/es/atareao/touchpad_indicator_service')
		change_state = touchpad_indicator_service.get_dbus_method('change_state', 'es.atareao.touchpad_indicator_service')
		change_state()
		print('Touchpad-Indicator is working')
	except dbus.exceptions.DBusException,argument:
		print('Touchpad-Indicator is not working')
	exit(0)
