#!/usr/bin/env python
import sys
import traceback

import dbus
import dbus.mainloop.glib
import gi.repository.GLib

nm_states = {0: "NM_ACTIVE_CONNECTION_STATE_UNKNOWN",
             1: "NM_ACTIVE_CONNECTION_STATE_ACTIVATING",
             2: "NM_ACTIVE_CONNECTION_STATE_ACTIVATED",
             3: "NM_ACTIVE_CONNECTION_STATE_DEACTIVATING",
             4: "NM_ACTIVE_CONNECTION_STATE_DEACTIVATED"}

def get_ip(bus, connection):
    dhcp_path = dbus.Interface(
        bus.get_object("org.freedesktop.NetworkManager", connection),
        "org.freedesktop.DBus.Properties"
    ).Get("org.freedesktop.NetworkManager.Connection.Active", "Dhcp4Config")

    return dbus.Interface(
        bus.get_object("org.freedesktop.NetworkManager", dhcp_path),
        "org.freedesktop.DBus.Properties"
    ).Get(
        "org.freedesktop.NetworkManager.DHCP4Config", "Options"
    )["ip_address"]

def state_changed(state, reason, dbus_message):
    state = nm_states[state]
    print("%s.state_changed(%s)" % (dbus_message.get_path(), state))
    if state == "NM_ACTIVE_CONNECTION_STATE_ACTIVATED":
        print("Got new ip: %s" % get_ip(bus, dbus_message.get_path()))
    if state == "NM_ACTIVE_CONNECTION_STATE_DEACTIVATED":
        print("Lost ip: %s" % get_ip(bus, dbus_message.get_path()))
        
def interface_handler(*arg, **kw):
    dbus_message = kw.pop("dbus_message")
    print("org.freedesktop.NetworkManager.Connection.Active.%s(%s, %s)" % (dbus_message.get_member(), arg, kw))

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    bus.add_signal_receiver(state_changed, dbus_interface = "org.freedesktop.NetworkManager.Connection.Active", signal_name = "StateChanged", message_keyword='dbus_message')

    bus.add_signal_receiver(interface_handler, dbus_interface = "org.freedesktop.NetworkManager.Connection.Active", message_keyword='dbus_message')


      
    nm = dbus.Interface(bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager"), "org.freedesktop.DBus.Properties")
    connections = nm.Get("org.freedesktop.NetworkManager", "ActiveConnections")
    for connection in connections:
        print("Connected as %s" % get_ip(bus, connection))
    
    loop = gi.repository.GLib.MainLoop()
    loop.run()
    
