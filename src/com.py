#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
#
#
# com.py
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

import os

######################################

def is_package():
    return __file__.find('src') < 0

######################################


VERSION = '0.9.1.2'
APPNAME = 'Touchpad-Indicator'
APP = 'touchpad-indicator'

# check if running from source
if is_package():
    ROOTDIR = '/usr/share/'
    LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
    APPDIR = os.path.join(ROOTDIR, APP)
    IMGDIR = '/usr/share/pixmaps'
else:
    VERSION = VERSION + '-src'
    ROOTDIR = os.path.dirname(__file__)
    LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../template1'))
    APPDIR = ROOTDIR
    IMGDIR = os.path.join(APPDIR, '../data/icons')

AUTOSTART_DIR = os.path.join(os.getenv('HOME'),'.config/autostart')
FILE_AUTO_START = os.path.join(AUTOSTART_DIR,'touchpad-indicator-autostart.desktop')

ICON = os.path.join(IMGDIR, 'touchpad-indicator.svg')
ICON_ENABLED = 'touchpad-indicator'
ICON_DISABLED = 'touchpad-indicator-disabled'

WATCHDOG = os.path.join(APPDIR, 'watchdog.py')
LISTENKBD = os.path.join(APPDIR, 'listenkbd.py')
KEY = 'apps.indicators.touchpad-indicator'
