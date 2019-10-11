import dbus
import dbus.service
import dbus.mainloop.glib
import gi.repository.GLib
import sys

def timeout(to):
    def wrapper(fn):
        gi.repository.GLib.timeout_add(to, fn)
    return wrapper
        
class ElcheapoAIS(dbus.service.Object):
    def __init__(self, conn, object_path='/no/innovationgarage/elcheapoais/NMEA'):
        dbus.service.Object.__init__(self, conn, object_path)
        
    @dbus.service.signal('no.innovationgarage.elcheapoais')
    def NMEA(self, message):
        print("Sending %s" % message)

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    elcheapoais = ElcheapoAIS(bus)

    @timeout(0)
    def emit():
        elcheapoais.NMEA(sys.argv[1])
        sys.exit(1)
        return True
    
    loop = gi.repository.GLib.MainLoop()
    print("Running example signal emitter service.")
    loop.run()
