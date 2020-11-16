from bluepy import btle
from binascii import b2a_hex


class MyDelegate(btle.DefaultDelegate):

    """
    handle the notification from the BLE device
    """

    def __init__(self, param):
        btle.DefaultDelegate.__init__(self)
        self.signal = param

    def handleNotification(self, cHandle, data):
        """
        sending the data as a signal to the data acquiring window
        :param cHandle: ignore it
        :param data: the notification
        :return: none
        """
        msg = str(b2a_hex(data))
        self.signal.emit(msg)
        # print("Received data: %s" % msg)
