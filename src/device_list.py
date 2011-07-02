#!/usr/bin/env python

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
