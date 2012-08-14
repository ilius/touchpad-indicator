#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
# com.py
#
# Copyright (C) 2010,2011,2012
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

import os
import shutil
import locale
import gettext

######################################

def is_package():
	return __file__.find('src') < 0

######################################


VERSION = '0.9.3.12'
APPNAME = 'Touchpad-Indicator'
APP = 'touchpad-indicator'
APPCONF = APP + '.conf'


PARAMS = {
			'first-time':True,
			'version':'',
			'is_working':False,
			'shortcut_enabled':False,
			'autostart':False,
			'disable_touchpad_on_start_indicator':False,
			'on_mouse_plugged':False,
			'enable_on_exit':True,
			'disable_on_exit':False,
			'start_hidden':False,
			'show_notifications':True,
			'theme':'light',
			'touchpad_enabled':True,
			'shortcut':'<Primary><Alt>c'
			}


# check if running from source
STATUS_ICON = {}
if is_package():
	ROOTDIR = '/usr/share/'
	LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
	APPDIR = os.path.join(ROOTDIR, APP)
	GCONFXML = os.path.join(APPDIR,'touchpad-indicator.xml')
	IMGDIR = '/usr/share/pixmaps'
	ICON = os.path.join(IMGDIR, 'touchpad-indicator.svg')
	STATUS_ICON['normal'] = ('touchpad-indicator-normal-enabled','touchpad-indicator-normal-disabled')
	STATUS_ICON['light'] = ('touchpad-indicator-light-enabled','touchpad-indicator-light-disabled')
	STATUS_ICON['dark'] = ('touchpad-indicator-dark-enabled','touchpad-indicator-dark-disabled')
else:
	VERSION = VERSION + '-src'
	ROOTDIR = os.path.dirname(__file__)
	LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../template1'))
	LANG_DIR = '/usr/share/locale-langpack'
	APPDIR = ROOTDIR
	GCONFXML = os.path.join(APPDIR,'touchpad-indicator.xml')
	IMGDIR = os.path.normpath(os.path.join(APPDIR, '../data/icons'))
	ICON = os.path.join(IMGDIR, 'touchpad-indicator.svg')
	STATUS_ICON['normal'] = (os.path.join(IMGDIR,'touchpad-indicator-normal-enabled.svg'),os.path.join(IMGDIR,'touchpad-indicator-normal-disabled.svg'))
	STATUS_ICON['light'] = (os.path.join(IMGDIR,'touchpad-indicator-light-enabled.svg'),os.path.join(IMGDIR,'touchpad-indicator-light-disabled.svg'))
	STATUS_ICON['dark'] = (os.path.join(IMGDIR,'touchpad-indicator-dark-enabled.svg'),os.path.join(IMGDIR,'touchpad-indicator-dark-disabled.svg'))


CONFIG_DIR = os.path.join(os.path.expanduser('~'),'.config')
CONFIG_APP_DIR = os.path.join(CONFIG_DIR, APP)
CONFIG_FILE = os.path.join(CONFIG_APP_DIR, APPCONF)

AUTOSTART_DIR = os.path.join(CONFIG_DIR,'autostart')
FILE_AUTO_START = os.path.join(AUTOSTART_DIR,'touchpad-indicator-autostart.desktop')
WATCHDOG = os.path.join(APPDIR, 'watchdog.py')

####
locale.setlocale(locale.LC_ALL, '')
current_locale, encoding = locale.getdefaultlocale()
print 'Encoding: %s'%encoding
print 'Current Locale: %s'%current_locale
try:
	language = gettext.translation(APP, LANGDIR, languages = [current_locale])
	language.install(unicode=True)
	_ = language.ugettext
except Exception, e:
	print e
	_ = str
