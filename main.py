import sys
from PyQt5 import QtWidgets, QtCore
from avatar_window import AvatarWindow
from lip_detector import LipDetector
from config import THRESHOLDS, CAMERA_INDEX, UPDATE_INTERVAL_MS

def get_mouth_index(lip_open):
    if lip_open < THRESHOLDS[0]:
        return 0
    elif lip_open < THRESHOLDS[1]:
        return 1
    elif lip_open < THRESHOLDS[2]:
        return 2
    else:
        return 3

class Controller(QtCore.QObject):
    def __init__(self, avatar, detector):
        super().__init__()
        self.avatar = avatar
        self.detector = detector
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_avatar)
        self.timer.start(UPDATE_INTERVAL_MS)

    def update_avatar(self):
        lip_open = self.detector.get_lip_open_ratio()
        if lip_open is not None:
            idx = get_mouth_index(lip_open)
            self.avatar.update_expression(idx)

def main():
    app = QtWidgets.QApplication(sys.argv)
    avatar = AvatarWindow()
    detector = LipDetector(CAMERA_INDEX)
    controller = Controller(avatar, detector)
    avatar.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
