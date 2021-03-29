import argparse
import numpy as np
from cv2 import cv2
from os import path


class MaskPainter():
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.image_copy = self.image.copy()

        self.mask = np.zeros(self.image.shape)
        self.mask_copy = self.mask.copy()
        self.size = 4
        self.to_draw = False

        self.window_name = "Draw mask. s:save; r:reset; q:quit"

    def _paint_mask_handler(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.to_draw = True

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.to_draw:
                cv2.circle(self.image, (x, y), 7,
                           (0, 0, 255), -1)
                cv2.circle(self.mask, (x, y), 7,
                           (255, 255, 255), -1)
                cv2.imshow(self.window_name, self.image)

        elif event == cv2.EVENT_LBUTTONUP:
            self.to_draw = False

    def paint_mask(self):
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name,
                             self._paint_mask_handler)

        while True:
            cv2.imshow(self.window_name, self.image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):
                self.image = self.image_copy.copy()
                self.mask = self.mask_copy.copy()

            elif key == ord("s"):
                break

            elif key == ord("q"):
                cv2.destroyAllWindows()
                exit()

        roi = self.mask
        cv2.imshow("Press any key to save the mask", roi)
        cv2.waitKey(0)
        maskPath = path.join(path.dirname(self.image_path),
                             'mask.png')
        cv2.imwrite(maskPath, self.mask)

        # close all open windows
        cv2.destroyAllWindows()
        return maskPath
