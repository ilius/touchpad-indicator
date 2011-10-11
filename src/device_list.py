#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# device_list.py
#
# Copyright (C) 2010,2011
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
# Miguel Angel Santamaría Rogado <leibag@gmail.com>
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

try:
    import pyudev
except:
    print('Error: no pyudev installed.')


def print_device_attrib(Device):
    print('------------------------------------------------------')
    print('sys_name: ' + Device.sys_name)
    for attrName, attrValue in Device.iteritems():
        print(attrName + ': ' + str(attrValue))

if __name__ == "__main__":
    context = pyudev.Context()

    print('---------------MICE----------------')
    mice_list = context.list_devices(subsystem='input', ID_INPUT_MOUSE=True)
    for device in mice_list:
        print('\n\n******************************************************')
        print('device: ' + device.sys_name)
        try:
            print('parent name: ' + device.parent['NAME'])
            print('parent attributes:')
            print_device_attrib(device.parent)
        except:
            print(device.sys_name + ' has no parent')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('device atributes:')
        print_device_attrib(device)

    print('\n\n-------------TOUCHPADS-------------')
    touch_list = context.list_devices(subsystem='input', ID_INPUT_TOUCHPAD=True)
    for device in touch_list:
        print('\n\n******************************************************')
        print('device: ' + device.sys_name)
        try:
            print('parent name: ' + device.parent['NAME'])
            print('parent attributes:')
            print_device_attrib(device.parent)
        except:
            print(device.sys_name + ' has no parent')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('device atributes:')
        print_device_attrib(device)

    print('\n\n-----------OTHER DEVICES-----------')
    others = context.list_devices(subsystem='input')
    for device in others:
        print('\n\n******************************************************')
        print('device: ' + device.sys_name)
        try:
            print('parent name: ' + device.parent['NAME'])
            print('parent attributes:')
            print_device_attrib(device.parent)
        except:
            print(device.sys_name + ' has no parent')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('device atributes:')
        print_device_attrib(device)
