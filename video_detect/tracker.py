import math


class ObjectTracker:

    def __init__(self, disp_threshold=0.05):
        self.objs = []
        self.disp_threshold = disp_threshold
        self.obj_id = 1

    def track_frame(self, index, objs):
        out_seq = []
        for track_obj_seq in self.objs:
            before = len(track_obj_seq.data)
            i = -1
            for j in range(len(objs)-1, -1, -1):
                # 取该物体最后一次出现的值
                while not track_obj_seq.data[i]:
                    i -= 1
                if track_obj_seq.data[i].cls_id == objs[j].cls_id:
                    obj_center_x, obj_center_y = objs[j].position.center()
                    track_obj_center_x, track_obj_center_y = track_obj_seq.data[i].position.center()

                    disp = math.sqrt((track_obj_center_x - obj_center_x) ** 2 + (track_obj_center_y - obj_center_y) ** 2)

                    if disp < self.disp_threshold:
                        objs[j].id = track_obj_seq.data[i].id
                        track_obj_seq.data.append(objs[j])
                        objs.pop(j)
                        break

            after = len(track_obj_seq.data)

            # 判断同一物体是否出现
            if before == after:
                track_obj_seq.data.append(False)

        for obj in objs:
            obj.id = self.obj_id
            self.obj_id += 1
            self.objs.append(ObjectSeq(index, [obj]))

        for i in range(len(self.objs)-1, -1, -1):
            if not self.objs[i].data[-1] and not self.objs[i].data[-2] and not self.objs[i].data[-3]:
                del self.objs[i].data[-3:]
                out_seq.append(self.objs[i])
                self.objs.pop(i)

        return out_seq

    def finish(self):
        out_seq = self.objs

        return out_seq


class ObjectSeq:
    def __init__(self, idx, seq):
        self.idx = idx
        self.data = seq
