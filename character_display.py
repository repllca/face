import cv2 as cv
import numpy as np
import os
from config import CHAR_DIR

class CharacterDisplay:
    def __init__(self):
        self.mouth_images = [
            cv.imread(os.path.join(CHAR_DIR, f"mouth_{i}.png"), cv.IMREAD_UNCHANGED)
            for i in range(4)
        ]

    def overlay_image(self, bg, fg, x=0, y=0):
        """透過PNGを合成"""
        h, w = fg.shape[:2]
        alpha = fg[:, :, 3] / 255.0
        for c in range(3):
            bg[y:y+h, x:x+w, c] = (
                alpha * fg[:, :, c] + (1 - alpha) * bg[y:y+h, x:x+w, c]
            )
        return bg

    def draw_character(self, frame, idx):
        """キャラクター画像を背景なしで表示"""
        h, w, _ = frame.shape
        char_img = self.mouth_images[idx]
        if char_img is None:
            return np.zeros((h, w, 3), dtype=np.uint8)

        resized = cv.resize(char_img, (w, h))
        transparent_bg = np.zeros_like(frame)
        result = self.overlay_image(transparent_bg, resized)
        return result
