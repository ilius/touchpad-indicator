#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# preferences.py
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
import locale
import gettext
import com
import shutil
from configurator import Configurator

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext

class Preferences():
	def __init__(self):
		self.configurator = Configurator(com.KEY)
		self.autostart = False
		self.on_mouse_plugged = False
		self.enable_on_exit = False
		self.enable_on_start = True
		self.start_hidden = False
		self.show_notifications = True
		self.theme = '0'
		self.shortcut = 'ctrl+alt+f'

	def check_autostart_dir(self):
		if not os.path.exists(com.AUTOSTART_DIR):
			os.makedirs(com.AUTOSTART_DIR)

	def create_or_remove_autostart(self,create):
		self.check_autostart_dir()
		if create == True:
			if not os.path.exists(com.FILE_AUTO_START):
				shutil.copyfile('/usr/share/touchpad-indicator/touchpad-indicator-autostart.desktop',com.FILE_AUTO_START)
		else:
			if os.path.exists(com.FILE_AUTO_START):
				os.remove(com.FILE_AUTO_START)

	def read(self):
		self.autostart = os.path.exists(com.FILE_AUTO_START)
		self.on_mouse_plugged = self.configurator.get('on-mouse-plugged')
		self.enable_on_start = self.configurator.get('enable-on-start')		
		self.enable_on_exit = self.configurator.get('enable-on-exit')
		self.start_hidden = self.configurator.get('start-hidden')
		self.show_notifications = self.configurator.get('show-notifications')
		self.shortcut = self.configurator.get('shortcut')
		self.theme = self.configurator.get('theme')
		
	def save(self):
		self.create_or_remove_autostart(self.autostart)
		self.configurator.set('on-mouse-plugged',self.on_mouse_plugged)
		self.configurator.set('enable-on-start',self.enable_on_start)
		self.configurator.set('enable-on-exit',self.enable_on_exit)
		self.configurator.set('start-hidden',self.start_hidden)
		self.configurator.set('show-notifications',self.show_notifications)
		self.configurator.set('shortcut',self.shortcut)	
		self.configurator.set('theme',self.theme)
		
	def set_default(self):
		self.autostart = False
		self.on_mouse_plugged = False
		self.enable_on_exit = False
		self.enable_on_start = True
		self.start_hidden = False
		self.show_notifications = True
		self.theme = '0'
		self.shortcut = 'ctrl+alt+f'
		self.save()
		
if __name__ == "__main__":
	pf = Preferences()
	pf.read()
	print pf.shortcut
	pf.shortcut = 'ctrl+alt+t'
	pf.save()
	exit(0)
