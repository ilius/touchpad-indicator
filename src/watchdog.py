#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
__author__='Miguel Angel Santamaría Rogado'
__date__ ='$27/05/2011'
#
# watchdog.py
#
#
# Copyright (C) 2011 Miguel Angel Santamarí­a Rogado
# leibag@gmail.com
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
is_working = None

udev_context = pyudev.Context()


def is_mouse_plugged():
    """Return True if there is any mouse connected"""
    global udev_context

    mice = udev_context.list_devices(subsystem="input", ID_INPUT_MOUSE=True)
    if len(list(mice)) == 0:
        return False
    else:
        return True


def is_mouse(device):
    """Return True if device is a mouse"""
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
    global is_working

    bus = dbus.SessionBus()
    try:
        touchpad_indicator_service = bus.get_object\
                                ('es.atareao.touchpad_indicator_service', \
                                '/es/atareao/touchpad_indicator_service')
        on_mouse_detected_plugged = touchpad_indicator_service.get_dbus_method\
                                ('on_mouse_detected_plugged', \
                                'es.atareao.touchpad_indicator_service')
        on_mouse_detected_unplugged = touchpad_indicator_service.get_dbus_method\
                                ('on_mouse_detected_unplugged', \
                                'es.atareao.touchpad_indicator_service')
        is_working = touchpad_indicator_service.get_dbus_method\
                                ('is_working', \
                                'es.atareao.touchpad_indicator_service')
    except:
        exit(0)


def watch():
    """The watcher"""
    global on_mouse_detected_plugged
    global on_mouse_detected_unplugged
    global is_working
    global udev_context

    monitor = pyudev.Monitor.from_netlink(udev_context)
    #TODO: filter also by device_type, so we can get rid of is_mouse()
    monitor.filter_by(subsystem="input", device_type=None)

    for action, device in monitor:
        if is_working() != True:
            exit(0)
        if is_mouse(device):
            try:
                if action == "add":
                        on_mouse_detected_plugged()
                elif action == "remove":
                        on_mouse_detected_unplugged()
            except:
                exit(0)

if __name__ == "__main__":
    """Watcher for plug/unplug of mice from the system"""
    init_dbus()
    watch()
