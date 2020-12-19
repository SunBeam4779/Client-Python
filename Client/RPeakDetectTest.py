from ecgdetectors import Detectors
import numpy as np

fs = 250
detector = Detectors(fs)
data = np.loadtxt("D:\\My Documents\\ECG Detector Project\\data\\ECG\\Filtered\\data999_Channel1_dec.txt")
r_peak = detector.christov_detector(data)
print(r_peak)