#!/usr/bin/python
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
import cairo

import tempfile
from os.path import abspath, normpath, splitext

from time import sleep

import subprocess

import gettext

from subprocess import Popen, PIPE

app_name = 'xfce4-keyboard-overlay'
app_version = '0.1'

_ = gettext.gettext # i18n shortcut

class PropertyTree(dict):
    def __init__(self):
        dict.__init__(self)
        
    def add_property(self, path, prop, delim='/'):
        try:
            key, next_path = path.split(delim, 1)
            if key not in self.keys():
                self[key] = PropertyTree()
            if next_path:
                self[key].add_property(next_path, prop, delim)
        except ValueError:
            self[path] = prop
        except AttributeError:
            pass
            
    def get_property(self, path, delim='.'):
        try:
            key, next_path = path.split(delim, 1)
            if key not in self.keys():
                return None
            if next_path:
                return self[key].get_property(next_path, delim)
        except ValueError:
            return self[path]

class Settings:
    def __init__(self, channel):
        self.channel = channel
        self.props = self.get_xfconf_properties()
        
    def get_keys(self):
        cmd = 'xfconf-query -c %s -l' % self.channel
        out = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].decode("utf-8")
        keys = []
        for key in out.split('\n'):
            if '\override' not in key:
                keys.append( key.rstrip().lstrip() )
        return keys
        
    def get_xfconf_properties(self):
        keys = self.get_keys()
        props = PropertyTree()
        for key in keys:
            if key != '\'':
                cmd = 'xfconf-query -c %s -p \"%s\"' % (self.channel, key)
                val = Popen(cmd, shell=True, stdout=PIPE).communicate()[0].decode("utf-8").rstrip().lstrip()
                if len(val) != 0 and val != '\'':
                    props.add_property(key, val)
        return props
        
    def get_properties(self, prop, delim=None):
        if delim == None:
            if prop[0] == '.' or prop[0] == '/':
                delim = prop[0]
            else:
                if '/' in prop:
                    delim = '/'
                else:
                    delim = '.'
        if prop[0] != delim:
            return self.props.get_property(delim + prop, delim)
        else:
            return self.props.get_property(prop, delim)


wait_time = 3

border = 6
launcher_key = Gdk.KEY_Super_L

header_markup = "<big><big><b>%s</b></big></big>"
group_markup = "<big><b>%s</b></big>"
shortcut_combo_markup = "<b>%s</b>"
shortcut_description_markup = "%s"

font_color = Gdk.Color(65535, 65535, 65535)
button_color = Gdk.Color(11822, 11822, 11822)

# The following dictionaries are for text replacement.  The command being 
# matched is the key, whereas the description shown in the overlay is the value.
applications = {'xfdesktop --menu': 'Applications Menu', 
'exo-open --launch TerminalEmulator': 'Terminal Emulator', 
'pidgin': 'Pidgin Instant Messenger', 
'exo-open --launch WebBrowser': 'Web Browser', 
'xfce4-screenshooter -w': 'Take an application screenshot', 
'xfrun4': 'Run dialog', 'leafpad': 'Text Editor', 'xflock4': 'Lock the screen', 
'exo-open --launch FileManager': 'File Manager', 
'xfce4-screenshooter -f': 'Take a screenshot', 
'xfce4-display-settings --minimal': 'Display Settings', 
'exo-open --launch MailReader': 'Email Client', 
'gmusicbrowser': 'Music Application', 'abiword': 'Word Processor', 
'gnumeric': 'Spreadsheet application.', 'xfce4-appfinder': 'Application Finder'}
switching = {'cycle_windows_key': 'Switch between applications', 
'cycle_reverse_windows_key': 'Switch between applications (reverse)', 
'switch_window_key': 'Switch windows of current application'}
workspaces = {'move_window_prev_workspace_key': 'Move window to previous workspace.', 
'move_window_next_workspace_key': 'Move window to next workspace.'}
windows = {'show_desktop_key': 'Minimizes all windows.', 
'close_window_key': 'Closes the current window.', 
'maximize_horiz_key': 'Maximizes the current window horizontally.', 
'maximize_vert_key': 'Maximizes the current window vertically.', 
'maximize_window_key': 'Maximizes the current window.', 
'stick_window_key': 'Shows the current window on all workspaces.', 
'hide_window_key': 'Minimizes the current window.', 
'fullscreen_key': 'Shows the current window fullscreen.'}

# The following SingleInstance class is used to prevent multiple copies of the 
# application from being started when a keyboard shortcut is used.
class SingleInstance:
    """
    If you want to prevent your script from running in parallel just instantiate
    SingleInstance() class. If is there another instance already running it will
    exist the application with the message "Another instance is already running,
    quitting.", returning -1 error code.
    
    >>> me = SingleInstance()
    """
    def __init__(self):
        self.lockfile = normpath(tempfile.gettempdir() + '/' +
            splitext(abspath(__file__))[0].replace("/","-").replace(":","").replace("\\","-")  + '.lock')
        import fcntl, sys
        self.fp = open(self.lockfile, 'w')
        try:
            fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            sys.exit(-1)
            

class XfceKeyboardOverlay:
    """A Keyboard Shortcut Overlay (KSO) for Xfce.  It uses the xfconf module
    to query keyboard shortcut settings from xfconf, and applies text 
    replacement to show commands as user-friendly as possible.
    
    The overlay is designed to be called from a keyboard shortcut, with the
    launcher key variable set at the top of this file.  The overlay will 
    disappear when the launcher key is released or focus is lost."""
    def __init__(self, display_unknown=False):
        """Initialize the overlay interface and populate it with the user data."""
#        super(XfceKeyboardOverlay, self).__init__()
        self.display_unknown = display_unknown
        
        self.get_interface()
        
        #self.set_position(Gtk.WindowPosition.CENTER)
        self.last_screen = 0
        
        self.normal_opacity = 0.80
        self.border_radius = 2
        
        self.window.set_keep_above(True)
        
        # If the screen is composited, we will want to decorate it and make it
        # transparent.
        self.screen = self.window.get_screen()
        if self.screen.is_composited():
            self.window.set_visual( self.screen.get_rgba_visual() )
            
        self.window.ensure_style()

        shortcuts = self.get_keyboard_settings()
        self.add_shortcut_group(self.grid_applications, shortcuts[0])
        self.add_shortcut_group(self.grid_switching, shortcuts[1])
        self.add_shortcut_group(self.grid_workspaces, shortcuts[2])
        self.add_shortcut_group(self.grid_windows, shortcuts[3])
        
        shortcut_width = 0
        description_width = 0
        col = 0
        for grid in [self.grid_applications, self.grid_switching, self.grid_workspaces, self.grid_windows]:
            for child in grid.get_children():
                w = child.get_preferred_width()[0]
                if col == 0:
                    if w > shortcut_width:
                        shortcut_width = w
                    col = 1
                else:
                    if w > description_width:
                        description_width = w
                    col = 0
        for grid in [self.grid_applications, self.grid_switching, self.grid_workspaces, self.grid_windows]:
            grid.get_children()[0].set_size_request(shortcut_width, -1)
            grid.get_children()[1].set_size_request(description_width, -1)
        
        # Window closed, end program.
        self.window.connect("delete-event", Gtk.main_quit)
        # Catches key presses and releases.
        self.window.connect("key-release-event", self.on_keyboard_release)
        self.window.connect("key-press-event", self.on_keyboard_press)
        # When the window is drawn, do the coloring and compositing.
        self.window.connect("draw", self.area_draw)
        # Catches window focus events.
        self.window.connect("notify::is-active", self.on_focus_event)
        
        # Make sure we grab focus so we can grab keyboard events.
        self.window.grab_add()
        
    def get_interface(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('xfce4-keyboard-overlay.glade')
        
        self.window = self.builder.get_object('window')
        self.title = self.builder.get_object('label_title')
        self.title.set_markup( header_markup % _('Keyboard Shortcuts') )
        self.title.modify_fg(Gtk.StateType.NORMAL, font_color)
        
        self.label_applications = self.builder.get_object('label_applications')
        self.label_applications.set_markup( group_markup % _('Applications') )
        self.label_applications.modify_fg(Gtk.StateType.NORMAL, font_color)
        
        self.button_applications = self.builder.get_object('button_applications')
        #self.button_applications.modify_fg(Gtk.StateType.NORMAL, button_color)
        self.grid_applications = self.builder.get_object('grid_applications')
        
        self.label_switching = self.builder.get_object('label_switching')
        self.label_switching.set_markup( group_markup % _('Switching') )
        self.label_switching.modify_fg(Gtk.StateType.NORMAL, font_color)
        
        self.button_switching = self.builder.get_object('button_switching')
        self.grid_switching = self.builder.get_object('grid_switching')
        
        self.label_workspaces = self.builder.get_object('label_workspaces')
        self.label_workspaces.set_markup( group_markup % _('Workspaces') )
        self.label_workspaces.modify_fg(Gtk.StateType.NORMAL, font_color)
        
        self.button_workspaces = self.builder.get_object('button_workspaces')
        self.grid_workspaces = self.builder.get_object('grid_workspaces')
        
        self.label_windows = self.builder.get_object('label_windows')
        self.label_windows.set_markup( group_markup % _('Windows') )
        self.label_windows.modify_fg(Gtk.StateType.NORMAL, font_color)
        
        self.button_windows = self.builder.get_object('button_windows')
        self.grid_windows = self.builder.get_object('grid_windows')
        
        self.builder.connect_signals(self)
    
    def add_shortcut_group(self, grid, group):
        for item in group:
            self.add_shortcut(grid, item[0], item[1])
        self.add_shortcut(grid, '', '')
    
        
    def add_shortcut(self, grid, key_combo, description):
        """Add a shortcut to the group, with the parameters key_combo and 
        description.  Should be pretty straight-forward."""
        combo_text = Gtk.Label("")
        combo_text.set_markup(shortcut_combo_markup % key_combo)
        combo_text.modify_fg(Gtk.StateType.NORMAL, font_color)
        combo_text.set_halign(Gtk.Align.START)
        text = Gtk.Label("")
        text.set_markup(shortcut_description_markup % description)
        text.set_halign(Gtk.Align.START)
        text.modify_fg(Gtk.StateType.NORMAL, font_color)
        grid.add(combo_text)
        grid.attach_next_to(text, combo_text, Gtk.PositionType.RIGHT, 1, 1)
        
    def on_keyboard_press(self, widget, event):
        """On Key press events, exit."""
        Gtk.main_quit()
        
    def on_keyboard_release(self, widget, event):
        """On Key release events, exit."""
        Gtk.main_quit()
       # if event.keyval == launcher_key:
       #     Gtk.main_quit()
            
    def on_focus_event(self, widget, event=None):
        """Make sure we have had focus once.  If we lose focus after that, exit."""
        try:
            if self.focused:
                Gtk.main_quit()
        except AttributeError:
            self.focused = True
            
    def get_keyboard_settings(self):
        """Get the keyboard settings from xfconf.  Return the groups as a list
        in the following order: Applications, Switching, Workspaces, Windows."""
        #settings = xfconf.xfconf.Settings('xfce4-keyboard-shortcuts')
        settings = Settings('xfce4-keyboard-shortcuts')
        commands = settings.get_properties('commands.custom')
        wm = settings.get_properties('xfwm4.custom')
        # Applications
        order = ['xfdesktop --menu', 'xfce4-appfinder', 'xfrun4', 
        'exo-open --launch WebBrowser', 'exo-open --launch MailReader', 
        'exo-open --launch FileManager', 'exo-open --launch TerminalEmulator', 
        'leafpad', 'gmusicbrowser', 'pidgin', 'abiword', 'gnumeric']
        applications_list = []
        for item in order:
            for prop in commands:
                if commands[prop] == item:
                    combo = key_combo_cleaner(prop)
                    value = applications[commands[prop]]
                    applications_list.append( [combo, value] )
        # Switching
        order = ['cycle_windows_key', 'cycle_reverse_windows_key', 
        'switch_window_key']
        switching_list = []
        for item in order:
            for prop in wm:
                if wm[prop] == item:
                    combo = key_combo_cleaner(prop)
                    value = switching[wm[prop]]
                    switching_list.append( [combo, value] )
        # Workspaces
        workspaces_list = [['Ctrl + Alt + Cursor Keys', 'Switch Workspaces'], 
        ['Alt + Ctrl + 1 to 9', 'Move window to workspace 1 to 9'], 
        ['Ctrl + F1 to F12', 'Switch to workspace 1 to 12']]
        order = ['move_window_prev_workspace_key', 
                 'move_window_next_workspace_key']
        for item in order:
            for prop in wm:
                if wm[prop] == item:
                    combo = key_combo_cleaner(prop)
                    value = workspaces[wm[prop]]
                    workspaces_list.append( [combo, value] )
        # Windows
        order = ['show_desktop_key', 'close_window_key', 'maximize_horiz_key', 
        'maximize_vert_key', 'maximize_window_key', 'stick_window_key', 
        'hide_window_key', 'fullscreen_key']
        windows_list = []
        for item in order:
            for prop in wm:
                if wm[prop] == item:
                    combo = key_combo_cleaner(prop)
                    value = windows[wm[prop]]
                    windows_list.append( [combo, value] )
        windows_list.append( ['Alt + Left Mouse Drag', 'Move window.'] )
        return [ applications_list,
                  switching_list,
                  workspaces_list,
                  windows_list
                ]
        
    def area_draw(self, widget, cr):
        """When the screen is drawn, determine if we are composited and draw
        the window appropriately."""
        if self.screen.is_composited():
            # If the screen is composited, let's make the window transparent
            # and round the edges.  Radius rounding is defined by r.
            cr.set_source_rgba(.0, .0, .0, 0.0)
            cr.set_operator(cairo.OPERATOR_SOURCE)
            cr.paint()
            cr.set_operator(cairo.OPERATOR_OVER)
            x = 0
            r = 24
            y = 0
            w = self.window.get_allocated_width()
            h = self.window.get_allocated_height()
            cr.move_to(x+r,y)
            cr.line_to(x+w-r,y)
            cr.curve_to(x+w,y,x+w,y,x+w,y+r)
            cr.line_to(x+w,y+h-r)
            cr.curve_to(x+w,y+h,x+w,y+h,x+w-r,y+h)
            cr.line_to(x+r,y+h)
            cr.curve_to(x,y+h,x,y+h,x,y+h-r)
            cr.line_to(x,y+r)
            cr.curve_to(x,y,x,y,x+r,y)
            cr.stroke_preserve()
        cr.set_source_rgba(.2, .2, .2, 0.9)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        if self.screen.is_composited():
            cr.fill()
        else:
            cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        
    def on_button_applications_clicked(self, widget):
        subprocess.Popen('xfce4-keyboard-settings', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
    def on_button_switching_clicked(self, widget):
        subprocess.Popen('xfwm4-settings', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
    def on_button_workspaces_clicked(self, widget):
        subprocess.Popen('xfwm4-settings', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
    def on_button_windows_clicked(self, widget):
        subprocess.Popen('xfwm4-settings', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def key_combo_cleaner(combo):
    """Return a key combination that is easier on the eyes.  Remove '<' and '>'.
    Add '+' between keys, uppercase single letters, underline single letters 
    (broken), and return the key combo in title format."""
    combo = combo.split('>')
    newcombo = []
    for each in combo:
        if len(each) == 1:
            uppercase = each.upper()
            #if uppercase.isalpha():
            #    uppercase = '<u>%s</u>' % uppercase
            newcombo.append( uppercase )
        else:
            cleaneach = each
            cleaneach = cleaneach.replace('<', '').replace('Control', 'Ctrl').replace('Primary', 'Ctrl')
            newcombo.append( cleaneach )
    newcombo = ' + '.join(newcombo)
    newcombo = newcombo.title()
    return newcombo

if __name__=='__main__':
    # Make sure there is only a single instance of this application around.
    me = SingleInstance()
    
    # Add in wait time for keyboard shortcut once we figure out how to do it.
    #time.sleep(wait_time)

    # Init and show the overlay.
    overlay = XfceKeyboardOverlay()
    overlay.window.show_all()
    Gtk.main()
