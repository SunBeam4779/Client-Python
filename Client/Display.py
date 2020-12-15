import numpy as np
import sys
from pyqtgraph import *
from pyqtgraph.Qt import QtGui, QtCore


# data = np.loadtxt("D:\\My Documents\\ECG Detector Project\\data\\ECG\\Filtered\\data332_Channel1_dec.txt")


class Display(GraphicsLayoutWidget):

    """
    handle the data displaying
    """

    def __init__(self, data_):
        super(Display, self).__init__()

        self.data = data_
        # try:
        #     self.data = np.loadtxt(path_)
        # except Exception as e:
        #     print("failed to open file: " + e.__str__())
        #     return
        self.setWindowTitle('ECG')
        self.label = LabelItem(justify='right')
        self.addItem(self.label)
        self.p1 = self.addPlot(row=1, col=0)
        self.p2 = self.addPlot(row=2, col=0)

        self.region = LinearRegionItem()
        self.region.setZValue(10)
        # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
        # item when doing auto-range calculations.
        self.p2.addItem(self.region, ignoreBounds=True)

        # pg.dbg()
        self.p1.setAutoVisible(y=True)

        # create numpy arrays
        # make the numbers large to show that the xrange shows data from 10000 to all the way 0
        self.data1 = self.data
        self.data2 = self.data

        self.p1.plot(self.data1, pen="r")
        self.p1.plot(self.data2, pen="r")

        self.p2.plot(self.data1, pen="w")

        self.region.sigRegionChanged.connect(self.update)

        self.p1.sigRangeChanged.connect(self.update_region)
        self.region.setRegion([1000, 2000])

        # cross hair
        vLine = InfiniteLine(angle=90, movable=False)
        hLine = InfiniteLine(angle=0, movable=False)
        # self.p1.addItem(vLine, ignoreBounds=True)
        # self.p1.addItem(hLine, ignoreBounds=True)

        self.vb = self.p1.vb

    def update(self):
        self.region.setZValue(1)
        min_x, max_x = self.region.getRegion()
        self.p1.setXRange(min_x, max_x, padding=0)

    def update_region(self, window, view_range):
        rgn = view_range[0]
        self.region.setRegion(rgn)

    def mouse_moved(self, evt):
        pos = evt[1]  # using signal proxy turns original arguments into a tuple
        if self.p1.sceneBoundingRect().contains(pos):
            mouse_point = self.vb.mapSceneToView(pos)
            index = int(mouse_point.x())
            if 0 < index < len(self.data1):
                self.label.setText("<span style='font-size: 12pt'>x=%0.1f,   "
                                   "<span style='color: red'>y1=%0.1f</span>,   "
                                   "<span style='color: green'>y2=%0.1f</span>" % (
                                       mouse_point.x(), self.data1[index], self.data2[index]))
            # vLine.setPos(mouse_point.x())
            # hLine.setPos(mouse_point.y())


# proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
# p1.scene().sigMouseMoved.connect(mouse_moved)

# Start Qt event loop unless running in interactive mode or using pyside.
# if __name__ == '__main__':
#     import sys
#
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         # noinspection PyUnresolvedReferences
#         QtGui.QApplication.instance().exec_()
