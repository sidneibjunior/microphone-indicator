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

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify
from gi.repository import Keybinder
from threading import Timer
from gi.repository import GdkPixbuf


APPINDICATOR_ID = 'micmuteindicator'
keystr = "<Ctrl><Alt><Shift>M"

class Indicator():
    

    def __init__(self):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, self.get_current_state_icon(), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.update_mic_state()
        Notify.init(APPINDICATOR_ID)

        Keybinder.init()
        Keybinder.set_use_cooked_accelerators(False)
        Keybinder.bind(keystr, self.callback_toggle_mic, "keystring %s (user data)" % keystr)
        print ("Press '" + keystr + "' to toggle microphone mute")

    # callback function for the about_action's "activate" signal
    def show_about_dialog(self, _):
        aboutdialog = Gtk.AboutDialog()

        authors = ["Sidnei Bernardo Junior"]
        documenters = ["Sidnei Bernardo Junior"]

        aboutdialog.set_program_name("Microphone AppIndicator for Ubuntu")
        aboutdialog.set_comments("AppIndicator to mute and show microphone mute status.")
        aboutdialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(self.get_resource("icon.svg")))
        aboutdialog.set_authors(authors)
        aboutdialog.set_documenters(documenters)
        aboutdialog.set_website("https://github.com/sidneibjunior/microphone-indicator")
        aboutdialog.set_website_label("Source code at GitHub")

        aboutdialog.show()


    def callback_toggle_mic(self, keystr, user_data):
        self.toggle_mic(None)


    def get_resource(self, resource_name):
        return os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources'), resource_name)
    

    def get_current_state_icon(self):
        if self.get_current_mic_state() == "[off]":
            icon_name = 'mute.svg'
        else:
            icon_name = 'on.svg'
        return self.get_resource(icon_name)

    def get_current_mic_state(self):
        ps = subprocess.Popen(("amixer", "get", "Capture"), stdout=subprocess.PIPE)
        output = subprocess.check_output(('egrep', '-o', '\[o.+\]', '-m', '1'), stdin=ps.stdout)
        ps.wait()
        return filter(lambda x: not re.match(r'^\s*$', x), output)


    def build_menu(self):
        menu = Gtk.Menu()

        self.item_toggle = Gtk.MenuItem('Toggle Microphone')
        self.item_toggle.connect('activate', self.toggle_mic)
        menu.append(self.item_toggle)

        self.item_about = Gtk.MenuItem('About')
        self.item_about.connect('activate', self.show_about_dialog)
        menu.append(self.item_about)

        item_quit1 = Gtk.MenuItem('Quit')
        item_quit1.connect('activate', self.quit1)
        menu.append(item_quit1)

        menu.show_all()
        return menu

    def update_mic_state(self):
        self.update_menu_toggle_label()
        self.indicator.set_icon(self.get_current_state_icon())

    def update_menu_toggle_label(self):
        if self.get_current_mic_state() == "[off]":
            self.item_toggle.set_label("Turn Microphone On ( " + keystr + " )")
        else:
            self.item_toggle.set_label("Turn Microphone Off ( " + keystr + " )")

    def toggle_mic(self, _):
        subprocess.call('amixer set Capture toggle', shell=True)
        self.update_mic_state()

        self.show_toggle_notification()
        
    def show_toggle_notification(self):
        self.notification = Notify.Notification.new("Notify")
        title = ""
        if self.get_current_mic_state() == "[off]":
            title = "Microphone Muted"
        else:
            title = "Microphone is On"
        
        self.notification.update(title)
        self.notification.show()

        # creates a timer to close the notification as the 'set_timeout' Notify method is ignored by the server.
        t = Timer(1.0, self.close_toggle_notification) 
        t.start()
    
    def close_toggle_notification(self):
        self.notification.close()

    def quit1(self, _):
        Notify.uninit()
        Gtk.main_quit()

if __name__ == "__main__":
    Indicator()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()



