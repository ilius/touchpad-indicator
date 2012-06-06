#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Name: config
Description: Modulo que permite copiar la configuracion a las cuentas de los usuarios en el equipo
Version:0.1
License: GPLv3
Copyright: Copyright (C) 2009  Ernesto Nadir Crespo Avila <ecrespo@debianvenezuela.org>
Author: Ernesto Nadir Crespo Avila
Email: ecrespo@debianvenezuela.org
"""

from commands import getstatusoutput

print getstatusoutput('gconftool-2 -R /desktop/gnome/keybindings')
print getstatusoutput('gconftool-2 -a /desktop/gnome/keybindings/touchpad-indicator')
print getstatusoutput('gconftool-2 --set --type string /desktop/gnome/keybindings/touchpad-indicator/binding "<Primary><Alt>x"')
print getstatusoutput('gconftool-2 -a /desktop/gnome/keybindings/touchpad-indicator')
print getstatusoutput('gconftool-2 --set --type string /desktop/gnome/keybindings/touchpad-indicator/binding ""')
print getstatusoutput('gconftool-2 -a /desktop/gnome/keybindings/touchpad-indicator')

'''
from commands import getstatusoutput
def conf_escritorio():
    usuarios = usuarios.get_users()
    for usuario in usuarios:
        ejecutar-root.ejecutar("cp -R ./conf/.*  /home/%s/" %usuario)
        r = getstatusoutput("sudo -u %s gconftool-2 --set --type string /apps/metacity/keybinding_commands/command_1 \"orca\"" %usuario)
        if r[0] <> 0: print "Error al colocar el acceso rapido de orca"
        r = getstatusoutput("sudo -u %s gconftool-2 --set --type string /apps/metacity/global_keybindings/run_command_1 \"<Super>o\" " %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/keybinding_commands/command_2 \"gnome-terminal\" " %usuario)
        if r[0] <> 0: print "Error al colocar el acceso rapido del terminal"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/global_keybindings/run_command_2 \"<Super>t'" " %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/keybinding_commands/command_3 \"oowriter\"" %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/global_keybindings/run_command_3 \"<Super>w\"" %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/keybinding_commands/command_4 \"iceweasel\"" %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/global_keybindings/run_command_4 \"<Super>n\"" %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/keybinding_commands/command_5 \"nautilus\"" %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/global_keybindings/run_command_5 \"<Super>h\"" %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/keybinding_commands/command_6 \"ooimpress\"" %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/global_keybindings/run_command_6 \"<Super>i\"" %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/keybinding_commands/command_7 \"pidgin\" %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"
        r = getstatusoutput("sudo -u tiflo gconftool-2 --set --type string /apps/metacity/global_keybindings/run_command_7 \"<Super>p\"" %usuario)
        if r[0] <> 0: print "Error al cambiar los accesos rápidos en gnome"

 '''
