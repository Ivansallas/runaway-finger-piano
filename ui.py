import cv2
import numpy as np

from config import Config


def load_hand_landmarks_connections():
    from mediapipe.tasks.python.vision import HandLandmarksConnections

    return HandLandmarksConnections


class UIRenderer:

    @staticmethod
    def draw_panel(frame, x, y, w, h, border_color, alpha=0.45, border_thickness=1):
        UIRenderer.draw_alpha_rect(frame, x, y, w, h, (0, 0, 0), alpha)
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            border_color,
            border_thickness,
            cv2.LINE_AA,
        )

    @staticmethod
    def draw_text(frame, text, x, y, font, scale, color, thickness=1):
        cv2.putText(frame, text, (x, y), font, scale, color, thickness, cv2.LINE_AA)

    @staticmethod
    def wrap_text(text, max_chars):
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            candidate = " ".join(current_line + [word])
            if len(candidate) <= max_chars or not current_line:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    @staticmethod
    def draw_alpha_rect(frame, x, y, w, h, color, alpha):
        fh, fw = frame.shape[:2]
        x1, y1 = max(0, int(x)), max(0, int(y))
        x2, y2 = min(fw, int(x+w)), min(fh, int(y+h))
        if x1 >= x2 or y1 >= y2: return

        roi = frame[y1:y2, x1:x2]
        rect_overlay = np.full_like(roi, color, dtype=np.uint8)
        cv2.addWeighted(rect_overlay, alpha, roi, 1.0 - alpha, 0, roi)

    @staticmethod
    def draw_rounded_rect(frame, x, y, w, h, color, radius, thickness=-1):
        x, y, w, h = int(x), int(y), int(w), int(h)
        if w <= 0 or h <= 0:
            return

        r = max(0, min(int(radius), w // 2, h // 2))
        if r == 0:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness, cv2.LINE_AA)
            return

        if thickness < 0:
            cv2.rectangle(frame, (x + r, y), (x + w - r, y + h), color, -1)
            cv2.rectangle(frame, (x, y + r), (x + w, y + h - r), color, -1)
            cv2.circle(frame, (x + r, y + r), r, color, -1, cv2.LINE_AA)
            cv2.circle(frame, (x + w - r, y + r), r, color, -1, cv2.LINE_AA)
            cv2.circle(frame, (x + r, y + h - r), r, color, -1, cv2.LINE_AA)
            cv2.circle(frame, (x + w - r, y + h - r), r, color, -1, cv2.LINE_AA)
            return

        cv2.line(frame, (x + r, y), (x + w - r, y), color, thickness, cv2.LINE_AA)
        cv2.line(
            frame, (x + r, y + h), (x + w - r, y + h), color, thickness, cv2.LINE_AA
        )
        cv2.line(frame, (x, y + r), (x, y + h - r), color, thickness, cv2.LINE_AA)
        cv2.line(
            frame, (x + w, y + r), (x + w, y + h - r), color, thickness, cv2.LINE_AA
        )
        cv2.ellipse(
            frame, (x + r, y + r), (r, r), 180, 0, 90, color, thickness, cv2.LINE_AA
        )
        cv2.ellipse(
            frame, (x + w - r, y + r), (r, r), 270, 0, 90, color, thickness, cv2.LINE_AA
        )
        cv2.ellipse(
            frame, (x + r, y + h - r), (r, r), 90, 0, 90, color, thickness, cv2.LINE_AA
        )
        cv2.ellipse(
            frame,
            (x + w - r, y + h - r),
            (r, r),
            0,
            0,
            90,
            color,
            thickness,
            cv2.LINE_AA,
        )

    @staticmethod
    def draw_vertical_gradient_rect(frame, x, y, w, h, top_color, bottom_color):
        fh, fw = frame.shape[:2]
        x1, y1 = max(0, int(x)), max(0, int(y))
        x2, y2 = min(fw, int(x + w)), min(fh, int(y + h))
        if x1 >= x2 or y1 >= y2:
            return

        roi_h = y2 - y1
        roi_w = x2 - x1
        top = np.array(top_color, dtype=np.float32)
        bottom = np.array(bottom_color, dtype=np.float32)
        ramp = np.linspace(0.0, 1.0, roi_h, dtype=np.float32)[:, None, None]
        grad = top * (1.0 - ramp) + bottom * ramp
        grad = np.repeat(grad, roi_w, axis=1).astype(np.uint8)
        frame[y1:y2, x1:x2] = grad

    @staticmethod
    def parse_note(note_name):
        if len(note_name) < 2:
            return None, None
        if note_name[1] == "#":
            pitch = note_name[:2]
            octave_txt = note_name[2:]
        else:
            pitch = note_name[:1]
            octave_txt = note_name[1:]
        try:
            octave = int(octave_txt)
        except ValueError:
            return None, None
        return pitch, octave

    @staticmethod
    def draw_background_tint(frame):
        UIRenderer.draw_alpha_rect(frame, 0, 0, frame.shape[1], frame.shape[0], (20, 10, 10), 0.3)

    @staticmethod
    def draw_title(frame, w, h):
        s = w / 1280.0
        x, y = int(30 * s), int(30 * s)
        pw, ph = int(360 * s), int(80 * s)

        UIRenderer.draw_panel(frame, x, y, pw, ph, Config.ACCENT_GOLD, 0.5)
        UIRenderer.draw_text(
            frame,
            "MUSIC",
            x + int(20 * s),
            y + int(40 * s),
            cv2.FONT_HERSHEY_DUPLEX,
            1.3 * s,
            (255, 255, 255),
            max(1, int(2 * s)),
        )
        UIRenderer.draw_text(
            frame,
            "FINGER PIANO",
            x + int(225 * s),
            y + int(35 * s),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4 * s,
            Config.ACCENT_GOLD,
        )
        UIRenderer.draw_text(
            frame,
            "Escolha uma musica e toque no ar",
            x + int(20 * s),
            y + int(65 * s),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45 * s,
            (200, 200, 200),
        )
        cv2.line(
            frame,
            (x + int(20 * s), y + int(75 * s)),
            (x + pw - int(20 * s), y + int(75 * s)),
            Config.ACCENT_GOLD,
            max(1, int(1 * s)),
        )

    @staticmethod
    def draw_tracking_status(frame, hand_detected, w, h):
        s = w / 1280.0
        pw, ph = int(200 * s), int(42 * s)
        x0, y0 = w - pw - int(30 * s), int(120 * s)
        status_text = "MAO DETECTADA" if hand_detected else "AGUARDANDO MAO"
        status_color = (110, 220, 140) if hand_detected else (120, 120, 220)

        UIRenderer.draw_panel(frame, x0, y0, pw, ph, status_color)
        cv2.circle(
            frame,
            (x0 + int(18 * s), y0 + ph // 2),
            max(2, int(5 * s)),
            status_color,
            -1,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            status_text,
            (x0 + int(32 * s), y0 + int(27 * s)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45 * s,
            (230, 230, 230),
            max(1, int(1 * s)),
            cv2.LINE_AA,
        )

    @staticmethod
    def draw_autoplay_status(frame, autoplay_enabled, w, h):
        if not autoplay_enabled:
            return

        s = w / 1280.0
        pw, ph = int(220 * s), int(56 * s)
        x0, y0 = w - pw - int(30 * s), int(168 * s)

        UIRenderer.draw_panel(frame, x0, y0, pw, ph, Config.ACCENT_GOLD, 0.55)
        UIRenderer.draw_text(
            frame,
            "AUTOPLAY ATIVO",
            x0 + int(12 * s),
            y0 + int(22 * s),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42 * s,
            (230, 230, 230),
            max(1, int(1 * s)),
        )
        UIRenderer.draw_text(
            frame,
            "GESTOS BLOQUEADOS",
            x0 + int(12 * s),
            y0 + int(44 * s),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4 * s,
            Config.ACCENT_GOLD,
            max(1, int(1 * s)),
        )

    @staticmethod
    def draw_mode_banner(frame, text, w, h):
        s = w / 1280.0
        pw, ph = int(260 * s), int(42 * s)
        x0 = (w - pw) // 2
        y0 = int(30 * s)

        UIRenderer.draw_panel(frame, x0, y0, pw, ph, Config.ACCENT_GOLD)
        UIRenderer.draw_text(
            frame,
            text,
            x0 + int(18 * s),
            y0 + int(27 * s),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48 * s,
            (235, 235, 235),
        )

    @staticmethod
    def draw_demo_controls(frame, w, h, autoplay_enabled, autoplay_playing=False):
        s = w / 1280.0
        pw, ph = int(260 * s), int(188 * s)
        x0, y0 = w - pw - int(30 * s), int(180 * s)

        UIRenderer.draw_panel(frame, x0, y0, pw, ph, (110, 110, 110))
        UIRenderer.draw_text(
            frame,
            "CONTROLES DEMO",
            x0 + int(16 * s),
            y0 + int(24 * s),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.46 * s,
            (225, 225, 225),
        )

        controls = [
            "1 Polegar",
            "2 Indicador",
            "3 Medio",
            "4 Anelar",
            "5 Minimo",
            "A Autoplay on/off",
        ]
        for idx, label in enumerate(controls):
            cv2.putText(
                frame,
                label,
                (x0 + int(16 * s), y0 + int((48 + idx * 14) * s)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4 * s,
                (200, 200, 200),
                max(1, int(1 * s)),
                cv2.LINE_AA,
            )

        autoplay_text = "Autoplay ligado" if autoplay_enabled else "Autoplay desligado"
        autoplay_color = (120, 220, 160) if autoplay_enabled else (180, 180, 180)
        UIRenderer.draw_text(
            frame,
            autoplay_text,
            x0 + int(16 * s),
            y0 + int(146 * s),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4 * s,
            autoplay_color,
            max(1, int(1 * s)),
        )

        if autoplay_playing:
            UIRenderer.draw_text(
                frame,
                "AUTO TOCANDO AGORA",
                x0 + int(16 * s),
                y0 + int(170 * s),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4 * s,
                Config.ACCENT_GOLD,
                max(1, int(1 * s)),
            )

    @staticmethod
    def draw_error_screen(frame, message, w, h):
        s = w / 1280.0
        UIRenderer.draw_background_tint(frame)

        pw, ph = int(720 * s), int(260 * s)
        x0, y0 = (w - pw) // 2, (h - ph) // 2
        UIRenderer.draw_panel(
            frame, x0, y0, pw, ph, (70, 110, 240), 0.7, max(1, int(2 * s))
        )

        UIRenderer.draw_text(
            frame,
            "FALHA NA INICIALIZACAO",
            x0 + int(24 * s),
            y0 + int(48 * s),
            cv2.FONT_HERSHEY_DUPLEX,
            0.95 * s,
            (255, 255, 255),
            max(1, int(2 * s)),
        )

        for index, line in enumerate(UIRenderer.wrap_text(message, 48)):
            UIRenderer.draw_text(
                frame,
                line,
                x0 + int(24 * s),
                y0 + int((96 + index * 28) * s),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55 * s,
                (220, 220, 220),
            )

        UIRenderer.draw_text(
            frame,
            "Pressione Q ou ESC para fechar",
            x0 + int(24 * s),
            y0 + ph - int(28 * s),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5 * s,
            (180, 180, 180),
        )

    @staticmethod
    def draw_song_selector(frame, songs, current_idx, w, h):
        s = w / 1280.0
        pw, ph = int(360 * s), int(128 * s)
        x0, y0 = int(30 * s), int(205 * s)

        UIRenderer.draw_panel(frame, x0, y0, pw, ph, Config.ACCENT_GOLD, 0.5)
        UIRenderer.draw_text(
            frame,
            "PLAYLIST (B/N)",
            x0 + int(15 * s),
            y0 + int(25 * s),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.44 * s,
            (210, 210, 210),
        )

        for idx, song in enumerate(songs):
            is_selected = idx == current_idx
            color = Config.ACCENT_GOLD if is_selected else (170, 170, 170)
            prefix = ">" if is_selected else " "
            UIRenderer.draw_text(
                frame,
                f"{prefix} {idx + 1}. {song['name']}",
                x0 + int(15 * s),
                y0 + int((48 + idx * 22) * s),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.43 * s,
                color,
                max(1, int(1 * s)),
            )

    @staticmethod
    def draw_sequence(frame, song_name, sequence, seq_idx, w, h):
        s = w / 1280.0
        pw, ph = int(350 * s), int(80 * s)
        x0, y0 = w - pw - int(30 * s), int(30 * s)

        UIRenderer.draw_panel(frame, x0, y0, pw, ph, Config.ACCENT_GOLD, 0.5)

        UIRenderer.draw_text(
            frame,
            f"{song_name} | Proximas notas",
            x0 + int(15 * s),
            y0 + int(25 * s),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4 * s,
            (200, 200, 200),
        )

        seq_len = len(sequence)
        for i in range(5):
            idx = (seq_idx + i) % seq_len
            note = sequence[idx]

            is_current = (i == 0)
            color = Config.ACCENT_GOLD if is_current else (150,150,150)
            font_scale = (1.0 if is_current else 0.6) * s
            thickness = max(1, int((2 if is_current else 1) * s))

            y_text = y0 + int(60*s) if is_current else y0 + int(55*s)
            UIRenderer.draw_text(
                frame,
                note,
                x0 + int(20 * s) + i * int(65 * s),
                y_text,
                cv2.FONT_HERSHEY_DUPLEX,
                font_scale,
                color,
                thickness,
            )

    @staticmethod
    def draw_waveform(frame, wave_data, w, h):
        s = w / 1280.0
        pw, ph = int(360 * s), int(60 * s)
        x, y = int(30 * s), int(130 * s)

        UIRenderer.draw_panel(frame, x, y, pw, ph, (0, 0, 0), 0.4)
        if len(wave_data) < 2: return

        pts = np.array(wave_data[-360:], dtype=np.float32)
        if pts.max() - pts.min() == 0: return

        pts = (pts - pts.min()) / (pts.max() - pts.min() + 1e-6)
        pts = (pts * (ph - int(10*s))).astype(int)

        x_vals = np.linspace(0, pw, len(pts), dtype=int)
        for i in range(1, len(pts)):
            cv2.line(frame, (x + x_vals[i-1], y + ph - int(5*s) - pts[i-1]), (x + x_vals[i], y + ph - int(5*s) - pts[i]), Config.ACCENT_GOLD, max(1, int(2*s)), cv2.LINE_AA)

    @staticmethod
    def draw_piano_keys(frame, active_fingers, finger_notes, h, w):
        s = w / 1280.0
        octaves = 3 if w >= 1100 else 2
        white_per_octave = 7
        white_count = octaves * white_per_octave

        key_h = int((210 if octaves == 2 else 185) * s)
        y0 = h - key_h - int(26 * s)
        side_pad = int(24 * s)
        white_w = max(20, int((w - 2 * side_pad) / white_count))
        keyboard_w = white_w * white_count
        start_x = (w - keyboard_w) // 2

        white_classes = ["C", "D", "E", "F", "G", "A", "B"]
        black_after = {"C": "C#", "D": "D#", "F": "F#", "G": "G#", "A": "A#"}
        black_enharmonic = {
            "C#": "Db",
            "D#": "Eb",
            "F#": "Gb",
            "G#": "Ab",
            "A#": "Bb",
        }
        solfege_by_white = {
            "C": "DO",
            "D": "RE",
            "E": "MI",
            "F": "FA",
            "G": "SOL",
            "A": "LA",
            "B": "SI",
        }
        solfege_colors = {
            "C": (192, 92, 76),
            "D": (196, 138, 56),
            "E": (117, 166, 72),
            "F": (72, 153, 140),
            "G": (74, 130, 189),
            "A": (118, 106, 194),
            "B": (176, 90, 170),
        }

        white_key_rects = {}
        black_key_rects = {}

        note_to_finger = {}
        for finger in Config.FINGER_KEYS:
            note = finger_notes.get(finger)
            if note is None:
                continue
            if note not in note_to_finger or active_fingers.get(finger, False):
                note_to_finger[note] = finger

        # Moldura do teclado e sombra principal.
        UIRenderer.draw_rounded_rect(
            frame,
            start_x - int(10 * s),
            y0 - int(16 * s),
            keyboard_w + int(20 * s),
            key_h + int(34 * s),
            (12, 12, 12),
            int(10 * s),
            -1,
        )
        UIRenderer.draw_alpha_rect(
            frame,
            start_x - int(6 * s),
            y0 + key_h + int(2 * s),
            keyboard_w + int(12 * s),
            int(18 * s),
            (0, 0, 0),
            0.35,
        )

        base_octave = 4
        key_idx = 0
        for octave in range(base_octave, base_octave + octaves):
            for pitch in white_classes:
                x1 = start_x + key_idx * white_w
                x2 = x1 + white_w
                note_name = f"{pitch}{octave}"

                mapped_finger = note_to_finger.get(note_name)
                is_active = bool(
                    mapped_finger and active_fingers.get(mapped_finger, False)
                )
                press_offset = int(4 * s) if is_active else 0
                y_press = y0 + press_offset

                white_key_rects[note_name] = (x1, y_press, x2, y_press + key_h)

                # Sombra individual da tecla branca.
                UIRenderer.draw_alpha_rect(
                    frame,
                    x1 + int(1 * s),
                    y_press + int(3 * s),
                    white_w - int(2 * s),
                    key_h,
                    (0, 0, 0),
                    0.16,
                )

                UIRenderer.draw_vertical_gradient_rect(
                    frame,
                    x1,
                    y_press,
                    white_w,
                    key_h,
                    (252, 252, 252),
                    (225, 225, 225),
                )
                UIRenderer.draw_rounded_rect(
                    frame,
                    x1,
                    y_press,
                    white_w,
                    key_h,
                    (80, 80, 80),
                    int(4 * s),
                    max(1, int(1 * s)),
                )

                if mapped_finger:
                    accent = Config.NOTE_COLORS[mapped_finger]
                    glow_alpha = 0.60 if is_active else 0.25
                    UIRenderer.draw_alpha_rect(
                        frame,
                        x1 + int(2 * s),
                        y_press + int(key_h * 0.50),
                        white_w - int(4 * s),
                        int(key_h * 0.46),
                        accent,
                        glow_alpha,
                    )

                # Nome da nota centralizado e solfejo na base da tecla branca.
                text_size, _ = cv2.getTextSize(
                    pitch,
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.78 * s,
                    max(1, int(1 * s)),
                )
                text_x = x1 + (white_w - text_size[0]) // 2
                text_y = y_press + int(key_h * 0.78)
                cv2.putText(
                    frame,
                    pitch,
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.78 * s,
                    (32, 32, 32),
                    max(1, int(1 * s)),
                    cv2.LINE_AA,
                )

                solfege = solfege_by_white[pitch]
                sol_badge_w = int(white_w * 0.72)
                sol_badge_h = int(18 * s)
                sol_x = x1 + (white_w - sol_badge_w) // 2
                sol_y = y_press + key_h - sol_badge_h - int(6 * s)
                sol_color = solfege_colors[pitch]

                UIRenderer.draw_rounded_rect(
                    frame,
                    sol_x,
                    sol_y,
                    sol_badge_w,
                    sol_badge_h,
                    sol_color,
                    int(5 * s),
                    -1,
                )
                sol_size, _ = cv2.getTextSize(
                    solfege,
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.30 * s,
                    max(1, int(1 * s)),
                )
                cv2.putText(
                    frame,
                    solfege,
                    (
                        sol_x + (sol_badge_w - sol_size[0]) // 2,
                        sol_y + int(13 * s),
                    ),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.30 * s,
                    (245, 245, 245),
                    max(1, int(1 * s)),
                    cv2.LINE_AA,
                )

                if pitch in black_after:
                    black_note = f"{black_after[pitch]}{octave}"
                    black_w = int(white_w * 0.62)
                    black_h = int(key_h * 0.62)

                    bx1 = x2 - black_w // 2
                    bx2 = bx1 + black_w

                    mapped_black_finger = note_to_finger.get(black_note)
                    is_black_active = bool(
                        mapped_black_finger
                        and active_fingers.get(mapped_black_finger, False)
                    )
                    black_offset = int(2 * s) if is_black_active else 0
                    by1 = y0 + black_offset
                    by2 = by1 + black_h

                    black_key_rects[black_note] = (bx1, by1, bx2, by2)

                key_idx += 1

        # Teclas pretas ficam na camada superior.
        for note_name, (bx1, by1, bx2, by2) in black_key_rects.items():
            mapped_finger = note_to_finger.get(note_name)
            is_active = bool(mapped_finger and active_fingers.get(mapped_finger, False))
            pitch, _ = UIRenderer.parse_note(note_name)

            UIRenderer.draw_alpha_rect(
                frame,
                bx1 + int(1 * s),
                by1 + int(3 * s),
                bx2 - bx1,
                by2 - by1,
                (0, 0, 0),
                0.28,
            )
            UIRenderer.draw_vertical_gradient_rect(
                frame,
                bx1,
                by1,
                bx2 - bx1,
                by2 - by1,
                (48, 48, 56),
                (10, 10, 12),
            )

            # Brilho suave para efeito glossy das teclas pretas.
            UIRenderer.draw_alpha_rect(
                frame,
                bx1 + int(1 * s),
                by1 + int(1 * s),
                bx2 - bx1 - int(2 * s),
                int((by2 - by1) * 0.24),
                (255, 255, 255),
                0.16,
            )
            UIRenderer.draw_rounded_rect(
                frame,
                bx1,
                by1,
                bx2 - bx1,
                by2 - by1,
                (5, 5, 5),
                int(4 * s),
                max(1, int(1 * s)),
            )

            if mapped_finger:
                accent = Config.NOTE_COLORS[mapped_finger]
                glow_alpha = 0.65 if is_active else 0.35
                UIRenderer.draw_alpha_rect(
                    frame,
                    bx1 + int(1 * s),
                    by1 + int(2 * s),
                    bx2 - bx1 - int(2 * s),
                    by2 - by1 - int(3 * s),
                    accent,
                    glow_alpha,
                )

            upper = pitch if pitch is not None else note_name
            lower = black_enharmonic.get(upper, "")

            text_size, _ = cv2.getTextSize(
                upper,
                cv2.FONT_HERSHEY_DUPLEX,
                0.28 * s,
                max(1, int(1 * s)),
            )
            tx = bx1 + ((bx2 - bx1) - text_size[0]) // 2
            ty = by1 + int((by2 - by1) * 0.46)
            cv2.putText(
                frame,
                upper,
                (tx, ty),
                cv2.FONT_HERSHEY_DUPLEX,
                0.28 * s,
                (236, 236, 236),
                max(1, int(1 * s)),
                cv2.LINE_AA,
            )

            if lower:
                lower_size, _ = cv2.getTextSize(
                    lower,
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.24 * s,
                    max(1, int(1 * s)),
                )
                cv2.putText(
                    frame,
                    lower,
                    (
                        bx1 + ((bx2 - bx1) - lower_size[0]) // 2,
                        by1 + int((by2 - by1) * 0.70),
                    ),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.24 * s,
                    (226, 226, 226),
                    max(1, int(1 * s)),
                    cv2.LINE_AA,
                )

        # Indicador do dedo na tecla correspondente.
        for note_name, finger in note_to_finger.items():
            pitch, _ = UIRenderer.parse_note(note_name)
            is_black = pitch is not None and "#" in pitch
            target = (
                black_key_rects.get(note_name)
                if is_black
                else white_key_rects.get(note_name)
            )
            if target is None:
                continue

            x1, y1, x2, y2 = target
            accent = Config.NOTE_COLORS[finger]
            badge_text = finger[0]
            badge_w = (
                int(max(white_w * 0.42, 20 * s))
                if not is_black
                else int(max((x2 - x1) * 0.6, 18 * s))
            )
            badge_h = int(16 * s)
            bx = x1 + ((x2 - x1) - badge_w) // 2
            by = (y2 + int(4 * s)) if is_black else (y2 - badge_h - int(4 * s))

            UIRenderer.draw_rounded_rect(
                frame,
                bx,
                by,
                badge_w,
                badge_h,
                accent,
                int(5 * s),
                -1,
            )
            UIRenderer.draw_rounded_rect(
                frame,
                bx,
                by,
                badge_w,
                badge_h,
                (250, 250, 250),
                int(5 * s),
                max(1, int(1 * s)),
            )

            txt_size, _ = cv2.getTextSize(
                badge_text,
                cv2.FONT_HERSHEY_DUPLEX,
                0.33 * s,
                max(1, int(1 * s)),
            )
            cv2.putText(
                frame,
                badge_text,
                (bx + (badge_w - txt_size[0]) // 2, by + int(12 * s)),
                cv2.FONT_HERSHEY_DUPLEX,
                0.33 * s,
                (255, 255, 255),
                max(1, int(1 * s)),
                cv2.LINE_AA,
            )

    @staticmethod
    def draw_landmarks(frame, landmarks, active_fingers, finger_notes, w, h):
        s = w / 1280.0
        hand_landmarks_connections = load_hand_landmarks_connections()

        for conn in hand_landmarks_connections.HAND_CONNECTIONS:
            p1, p2 = landmarks[conn.start], landmarks[conn.end]
            cv2.line(
                frame,
                (int(p1.x * w), int(p1.y * h)),
                (int(p2.x * w), int(p2.y * h)),
                (150, 150, 150),
                max(1, int(1 * s)),
                cv2.LINE_AA,
            )

        for idx, lm in enumerate(landmarks):
            if idx not in Config.FINGER_TIPS:
                cv2.circle(
                    frame,
                    (int(lm.x * w), int(lm.y * h)),
                    max(1, int(3 * s)),
                    (180, 180, 180),
                    -1,
                    cv2.LINE_AA,
                )

        for i, fk in enumerate(Config.FINGER_KEYS):
            lm = landmarks[Config.FINGER_TIPS[i]]
            cx, cy = int(lm.x * w), int(lm.y * h)
            active = active_fingers.get(fk, False)
            color = Config.NOTE_COLORS[fk]

            if active:
                overlay = frame.copy()
                cv2.circle(overlay, (cx, cy), int(35 * s), color, -1)
                cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

                cv2.circle(
                    frame, (cx, cy), int(12 * s), (255, 255, 255), -1, cv2.LINE_AA
                )
                cv2.circle(
                    frame, (cx, cy), int(16 * s), color, max(1, int(2 * s)), cv2.LINE_AA
                )

                cv2.putText(
                    frame,
                    finger_notes[fk],
                    (cx + int(25 * s), cy - int(25 * s)),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.9 * s,
                    color,
                    max(1, int(2 * s)),
                    cv2.LINE_AA,
                )
            else:
                cv2.circle(frame, (cx, cy), int(6*s), (220,220,220), -1, cv2.LINE_AA)
                cv2.circle(frame, (cx, cy), int(9*s), (100,100,100), max(1, int(1*s)), cv2.LINE_AA)
