#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
#
__author__="atareao"
__date__ ="$19-feb-2011$"
#
# get devices
#
# Copyright (C) 2011 Lorenzo Carbonell
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
import usb

def get_devices():
	busses = usb.busses()
	totdevices = []
	for bus in busses:
		devices = bus.devices
		for dev in devices:
			devstr = "0x%04x:0x%04x" % (dev.idVendor, dev.idProduct)
			totdevices.append(devstr)
	return totdevices
