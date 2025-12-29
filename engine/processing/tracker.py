import math
import uuid


class ObjectTracker:
    def __init__(self, distance_threshold=60):
        self.tracks = {}
        self.distance_threshold = distance_threshold

    def _distance(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def update(self, detections):
        updated_tracks = {}
        events = []

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            matched = None
            for tid, track in self.tracks.items():
                if self._distance((cx, cy), track["center"]) < self.distance_threshold:
                    matched = tid
                    break

            if matched:
                updated_tracks[matched] = {
                    "center": (cx, cy),
                    "label": det["label"]
                }
            else:
                tid = str(uuid.uuid4())[:8]
                updated_tracks[tid] = {
                    "center": (cx, cy),
                    "label": det["label"]
                }
                events.append(("entered", det["label"], tid))

        exited = set(self.tracks.keys()) - set(updated_tracks.keys())
        for tid in exited:
            events.append(("exited", self.tracks[tid]["label"], tid))

        self.tracks = updated_tracks
        return events
