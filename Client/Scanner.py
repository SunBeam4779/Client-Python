# from bluepy import btle


class Scanner:

    """
    the BLE peripheral scanner
    """

    scanner = None
    result_of_scan = {}

    def __init__(self):
        # self.scanner = btle.Scanner()
        self.scanner = None

    def scan(self):

        """
        handle the BLE peripherals scanning and save them into the result list
        :return: none
        """

        self.scanner.scan(5.0)
        devices = self.scanner.getDevices()
        self.result_of_scan.clear()
        for dev in devices:
            name = dev.getValue(0x09)
            self.result_of_scan[name] = dev.addr
        return self.result_of_scan
