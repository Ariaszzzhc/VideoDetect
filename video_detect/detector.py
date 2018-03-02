import tensorflow as tf
import numpy as np

from .data_type import Object, ObjectList, Position


class Detector:
    def __init__(self, ckpt_path):

        # 获取当前默认Graph
        self.__graph = tf.get_default_graph()

        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(ckpt_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)

            # 将数据引入到当前默认Graph
            tf.import_graph_def(od_graph_def, name='')

            self.image_tensor = self.__graph.get_tensor_by_name('image_tensor:0')
            self.detection_boxes = self.__graph.get_tensor_by_name('detection_boxes:0')
            self.detection_scores = self.__graph.get_tensor_by_name('detection_scores:0')
            self.detection_classes = self.__graph.get_tensor_by_name('detection_classes:0')
            self.num_detections = self.__graph.get_tensor_by_name('num_detections:0')

        self.__sess = tf.Session(graph=self.__graph)
        self.__min_score_thresh = .5
        self.__max_obj = 20
        self.__label = ['N/A', '']

    def __del__(self):
        self.__sess.close()
        pass

    def detect_per_frame(self, frame):
        objs_per_frame = []

        frame_np_expanded = np.expand_dims(frame, axis=0)
        (boxes, scores, classes, num) = self.__sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: frame_np_expanded}
        )

        # 删除单维条目
        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes).astype(np.int32)

        # 获取物体
        if not self.__max_obj:
            self.__max_obj = boxes.shape[0]

            for i in range(min(self.__max_obj, boxes.shape[0])):
                if scores is None or scores[i] > self.__min_score_thresh:
                    x, y, w, h = self.cvt_box_data(boxes[i])
                    pos = Position(x, y, w, h)

                    objs_per_frame.append(Object(name=classes[i], position=pos))

        pass

    @staticmethod
    def cvt_box_data(box: tuple):
        return box[0], box[2], (box[1] - box[0]), (box[3] - box[2])

    @staticmethod
    def cvt_central_box_data(box: tuple):
        return box[0] - box[2] / 2, box[1] - box[3] / 2, box[2], box[3]