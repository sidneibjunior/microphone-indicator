#!/usr/bin/python

# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
# https://gist.github.com/candidtim/7290a1ad6e465d680b68

import os
import signal
import json
import subprocess
import re
import gi

from urllib2 import Request, urlopen # URLError

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
gi.require_version('Keybinder', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import Keybinder


APPINDICATOR_ID = 'micindicator'
# amixer get Capture | egrep 'Front Left.*?\[o' | egrep -o '\[o.+\]'

class Indicator():
    def __init__(self):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, self.get_current_state_icon(), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.update_mic_state()
        notify.init(APPINDICATOR_ID)

        keystr = "<Ctrl><Alt><Shift>M"
        Keybinder.init()
        Keybinder.set_use_cooked_accelerators(False)
        Keybinder.bind(keystr, self.callback_toggle_mic, "keystring %s (user data)" % keystr)
        print ("Press '" + keystr + "' to toggle microphone mute")

    def callback_toggle_mic(self, keystr, user_data):
        self.toggle_mic(None)

    def get_current_state_icon(self):
        if self.get_current_mic_state() == "[off]":
            icon_name = 'mic-mute.png'
        else:
            icon_name = 'mic-on.png'
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), icon_name)

    def get_current_mic_state(self):
        ps = subprocess.Popen(("amixer", "get", "Capture"), stdout=subprocess.PIPE)
        output = subprocess.check_output(('egrep', '-o', '\[o.+\]', '-m', '1'), stdin=ps.stdout)
        ps.wait()
        return filter(lambda x: not re.match(r'^\s*$', x), output)


    def build_menu(self):
        menu = gtk.Menu()

        self.item_toggle = gtk.MenuItem('Toggle Microphone')
        self.item_toggle.connect('activate', self.toggle_mic)
        menu.append(self.item_toggle)

        item_quit1 = gtk.MenuItem('Quit')
        item_quit1.connect('activate', self.quit1)
        menu.append(item_quit1)

        menu.show_all()
        return menu

    def update_mic_state(self):
        self.update_menu_toggle_label()
        self.indicator.set_icon(self.get_current_state_icon())

    def update_menu_toggle_label(self):
        if self.get_current_mic_state() == "[off]":
            self.item_toggle.set_label("Turn Microphone On")
        else:
            self.item_toggle.set_label("Turn Microphone Off")

    def toggle_mic(self, _):
        subprocess.call('amixer set Capture toggle', shell=True)
        self.update_mic_state()
        

    def quit1(self, _):
        notify.uninit()
        gtk.main_quit()

if __name__ == "__main__":
    Indicator()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gtk.main()

