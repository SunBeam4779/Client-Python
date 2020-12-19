import time

from Client.Util import Caller, TimeSwitcher, BCCCRC, Encoding
from datetime import datetime
import struct
import numpy as np

"""
this script is just for socket communication testing.
"""


address = "192.168.1.102"
port = 5561

"""
request time check
"""

# now = datetime.now()
# print(now)
# Col = TimeSwitcher.datetime_to_ColeDatetime(now)
# print("%13f", Col)
# value = float('%.12f' % Col)
# print(value)
# another = TimeSwitcher.ColeDatetime_to_datetime(Col)
# print(another)
#
# message = 0x2233
# ecc = 1
# length = struct.calcsize("idhh")
# print(length)
# print(struct.pack("!d", Col))
# head = struct.pack("<id4h", message, Col, 0, 0, length, ecc)  # Those two 0s are placeholder token
# print(head)


"""
user information transmission

NOTE: when transmitting the user information, the header and body should use the identical socket
"""

# message = 0x4411
# length = struct.calcsize("idhh")
# userid = 1118
# name = "诸葛亮"
# gender = 1
# height = "185"
# weight = "85"
# enter_time = TimeSwitcher.datetime_to_ColeDatetime(datetime.now())
# birth = enter_time
# id_card = "123"
# phone_home = "456"
# cellphone = "789"
# home = "111"
# health = "dead"
#
# size = struct.calcsize("<ii40s20s20s40s40s40s200s400sd2hd2h")
# print(size)
# print(name)
# userinfo = struct.pack("<ii40s20s20s40s40s40s200s400sd2hd2h",
#                        userid,
#                        gender,
#                        bytearray(name, encoding='utf-16'),
#                        bytearray(height, encoding='utf-16'),
#                        bytearray(weight, encoding='utf-16'),
#                        bytearray(id_card, encoding='utf-16'),
#                        bytearray(phone_home, encoding='utf-16'),
#                        bytearray(cellphone, encoding='utf-16'),
#                        bytearray(home, encoding='utf-16'),
#                        bytearray(health, encoding='utf-16'),
#                        enter_time, 0, 0,
#                        birth, 0, 0)
# print(userinfo)
#
# ecc = BCCCRC.calc(userinfo)
#
# print(ecc)
#
# head = struct.pack("<id4h", message, enter_time, 0, 0, length, ecc)

print(str(time.strftime("%Y%m%d%H%M%S", time.localtime())))
data = np.loadtxt("D:\\My Documents\\ECG Detector Project\\data\\ECG\\Filtered\\data999_Channel1_dec.txt")
temp = data.reshape(1, len(data))
signal = temp.tolist()
# print(type(signal))
signal1 = list.copy(signal[0][:4096])
signal2 = [0.0 for _ in range(4096)]
signal3 = [0.0 for _ in range(4096)]

userid = 1118
message = Encoding.encode('diagnosis')  # data
length = struct.calcsize("idhh")
time_now = TimeSwitcher.datetime_to_ColeDatetime(datetime.now())

phy = struct.pack("<i2iiii%sf%sf%sffffd2h" % (len(signal1), len(signal2), len(signal3)),
                  userid,
                  *[0, 0],
                  0,
                  0,
                  0,
                  *signal1,
                  *signal2,
                  *signal3,
                  0.0,
                  0.0,
                  0.0,
                  time_now, 0, 0)
ecc = BCCCRC.calc(phy)
print(ecc)
# print(int.from_bytes(ecc, byteorder='little'))

head = struct.pack("<id4h", message, time_now, 0, 0, length, ecc)

caller1 = Caller(address, port)
caller1.setter(head, "")  # phy
caller1.client_send()
receive, info = caller1.getter()
print(receive)
print(info)
first, second, third, fourth, fifth, six = struct.unpack("<id4h", receive)

diagnosis = struct.unpack("=%ds" % len(info), info)
print(type(diagnosis))
string = str(diagnosis[0], encoding="gbk")
print(first)
print(second)
print(diagnosis)
print(string)
