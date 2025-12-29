class EngineConfig:
    VIDEO_SOURCE: int | str = 0  # 0 = webcam
    MOTION_THRESHOLD: int = 5000
    CONFIDENCE_SCALE: float = 1.0
    TARGET_FPS: int = 30
