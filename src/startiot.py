from network import LoRa
import socket
import time
import binascii


class Startiot:
    def __init__(self):
        self.dev_eui = binascii.unhexlify("ffffffff00001373")
        self.app_eui = binascii.unhexlify("8000000000000006")
        self.app_key = binascii.unhexlify("8a64620c7bafddb59031f380f51dab1f")

    def connect(self, blocking=False, timeout=0, function=None):
        lora = LoRa(mode=LoRa.LORAWAN)
        lora.join(activation=LoRa.OTAA, auth=(
            self.dev_eui, self.app_eui, self.app_key), timeout=0)

        if timeout == 0:
            while not lora.has_joined():
                if function:
                    function()
                else:
                    time.sleep(2.5)
        else:
            for x in range(timeout):
                if lora.has_joined():
                    break
                if function:
                    function()
                else:
                    time.sleep(2.5)

        if not lora.has_joined():
            return False

        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        self.s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

        # make the socket non-blocking
        self.s.setblocking(blocking)

        return True

    def send(self, data):
        print(self.s.send(data))

    def recv(self, length):
        return self.s.recv(length)
