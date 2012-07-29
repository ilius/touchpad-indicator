#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# watchdog.py
#
# Copyright (C) 2010,2011
# Miguel Angel Santamaría Rogado <leibag@gmail.com>
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
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
import pyudev
import dbus

on_mouse_detected_plugged = None
on_mouse_detected_unplugged = None
check_status = None

faulty_devices = [
	u'11/2/a/0', # TPPS/2 IBM TrackPoint
	u'11/2/5/7326'] # ImPS/2 ALPS GlidePoint

udev_context = pyudev.Context()


def is_mouse_plugged(blacklist=faulty_devices):
	"""Return True if there is any mouse connected
	   :param blacklist: list of devices to discard."""
	possible_mice = udev_context.list_devices(subsystem="input",
												ID_INPUT_MOUSE=True)
	mice_list = []

	if blacklist != None:
		for mouse in possible_mice:
			if mouse.parent != None and 'PRODUCT' in mouse.parent.keys() and mouse.parent['PRODUCT'] not in blacklist:
				mice_list.append(mouse)
	else:
		mice_list = list(possible_mice)

	if len(mice_list) == 0:
		return False
	else:
		return True


def is_mouse(device, blacklist=faulty_devices):
	"""Return True if device is a mouse.
	   :param device: pyudev.core.Device
	   :param blacklist: list of devices to discard."""
	if blacklist != None:
		try:
			if device.parent != None and 'PRODUCT' in device.parent.keys() and device.parent['PRODUCT'] in blacklist:
				return False
			elif 'PRODUCT' in device.keys() and device['PRODUCT'] in blacklist:
				return False
		except KeyError:
			# if no PRODUCT attribute, ignore the blacklist
			pass
	try:
		if device.asbool("ID_INPUT_MOUSE"):
			return True
		else:
			return False
	except KeyError:
		return False


def init_dbus():
	"""Initialize dbus parameters"""
	global on_mouse_detected_plugged
	global on_mouse_detected_unplugged
	global check_status

	bus = dbus.SessionBus()
	try:
		touchpad_indicator_service = bus.get_object\
								('es.atareao.touchpad_indicator_service',
								'/es/atareao/touchpad_indicator_service')
		on_mouse_detected_plugged = touchpad_indicator_service.get_dbus_method\
								('on_mouse_detected_plugged',
								'es.atareao.touchpad_indicator_service')
		on_mouse_detected_unplugged = touchpad_indicator_service.get_dbus_method\
								('on_mouse_detected_unplugged',
								'es.atareao.touchpad_indicator_service')
		check_status = touchpad_indicator_service.get_dbus_method\
								('check_status',
								'es.atareao.touchpad_indicator_service')
	except:
		print('watchdog: Failed to initialize dbus.')
		exit(0)


def watch():
	"""The watcher"""
	global on_mouse_detected_plugged
	global on_mouse_detected_unplugged
	global check_status
	global udev_context

	monitor = pyudev.Monitor.from_netlink(udev_context)
	#TODO: filter also by device_type, so we can get rid of is_mouse()
	monitor.filter_by(subsystem="input", device_type=None)

	while True:
		try:
			for action, device in monitor:
				if is_mouse(device):
					try:
						if action == "add":
							on_mouse_detected_plugged()
							check_status()
						elif action == "remove":
							on_mouse_detected_unplugged()
							check_status()
					except:
						print('watchdog: failed to comunicate.')
						exit(0)
		except IOError:
			print('watchdog: Return from suspend? Reseting the monitor.')
			# reset the monitor, altought not really needed
			# if we are coming back from suspend, because it only
			# fails the first iteration after the suspend
			monitor = pyudev.Monitor.from_netlink(udev_context)
			monitor.filter_by(subsystem="input", device_type=None)
			check_status()
			continue

if __name__ == "__main__":
	"""Watcher for plug/unplug of mice from the system"""
	init_dbus()
	watch()
