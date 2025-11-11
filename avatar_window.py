from PyQt5 import QtWidgets, QtCore, QtGui
import os
from config import CHAR_DIR

class AvatarWindow(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setScaledContents(True)

        # 画像の読み込み
        self.images = [
            QtGui.QPixmap(os.path.join(CHAR_DIR, f"mouth_{i}.png"))
            for i in range(4)
        ]
        self.current_index = 0
        self.setPixmap(self.images[self.current_index])

        # 初期サイズと位置
        self.resize(800, 500)
        self.move(100, 100)

        # ドラッグ用変数
        self.offset = None

    def update_expression(self, idx: int):
        """口の開きに応じて画像を更新"""
        if idx != self.current_index and 0 <= idx < len(self.images):
            self.current_index = idx
            self.setPixmap(self.images[idx])

    # --------------------
    # ドラッグ処理
    # --------------------
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # クリックした位置とウィンドウ左上の差分を記憶
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() & QtCore.Qt.LeftButton:
            # マウスの移動量に合わせてウィンドウ移動
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None
