import uuid
import math


class EntityMemory:
    def __init__(self, dist_threshold=80):
        self.entities = {}
        self.dist_threshold = dist_threshold

    def _distance(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def update(self, detections):
        events = []
        updated = {}

        for det in detections:
            cx, cy = det["center"]
            matched_id = None

            for eid, ent in self.entities.items():
                if self._distance((cx, cy), ent["center"]) < self.dist_threshold:
                    matched_id = eid
                    break

            if matched_id:
                updated[matched_id] = det
            else:
                eid = str(uuid.uuid4())[:8]
                updated[eid] = det
                events.append(("entity_appeared", eid, det))

        disappeared = set(self.entities.keys()) - set(updated.keys())
        for eid in disappeared:
            events.append(("entity_disappeared", eid, self.entities[eid]))

        self.entities = updated
        return events
