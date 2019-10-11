#!/usr/bin/env python
import sys
import traceback

import dbus
import dbus.mainloop.glib
import gi.repository.GLib

#def catchall_hello_signals_handler(hello_string):
#    print("Received a hello signal and it says " + hello_string)
    
def catchall_testservice_interface_handler(*arg, **kw):
    dbus_message = kw.pop("dbus_message")
    print("no.innovationgarage.elcheapoais.%s(%s, %s)" % (dbus_message.get_member(), arg, kw))

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()

    #bus.add_signal_receiver(catchall_hello_signals_handler, dbus_interface = "com.example.TestService", signal_name = "HelloSignal")

    bus.add_signal_receiver(catchall_testservice_interface_handler, dbus_interface = "no.innovationgarage.elcheapoais", message_keyword='dbus_message')

    loop = gi.repository.GLib.MainLoop()
    loop.run()
    
