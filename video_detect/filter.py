from video_detect.data_type import Position, Object
import math


class Filter:
    def __init__(self):
        self.obj_filter = ObjectFilter()

    def filter(self, objs_seqs):
        self.obj_filter.filter_seq(objs_seqs)

        for objs_seq in objs_seqs:
            x_filter = KalmanFilter()
            y_filter = KalmanFilter()
            w_filter = KalmanFilter()
            h_filter = KalmanFilter()
            for i in range(len(objs_seq.data)):
                objs_seq.data[i].position.x = x_filter.filter(objs_seq.data[i].position.x)
                objs_seq.data[i].position.y = y_filter.filter(objs_seq.data[i].position.y)
                objs_seq.data[i].position.w = w_filter.filter(objs_seq.data[i].position.w)
                objs_seq.data[i].position.h = h_filter.filter(objs_seq.data[i].position.h)

        return objs_seqs


class ObjectFilter:
    @staticmethod
    def filter_seq(objs_seqs):
        for obj_seq in objs_seqs:
            for i in range(len(obj_seq.data)):
                if not obj_seq.data[i]:
                    if i >= 2:
                        pos = Position((2 * obj_seq.data[i - 1].position.x - obj_seq.data[i - 2].position.x),
                                       (2 * obj_seq.data[i - 1].position.y - obj_seq.data[i - 2].position.y),
                                       obj_seq.data[i - 1].position.w,
                                       obj_seq.data[i - 1].position.h
                                       )
                        obj_seq.data[i] = Object(obj_seq.data[i - 1].cls_id, obj_seq.data[i - 1].id, pos)
                    else:
                        obj_seq.data[i] = Object(obj_seq.data[i - 1].cls_id, obj_seq.data[i - 1].id,
                                                 obj_seq.data[i - 1].position)


class KalmanFilter:
    """
    卡尔曼滤波器
    :param Number options.R Process noise
    :param Number options.Q Measurement noise
    :param Number options.A State vector
    :param Number options.B Control vector
    :param Number options.C Measurement vector
    """

    def __init__(self, R: float = 0.02, Q: float = 1, A: float = 1, B: float = 0, C: float = 1):
        self.R = R
        self.Q = Q

        self.A = A
        self.C = C
        self.B = B
        self.cov = float('nan')
        self.x = float('nan')

    def filter(self, z: float, u: float = 0):
        if math.isnan(self.x):
            self.x = (1 / self.C) * z
            self.cov = (1 / self.C) * self.Q * (1 / self.C)
        else:
            # Compute prediction
            predX = (self.A * self.x) + (self.B * u)
            predCov = ((self.A * self.cov) * self.A) + self.R

            # Kalman gain
            K = predCov * self.C * (1 / ((self.C * predCov * self.C) + self.Q))

            # Correction
            self.x = predX + K * (z - (self.C * predX))
            self.cov = predCov - (K * self.C * predCov)

        return self.x

    def last_measurement(self):
        return self.x
