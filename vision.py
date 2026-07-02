import os
import urllib.request

import cv2
import numpy as np

from config import Config


def load_mediapipe():
    try:
        import mediapipe as mp
        from mediapipe.tasks.python.core.base_options import BaseOptions
        from mediapipe.tasks.python.vision import (
            HandLandmarker,
            HandLandmarkerOptions,
            RunningMode,
        )
    except ImportError as exc:
        raise RuntimeError("MediaPipe nao esta disponivel no ambiente atual.") from exc

    return mp, BaseOptions, HandLandmarker, HandLandmarkerOptions, RunningMode


class ModelDownloader:
    @staticmethod
    def ensure_model_exists():
        if os.path.exists(Config.MODEL_PATH) and os.path.getsize(Config.MODEL_PATH) > 10_000:
            return
        print("📥 Baixando modelo MediaPipe Hand Landmarker (~8 MB)...")
        try:
            os.makedirs(os.path.dirname(Config.MODEL_PATH), exist_ok=True)
            urllib.request.urlretrieve(Config.MODEL_URL, Config.MODEL_PATH)
            print("✅ Modelo baixado com sucesso!")
        except Exception as e:
            raise RuntimeError(f"Falha ao baixar o modelo do MediaPipe: {e}") from e


class HandTracker:
    def __init__(self):
        _, BaseOptions, HandLandmarker, HandLandmarkerOptions, RunningMode = (
            load_mediapipe()
        )
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=Config.MODEL_PATH),
            running_mode=RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.6,
            min_hand_presence_confidence=0.6,
            min_tracking_confidence=0.5,
        )
        try:
            self.detector = HandLandmarker.create_from_options(options)
        except Exception as exc:
            raise RuntimeError("Falha ao inicializar o rastreador de mao.") from exc
        self.frame_ts = 0

    def process_frame(self, frame: np.ndarray):
        mp, _, _, _, _ = load_mediapipe()
        self.frame_ts += 33
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
        )
        return self.detector.detect_for_video(mp_image, self.frame_ts)

    @staticmethod
    def _adaptive_margin(landmarks, anchor_idx: int) -> float:
        wrist = landmarks[0]
        anchor = landmarks[anchor_idx]
        scale = max(abs(anchor.y - wrist.y), abs(anchor.x - wrist.x))
        return max(0.015, scale * 0.12)

    @staticmethod
    def is_finger_pressed(landmarks, finger_idx: int, handedness: str) -> bool:
        tip = landmarks[Config.FINGER_TIPS[finger_idx]]
        pip = landmarks[Config.FINGER_PIPS[finger_idx]]
        margin = HandTracker._adaptive_margin(landmarks, Config.FINGER_PIPS[finger_idx])

        if finger_idx == 0:
            if handedness == "Right":
                return tip.x < pip.x - margin
            return tip.x > pip.x + margin

        return tip.y > pip.y - margin

    def close(self):
        if hasattr(self, "detector") and self.detector is not None:
            self.detector.close()
