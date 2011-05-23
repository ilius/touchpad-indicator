#!/usr/bin/env python
import os
import sys
import pynotify
import pyudev
import re
from copy import deepcopy
import dbus
 
# register to libnotify
if not pynotify.init("new-hardware"):
    print ("Cannot initialize libnotify")
    sys.exit(1)
devices = [
    {
        'type': 'CD-ROM Drive',
        'icon': 'media-optical',
        'detection': {
            'DEVTYPE': 'disk',
            'ID_TYPE': 'cd',
            'SUBSYSTEM': 'block' 
        }
    },
    {
        'type': 'Multimedia Player', #this must be BEFORE generic storage and USB devices
        'icon': 'multimedia-player',
        'detection': {
            'DEVTYPE':'usb_device',
            'SUBSYSTEM': 'usb',
            'ID_MEDIA_PLAYER': '*',
        }
    },
    #{
    #    'type': ('Disk Partition'),
    #    'icon': 'drive-removable-media',
    #    'detection': {
    #        'DEVTYPE':'partition',
    #        'ID_FS_USAGE':'filesystem',
    #        'ID_TYPE':'disk',
    #        'SUBSYSTEM':'block'
    #    }
    #},
    {
        'type': ('USB Storage Device'), # MemoryStick Reader?
        'icon': 'gnome-dev-media-ms',
        'detection': {
            'DEVTYPE':'disk',
            'ID_TYPE':'disk',
            'SUBSYSTEM':'block',
            'ID_BUS': 'usb',
            'ID_DRIVE_FLASH_MS' : '1'
        }
    },
    {
        'type': ('USB Storage Device'), #SmartMedia Reader?
        'icon': 'gnome-dev-media-sm',
        'detection': {
            'DEVTYPE':'disk',
            'ID_TYPE':'disk',
            'SUBSYSTEM':'block',
            'ID_BUS': 'usb',
            'ID_DRIVE_FLASH_SM' : '1'
        }
    },
    {
        'type': ('USB Storage Device'), #CompatFlash Reader?
        'icon': 'gnome-dev-media-cf',
        'detection': {
            'DEVTYPE':'disk',
            'ID_TYPE':'disk',
            'SUBSYSTEM':'block',
            'ID_BUS': 'usb',
            'ID_DRIVE_FLASH_CF' : '1'
        }
    },      
    {
        'type': ('SD/MMC Memory'),
        'icon': 'gnome-dev-media-sdmmc',
        'detection': {
            'SUBSYSTEM':'mmc'
        }
    },          
    {
        'type': ('Memory Stick'),
        'icon': 'gnome-dev-media-ms',
        'detection': {
            'SUBSYSTEM':'memstick'
        }
    },          
    {
        'type': ('USB Storage Device'), #SD Card Reader?
        'icon': 'gnome-dev-media-sdmmc',
        'detection': {
            'DEVTYPE':'disk',
            'ID_TYPE':'disk',
            'SUBSYSTEM':'block',
            'ID_BUS': 'usb',
            'ID_DRIVE_FLASH_SD' : '1'
        }
    },          
    {
        'type': ('USB Storage Device'),
        'icon': 'drive-removable-media',
        'detection': {
            'DEVTYPE':'disk',
            'ID_TYPE':'disk',
            'SUBSYSTEM':'block',
            'ID_BUS': 'usb'
        }
    },
    {
        'type': ('WiFi Device'),
        'icon': 'network-wireless',
        'detection': {
            'DEVTYPE':'wlan',
            'SUBSYSTEM': 'net'
        }
    },
    {
        'type': ('WebCam / TV Tuner'),
        'icon': 'camera-web',
        'detection': {
            'SUBSYSTEM': 'video4linux'
        }
    },
    {
        'type': ('Mouse'),
        'icon': 'mouse',
        'detection': {
            'ID_INPUT_MOUSE': '1',
            'ID_TYPE': 'hid',
            'SUBSYSTEM': 'input'
        }
    },
    {
        'type': ('Game Controller'),
        'icon': 'joystick',
        'detection': {
            'ID_INPUT_JOYSTICK': '1',
            'ID_TYPE': 'hid',
            'SUBSYSTEM': 'input'
        }
    },
    {
        'type': ('Sound Card'), # needs testing
        'icon': 'sound',
        'detection': {
            'ID_TYPE': 'sound',
            'SUBSYSTEM': 'sound'
        }
    },
    
    {
        'type': ('USB Modem'),
        'icon': 'modem',
        'detection': {
            'ID_BUS':'usb',
            'SUBSYSTEM': 'tty',
        }
    },
    {
        'type': ('Modem'),
        'icon': 'modem',
        'detection': {
            'ID_USB_DRIVER': 'cdc_acm',
            'SUBSYSTEM': 'tty'
        }
    },
    {
        'type': ('PDA Device'),
        'icon': 'pda',
        'detection': {
            'ID_USB_DRIVER': 'ipaq',
            'SUBSYSTEM': 'tty'
        }
    },    
    {
        'type': ('Keyboard'),
        'icon': 'gnome-dev-keyboard',
        'detection': {
            'ID_CLASS': 'kbd',
            'ID_TYPE': 'hid',
            'SUBSYSTEM': 'input'
        }
    },
    {
        'type': ('Digital Camera'),
        'icon': 'camera-photo',
        'detection': {
            'DEVTYPE':'usb_device',
            'ID_GPHOTO2': '1',
        }
    },    
    {
        'type': ('Network Device'),
        'icon': 'network-wired',
        'detection': {
            'ID_BUS':'pci',
            'SUBSYSTEM': 'net',
        }
    },
    {
        'type': ('USB Network Device'),
        'icon': 'network-wired',
        'detection': {
            'ID_BUS':'usb',
            'SUBSYSTEM': 'net',
        }
    },
    {
        'type': ('USB Device'),
        'icon': 'gnome-dev-unknown-usb',
        'detection': {
            'DEVTYPE':'usb_device',
            'SUBSYSTEM': 'usb',
        }
    },
]
def is_mouse_plugged():
	context = pyudev.Context()
	for device in context.list_devices(subsystem='input'):
		detected = detect_device(device)
		if detected != None:
			if detected['type'] == 'Mouse':
				return True
	return False

def cleanstr_cb(m):
    return unichr(int(eval('0'+m.group(1))))

def cleanstr(text):
    text = re.sub(r'\\(x([a-f0-9]{2}))', cleanstr_cb, text).encode('utf-8').strip()
    return text

def detect_device(device):
    for d in devices:
        d['name'] = ''
        detected = False  
        keys = d['detection'].keys()
        for k in keys:
            if k in device:
                if device[k] == d['detection'][k] or d['detection'][k] == '*':
                    detected = True
                else:
                    detected = False
                    break
            else:
                detected = False
                break
        if detected:
            result = deepcopy(d)
            
            if 'UDISKS_PRESENTATION_ICON_NAME' in device:
                result['icon'] = device['UDISKS_PRESENTATION_ICON_NAME']
            else:
                result['icon'] = result['icon']
            
            device_name = ''
            
            if 'ID_VENDOR_FROM_DATABASE' in device:
                device_name += device['ID_VENDOR_FROM_DATABASE'].strip()
            
            if 'ID_MODEL_FROM_DATABASE' in device:
                if device_name:
                    device_name += ' '
                device_name += device['ID_MODEL_FROM_DATABASE'].strip()
            
            if device_name == '' and 'ID_MODEL_ENC' in device and 'ID_VENDOR_ENC' in device:
                device_name += cleanstr(device['ID_VENDOR_ENC']) + ' '
                device_name += cleanstr(device['ID_MODEL_ENC'])
            
            if device_name == '' and 'ID_V4L_PRODUCT' in device:
                device_name = cleanstr(device['ID_V4L_PRODUCT'])
            
            if 'ID_FS_LABEL' in device and 'ID_FS_TYPE' in device:
                device_name = '%s (%s)' % (device['ID_FS_LABEL'], device['ID_FS_TYPE'])
            
            if device_name != '':
                 result['name'] = result['type'] + '\n' + device_name
            else:
                result['name'] = result['type']
            return result
        else:
            continue

if __name__ == '__main__':
	bus = dbus.SessionBus()
	try:
		touchpad_indicator_service = bus.get_object('es.atareao.touchpad_indicator_service', '/es/atareao/touchpad_indicator_service')
		on_mouse_detected_plugged = touchpad_indicator_service.get_dbus_method('on_mouse_detected_plugged', 'es.atareao.touchpad_indicator_service')
		on_mouse_detected_unplugged = touchpad_indicator_service.get_dbus_method('on_mouse_detected_unplugged', 'es.atareao.touchpad_indicator_service')
		is_working = touchpad_indicator_service.get_dbus_method('is_working', 'es.atareao.touchpad_indicator_service')
	except:
		exit(0)
	context = pyudev.Context()
	monitor = pyudev.Monitor.from_netlink(context)
	for action, device in monitor:
		if is_working() != True:
			exit(0)
		detected = detect_device(device)
		if detected != None:
			if detected['type'] == 'Mouse':
				if device['ACTION'] == 'add':
					try:
						on_mouse_detected_plugged(detected['type'])
					except:
						exit(0)
				elif device['ACTION'] == 'remove':
					try:
						on_mouse_detected_unplugged(detected['type'])
					except:
						exit(0)
	exit(0)
