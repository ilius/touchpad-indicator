#!/usr/bin/python
# -*- coding: utf-8 -*-
#
__author__='atareao'
__date__ ='$21/11/2010'
#
# Check touchpad status of Touchpad-Indicator
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
from touchpad import Touchpad
from configurator import Configuration
import time

if __name__ == '__main__':
	touchpad = Touchpad()
	configuration = Configuration()
	touchpad_enabled = configuration.get('touchpad_enabled')
	touchpad_indicator_working = configuration.get('is_working')
	if touchpad_indicator_working:
		print('Touchpad-Indicator is working')
		if touchpad_enabled != touchpad.are_all_touchpad_enabled():
			if touchpad_enabled:
				if touchpad.enable_all_touchpads():
					configuration.set('touchpad_enabled',self.touchpad.are_all_touchpad_enabled())
					configuration.save()
			else:
				if touchpad.disable_all_touchpads():
					configuration.set('touchpad_enabled',self.touchpad.are_all_touchpad_enabled())
					configuration.save()
	else:
		print('Touchpad-Indicator is not working')
	if touchpad.are_all_touchpad_enabled():
		print('Touchpad is enabled')
	else:
		print('Touchpad is disabled')

	'''
	error = True
	time.sleep(1)
	while error:
		try:
			bus = dbus.SessionBus()
			error = False
		except:
			time.sleep(1)
	try:
		touchpad_indicator_service = bus.get_object('es.atareao.touchpad_indicator_service', '/es/atareao/touchpad_indicator_service')
		check_status = touchpad_indicator_service.get_dbus_method('check_status', 'es.atareao.touchpad_indicator_service')
		check_status()
		print('Touchpad-Indicator is working')
	except dbus.exceptions.DBusException,argument:
		print argument
		print('Touchpad-Indicator is not working')
	'''
	exit(0)
