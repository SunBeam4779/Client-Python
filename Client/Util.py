# from bluepy import btle
import re
from binascii import b2a_hex


# class MyDelegate(btle.DefaultDelegate):
#
#     """
#     handle the notification from the BLE device
#     """
#
#     def __init__(self, signal):
#         btle.DefaultDelegate.__init__(self)
#         self.signal = signal
#         self.count = 0
#
#     def handleNotification(self, cHandle, data):
#         """
#         sending the data as a signal to the data acquiring window
#         :param cHandle: ignore it
#         :param data: the notification
#         :return: none
#         """
#         if self.count < 3:
#             self.count += 1
#             pass
#         else:
#             msg = str(b2a_hex(data))[2:-1]
#             # self.q.put(msg)
#             self.signal.emit(msg)
#             # if self.q.qsize() > 6:
#             #     res = [self.q.get(), self.q.get(), self.q.get()]
#             #     self.signal[str, str, str].emit(res[0], res[1], res[2])
#         # print("Received data:")


class Splitter:

    """
    handle the BLE string-type data splitting.
    """

    ori1 = []
    ori2 = []
    res1 = []
    res2 = []

    @staticmethod
    def process_string(message):

        """
        process the string of BLE data, to get the essential message.
        :param message:
        :return: none
        """

        # count = 0
        # data = ""
        # length = 6
        target = 72
        # head = 0
        # items = ""

        # for i in range(length):
        # message = messages.get()
        # count += 1
        # cut_head = message.split(":")[-1]
        # lower = cut_head.lower()
        # essence = lower.split("\"")[1]
        # string = "".join(essence)
        # data += string
        data1 = re.split("c0c0", message)
        item = "".join(data1[1:-1])
        if len(data1[0]) == len(data1[-1]) == 10:
            data1[0] = data1[0][2:]
            data1[-1] = data1[-1][:-2]
            item1 = data1[0] + item
            item = item1 + data1[-1]
            target = 80
        # data = item.split(" ")
        # data = "".join(data)
        # data = data.split(" ")
        # data = "".join(data)
        if len(item) == target:
            Splitter.ori1, Splitter.ori2, Splitter.res1, Splitter.res2 = Splitter.switch_form(item)
            # print(Splitter.res2[0])
            # return ori1, ori2, ans1, ans2
            # data = ""

    @staticmethod
    def two_complement(value, bits):

        """
        handle the two's complement data
        :param value:
        :param bits:
        :return: processed result
        """

        if value >= 2 ** bits:
            raise ValueError("Value: {} out of range of {}-bit value.".format(value, bits))
        else:
            return value - int((value << 1) & 2 ** bits)

    @staticmethod
    def get_dec(channel1, channel2):

        """
        switch from hex to dec
        :param channel1:
        :param channel2:
        :return: decimal result
        """

        res = int(channel1, 16)
        bits_width = 24
        r_e1 = Splitter.two_complement(res, bits_width)

        res = int(channel2, 16)
        bits_width = 24
        r_e2 = Splitter.two_complement(res, bits_width)
        return r_e1, r_e2

    @staticmethod
    def switch_form(string):

        """
        get the original data and final result of two channels
        :param string:
        :return: processed result
        """

        original_channel1 = []
        original_channel2 = []
        final1 = []
        final2 = []
        length = len(string)
        i = 0
        while i < length:
            result1 = '0x'
            result1 = result1 + ''.join(string[i])
            result1 = result1 + ''.join(string[i + 1])
            result1 = result1 + ''.join(string[i + 2])
            result1 = result1 + ''.join(string[i + 3])
            result1 = result1 + ''.join("00")

            result2 = '0x'
            result2 = result2 + ''.join(string[i + 4])
            result2 = result2 + ''.join(string[i + 5])
            result2 = result2 + ''.join(string[i + 6])
            result2 = result2 + ''.join(string[i + 7])
            result2 = result2 + ''.join("00")

            i += 8

            original_channel1.append(result1)
            original_channel2.append(result2)
            value1, value2 = Splitter.get_dec(result1, result2)
            final1.append(value1)
            final2.append(value2)
            # self.result1.put(value1)
            # self.result2.put(value2)
            # print(result1)
            # print(result2)
        return original_channel1, original_channel2, final1, final2
