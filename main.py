import argparse
import cv2
import time
import numpy as np

# Importações dos seus novos módulos locais
from config import Config
from ui import UIRenderer


def load_audio_engine():
    from audio import AudioEngine

    return AudioEngine


def load_vision_modules():
    from vision import HandTracker, ModelDownloader

    return ModelDownloader, HandTracker


class FingerPianoApp:

    def __init__(
        self,
        demo_mode: bool = False,
        autoplay_demo: bool = False,
        camera_index: int = 0,
    ):
        self.audio_engine = None
        self.hand_tracker = None
        self.cap = None
        self.demo_mode = demo_mode
        self.autoplay_demo = demo_mode and autoplay_demo
        self.camera_index = camera_index

        if not self.demo_mode:
            AudioEngine = load_audio_engine()
            self.audio_engine = AudioEngine()

        if not self.demo_mode:
            ModelDownloader, HandTracker = load_vision_modules()
            ModelDownloader.ensure_model_exists()
            self.hand_tracker = HandTracker()
            self.cap = cv2.VideoCapture(self.camera_index)

            if not self.cap.isOpened():
                raise RuntimeError(
                    f"Câmera não encontrada no índice {self.camera_index}!"
                )

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAM_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAM_HEIGHT)

        self.prev_pressed = {k: False for k in Config.FINGER_KEYS}
        self.cooldowns = {k: 0.0 for k in Config.FINGER_KEYS}
        self.demo_flash_until = {k: 0.0 for k in Config.FINGER_KEYS}
        self.seq_idx = 0
        self.next_autoplay_at = 0.0
        self.wave_buf = [0.0] * 360

    @staticmethod
    def startup_error_message(error: Exception) -> str:
        error_message = str(error)
        lowered_message = error_message.lower()

        if "áudio" in lowered_message or "audio" in lowered_message:
            return (
                f"{error_message}\n\n"
                "Verifique se há um dispositivo de saída ativo e se o volume do sistema está habilitado."
            )

        if "câmera" in lowered_message or "camera" in lowered_message:
            return (
                f"{error_message}\n\n"
                "Feche outros aplicativos que possam estar usando a webcam e tente novamente."
            )

        if "mediapipe" in lowered_message or "modelo" in lowered_message:
            return (
                f"{error_message}\n\n"
                "Confira se há acesso à internet no primeiro uso e se o download do modelo não foi bloqueado."
            )

        return error_message

    def get_current_finger_notes(self):
        return Config.get_finger_notes(self.seq_idx)

    def create_demo_frame(self):
        frame = np.zeros((Config.CAM_HEIGHT, Config.CAM_WIDTH, 3), dtype=np.uint8)
        gradient = np.linspace(15, 55, Config.CAM_WIDTH, dtype=np.uint8)
        frame[:, :, 0] = gradient
        frame[:, :, 1] = gradient // 2
        frame[:, :, 2] = 20
        return frame

    def trigger_note(self, finger: str, finger_notes: dict[str, str], now: float):
        note = finger_notes[finger]
        if self.audio_engine is not None:
            self.audio_engine.play_note(note)

        self.cooldowns[finger] = now + Config.COOLDOWN_SEC
        self.demo_flash_until[finger] = now + Config.COOLDOWN_SEC

        freq = Config.NOTE_FREQS[note]
        self.wave_buf.extend(
            [np.sin(2 * np.pi * freq * t / Config.SAMPLE_RATE) for t in range(40)]
        )

        target_note = Config.RUNAWAY_SEQUENCE[
            self.seq_idx % len(Config.RUNAWAY_SEQUENCE)
        ]
        if note == target_note:
            self.seq_idx += 1

    def apply_demo_input(
        self, pressed_key: int, finger_notes: dict[str, str], now: float
    ):
        key_char = chr(pressed_key) if 0 <= pressed_key <= 255 else ""
        finger = Config.get_demo_finger(key_char)
        if finger is None or now <= self.cooldowns[finger]:
            return None

        self.trigger_note(finger, finger_notes, now)
        return finger

    def get_target_finger(self, finger_notes: dict[str, str]) -> str | None:
        target_note = Config.RUNAWAY_SEQUENCE[
            self.seq_idx % len(Config.RUNAWAY_SEQUENCE)
        ]
        for finger, note in finger_notes.items():
            if note == target_note:
                return finger
        return None

    def apply_demo_autoplay(self, finger_notes: dict[str, str], now: float):
        if not self.autoplay_demo or now < self.next_autoplay_at:
            return None

        finger = self.get_target_finger(finger_notes)
        if finger is None or now <= self.cooldowns[finger]:
            return None

        self.trigger_note(finger, finger_notes, now)
        self.next_autoplay_at = now + Config.DEMO_AUTOPLAY_SEC
        return finger

    def handle_demo_toggle(self, pressed_key: int, now: float) -> bool:
        key_char = chr(pressed_key).lower() if 0 <= pressed_key <= 255 else ""
        if key_char != Config.DEMO_AUTOPLAY_TOGGLE_KEY:
            return False

        self.autoplay_demo = not self.autoplay_demo
        self.next_autoplay_at = now if self.autoplay_demo else 0.0
        return True

    def run(self):
        print(
            "\n🎵 RUNAWAY - HUD Edition iniciada! Aperte Q na janela de vídeo para sair.\n"
        )

        cv2.namedWindow(Config.WINDOW_TITLE, cv2.WINDOW_NORMAL)

        try:
            while True:
                if self.demo_mode:
                    frame = self.create_demo_frame()
                    ret = True
                else:
                    ret, frame = self.cap.read()
                    if not ret:
                        raise RuntimeError("Falha ao capturar frame da camera.")
                    frame = cv2.flip(frame, 1)

                h, w = frame.shape[:2]
                now = time.time()
                display_frame = frame.copy()

                UIRenderer.draw_background_tint(display_frame)

                active_fingers = {k: False for k in Config.FINGER_KEYS}
                finger_notes = self.get_current_finger_notes()
                hand_detected = False
                result = None

                if self.demo_mode:
                    for finger, flash_until in self.demo_flash_until.items():
                        active_fingers[finger] = now < flash_until

                    autoplay_finger = self.apply_demo_autoplay(finger_notes, now)
                    if autoplay_finger is not None:
                        active_fingers[autoplay_finger] = True

                if self.hand_tracker is not None:
                    result = self.hand_tracker.process_frame(frame)
                    hand_detected = bool(result.hand_landmarks)

                if hand_detected:
                    for hand_idx, landmarks in enumerate(result.hand_landmarks):
                        handedness_str = (
                            result.handedness[hand_idx][0].category_name
                            if result.handedness
                            else "Right"
                        )

                        for i, finger in enumerate(Config.FINGER_KEYS):
                            is_pressed = self.hand_tracker.is_finger_pressed(
                                landmarks, i, handedness_str
                            )
                            active_fingers[finger] = is_pressed

                            if (
                                is_pressed
                                and not self.prev_pressed[finger]
                                and now > self.cooldowns[finger]
                            ):
                                self.trigger_note(finger, finger_notes, now)

                            self.prev_pressed[finger] = is_pressed

                        UIRenderer.draw_landmarks(
                            display_frame, landmarks, active_fingers, finger_notes, w, h
                        )

                self.wave_buf = self.wave_buf[-360:]
                if len(self.wave_buf) < 360:
                    self.wave_buf = [0.0] * (360 - len(self.wave_buf)) + self.wave_buf

                UIRenderer.draw_title(display_frame, w, h)
                UIRenderer.draw_tracking_status(display_frame, hand_detected, w, h)
                if self.demo_mode:
                    UIRenderer.draw_mode_banner(
                        display_frame, "MODO DEMO SEM CAMERA", w, h
                    )
                    UIRenderer.draw_demo_controls(
                        display_frame, w, h, self.autoplay_demo
                    )
                UIRenderer.draw_sequence(display_frame, self.seq_idx, w, h)
                UIRenderer.draw_waveform(display_frame, self.wave_buf, w, h)
                UIRenderer.draw_piano_keys(
                    display_frame, active_fingers, finger_notes, h, w
                )

                s = w / 1280.0
                help_text = (
                    "Teclas 1-5 simulam os dedos | A alterna autoplay | Q sai"
                    if self.demo_mode
                    else "Dobre os dedos para tocar  |  Pressione 'Q' para sair"
                )
                cv2.putText(
                    display_frame,
                    help_text,
                    (w // 2 - int(200 * s), h - int(15 * s)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5 * s,
                    (100, 100, 100),
                    max(1, int(1 * s)),
                    cv2.LINE_AA,
                )

                cv2.imshow(Config.WINDOW_TITLE, display_frame)
                pressed_key = cv2.waitKey(1) & 0xFF
                if self.demo_mode:
                    autoplay_toggled = self.handle_demo_toggle(pressed_key, now)
                    if not autoplay_toggled:
                        triggered_finger = self.apply_demo_input(
                            pressed_key, finger_notes, now
                        )
                        if triggered_finger is not None:
                            active_fingers[triggered_finger] = True
                if pressed_key in (ord("q"), 27):
                    break
        finally:
            self.cleanup()

    def cleanup(self):
        if self.hand_tracker is not None:
            self.hand_tracker.close()
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        if self.audio_engine is not None:
            self.audio_engine.quit()


def show_startup_error(message: str):
    frame = np.zeros((Config.CAM_HEIGHT, Config.CAM_WIDTH, 3), dtype=np.uint8)
    cv2.namedWindow(Config.WINDOW_TITLE, cv2.WINDOW_NORMAL)
    UIRenderer.draw_error_screen(frame, message, Config.CAM_WIDTH, Config.CAM_HEIGHT)

    while True:
        cv2.imshow(Config.WINDOW_TITLE, frame)
        pressed_key = cv2.waitKey(30) & 0xFF
        if pressed_key in (ord("q"), 27):
            break

    cv2.destroyAllWindows()


def parse_args():
    parser = argparse.ArgumentParser(description="Runaway Finger Piano")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="executa uma demo visual sem camera e sem tracking",
    )
    parser.add_argument(
        "--autoplay",
        action="store_true",
        help="no modo demo, toca a sequencia automaticamente",
    )
    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="indice da camera para abrir quando nao estiver em modo demo",
    )
    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_args()
        app = FingerPianoApp(
            demo_mode=args.demo,
            autoplay_demo=args.autoplay,
            camera_index=args.camera_index,
        )
        app.run()
    except Exception as exc:
        print(f"❌ {exc}")
        show_startup_error(FingerPianoApp.startup_error_message(exc))
