import cv2 as cv
import numpy as np

from video_detect.common.detector import Detector

PATH_TO_CKPT = ''
PATH_TO_VIDEO = ''


def main():
    detector = Detector(PATH_TO_CKPT)

    cap = cv.VideoCapture(PATH_TO_VIDEO)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 色域转换
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        detector.detect_per_frame(frame)
    pass


if __name__ == '__main__':
    main()
