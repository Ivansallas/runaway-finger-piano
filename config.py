from dataclasses import dataclass
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent


@dataclass
class Config:
    SAMPLE_RATE: int = 44100
    DURATION: float = 1.5
    VOLUME: float = 0.35
    COOLDOWN_SEC: float = 0.25
    DEMO_AUTOPLAY_SEC: float = 0.45

    CAM_WIDTH: int = 1280
    CAM_HEIGHT: int = 720

    MODEL_PATH: str = str(PROJECT_DIR / "hand_landmarker.task")
    MODEL_URL: str = (
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    )
    WINDOW_TITLE: str = "Music - Finger Piano (HUD Edition)"

    NOTE_FREQS = {
        "C4": 261.63,
        "D4": 293.66,
        "E4": 329.63,
        "F4": 349.23,
        "G4": 392.00,
        "A4": 440.00,
        "B4": 493.88,
        "C5": 523.25,
        "D5": 587.33,
        "E5": 659.25,
        "F5": 698.46,
        "G5": 783.99,
        "G#5": 830.61,
        "A5": 880.00,
        "C#5": 554.37,
        "D#5": 622.25,
        "C#6": 1109.07,
        "D#6": 1244.51,
        "E6": 1318.51,
    }

    BASE_FINGER_NOTES = {
        "THUMB": "E5",
        "INDEX": "A5",
        "MIDDLE": "C#6",
        "RING": "D#6",
        "PINKY": "E6",
    }

    RUNAWAY_SEQUENCE = [
        "E6",
        "E6",
        "E6",
        "E6",
        "E6",
        "E6",
        "E6",
        "E6",
        "E6",
        "E6",
        "E6",
        "E6",
        "E6",
        "E6",
        "E6",
        "E5",
        "D#6",
        "D#6",
        "D#6",
        "D#5",
        "C#6",
        "C#6",
        "C#6",
        "C#5",
        "A5",
        "A5",
        "G#5",
    ]

    MUSIC_LIBRARY = [
        {
            "id": "runaway",
            "name": "Runaway - Kanye West",
            "sequence": RUNAWAY_SEQUENCE,
        },
        {
            "id": "pulse",
            "name": "Pulse Drive",
            "sequence": [
                "E6",
                "D#6",
                "C#6",
                "A5",
                "G#5",
                "A5",
                "C#6",
                "D#6",
                "E6",
                "D#6",
                "C#6",
                "A5",
            ],
        },
        {
            "id": "echo",
            "name": "Echo Lights",
            "sequence": [
                "E6",
                "E5",
                "D#6",
                "D#5",
                "C#6",
                "C#5",
                "A5",
                "G#5",
                "A5",
                "C#6",
            ],
        },
        # ===== Domínio Público =====
        {
            "id": "ode_to_joy",
            "name": "Ode to Joy",
            "sequence": [
                "E5",
                "E5",
                "A5",
                "C#6",
                "C#6",
                "A5",
                "E5",
                "D#5",
                "C#5",
                "C#5",
                "D#5",
                "E5",
            ],
        },
        {
            "id": "amazing_grace",
            "name": "Amazing Grace",
            "sequence": [
                "A5",
                "C#6",
                "E6",
                "C#6",
                "A5",
                "G#5",
                "A5",
                "C#6",
                "E6",
                "D#6",
                "C#6",
                "A5",
            ],
        },
        {
            "id": "greensleeves",
            "name": "Greensleeves",
            "sequence": [
                "E6",
                "D#6",
                "C#6",
                "A5",
                "C#6",
                "D#6",
                "E6",
                "D#6",
                "C#6",
                "A5",
                "G#5",
                "A5",
            ],
        },
        {
            "id": "scarborough",
            "name": "Scarborough Fair",
            "sequence": [
                "A5",
                "C#6",
                "D#6",
                "E6",
                "D#6",
                "C#6",
                "A5",
                "G#5",
                "A5",
                "C#6",
                "A5",
                "E5",
            ],
        },
        {
            "id": "frere_jacques",
            "name": "Frère Jacques",
            "sequence": [
                "A5",
                "C#6",
                "D#6",
                "A5",
                "A5",
                "C#6",
                "D#6",
                "A5",
                "D#6",
                "E6",
                "C#6",
                "A5",
            ],
        },
        {
            "id": "twinkle",
            "name": "Twinkle Twinkle Little Star",
            "sequence": [
                "A5",
                "A5",
                "E6",
                "E6",
                "C#6",
                "C#6",
                "A5",
                "G#5",
                "G#5",
                "C#6",
                "C#6",
                "A5",
            ],
        },
    ]
    ACCENT_GOLD = (50, 180, 255)
    NOTE_COLORS = {
        "THUMB": (80, 80, 255),
        "INDEX": (80, 180, 255),
        "MIDDLE": (80, 220, 180),
        "RING": (220, 180, 80),
        "PINKY": (220, 100, 180),
    }

    FINGER_TIPS = [4, 8, 12, 16, 20]
    FINGER_PIPS = [3, 6, 10, 14, 18]
    FINGER_KEYS = ["THUMB", "INDEX", "MIDDLE", "RING", "PINKY"]
    DEMO_KEY_BINDINGS = {
        "1": "THUMB",
        "2": "INDEX",
        "3": "MIDDLE",
        "4": "RING",
        "5": "PINKY",
    }
    DEMO_AUTOPLAY_TOGGLE_KEY = "a"
    NEXT_SONG_KEY = "n"
    PREV_SONG_KEY = "b"

    THUMB_BY_TARGET_NOTE = {
        "E6": "E5",
        "E5": "E5",
        "D#6": "D#5",
        "D#5": "D#5",
        "C#6": "C#5",
        "C#5": "C#5",
        "A5": "G#5",
        "G#5": "G#5",
    }

    DEFAULT_SONG_ID = "runaway"

    @classmethod
    def get_song_index_by_id(cls, song_id: str) -> int:
        for idx, song in enumerate(cls.MUSIC_LIBRARY):
            if song["id"] == song_id:
                return idx
        return 0

    @classmethod
    def get_sequence(cls, song_idx: int = 0) -> list[str]:
        if not cls.MUSIC_LIBRARY:
            return cls.RUNAWAY_SEQUENCE
        safe_idx = song_idx % len(cls.MUSIC_LIBRARY)
        return cls.MUSIC_LIBRARY[safe_idx]["sequence"]

    @classmethod
    def get_thumb_note(cls, seq_idx: int, sequence: list[str] | None = None) -> str:
        active_sequence = sequence or cls.RUNAWAY_SEQUENCE
        if not active_sequence:
            return cls.BASE_FINGER_NOTES["THUMB"]
        target_note = active_sequence[seq_idx % len(active_sequence)]
        return cls.THUMB_BY_TARGET_NOTE.get(target_note, cls.BASE_FINGER_NOTES["THUMB"])

    @classmethod
    def get_finger_notes(
        cls, seq_idx: int, sequence: list[str] | None = None
    ) -> dict[str, str]:
        finger_notes = dict(cls.BASE_FINGER_NOTES)
        finger_notes["THUMB"] = cls.get_thumb_note(seq_idx, sequence)
        return finger_notes

    @classmethod
    def get_demo_finger(cls, key_char: str) -> str | None:
        return cls.DEMO_KEY_BINDINGS.get(key_char)
