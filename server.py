import dbus
import dbus.service
import dbus.mainloop.glib
import gi.repository.GLib

def timeout(to):
    def wrapper(fn):
        gi.repository.GLib.timeout_add(to, fn)
    return wrapper
        
class TestObject(dbus.service.Object):
    def __init__(self, conn, object_path='/com/example/TestService/object'):
        dbus.service.Object.__init__(self, conn, object_path)
        @timeout(1000)
        def emit():
            self.HelloSignal("Hello world")
            return True
        
    @dbus.service.signal('com.example.TestService')
    def HelloSignal(self, message):
        print("Sending %s" % message)

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName('com.example.TestService', session_bus)
    test_object = TestObject(session_bus)

    loop = gi.repository.GLib.MainLoop()
    print("Running example signal emitter service.")
    loop.run()
