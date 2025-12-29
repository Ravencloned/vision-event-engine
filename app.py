import cv2
import asyncio

from engine.core.engine import VisionEventEngine
from engine.detectors.motion_detector import MotionDetector
from engine.input.video_source import VideoSource


class DummyEventBus:
    async def publish(self, event):
        print(f"[EVENT] {event.event_type} | value={event.value:.0f} | conf={event.confidence:.2f}")


class DummyStorage:
    def save(self, event):
        pass


async def main():
    video = VideoSource()
    detector = MotionDetector()
    engine = VisionEventEngine(
        detector=detector,
        event_bus=DummyEventBus(),
        storage=DummyStorage()
    )

    while True:
        frame, fps = video.read()
        if frame is None:
            break

        await engine.run(frame)

        cv2.putText(
            frame,
            f"FPS: {fps:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Vision Event Engine", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(main())
