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
        key_w, key_h = int(130 * s), int(160 * s)
        spacing = int(20 * s)
        total_w = 5 * key_w + 4 * spacing
        start_x = (w - total_w) // 2
        y0 = h - key_h - int(40 * s)

        for i, finger in enumerate(Config.FINGER_KEYS):
            note = finger_notes[finger]
            x = start_x + i * (key_w + spacing)
            active = active_fingers.get(finger, False)
            color = Config.NOTE_COLORS[finger]

            bg_color = color if active else (255, 255, 255)
            alpha = 0.6 if active else 0.08
            UIRenderer.draw_alpha_rect(frame, x, y0, key_w, key_h, bg_color, alpha)

            border_color = color if active else (150, 150, 150)
            cv2.rectangle(
                frame,
                (x, y0),
                (x + key_w, y0 + key_h),
                border_color,
                max(1, int((2 if active else 1) * s)),
                cv2.LINE_AA,
            )

            if active:
                cv2.rectangle(
                    frame,
                    (x, y0 + key_h - int(8 * s)),
                    (x + key_w, y0 + key_h),
                    (255, 255, 255),
                    -1,
                )

            text_color = (255, 255, 255) if active else (200, 200, 200)

            font_scale_note = 1.2 * s
            sz, _ = cv2.getTextSize(
                note, cv2.FONT_HERSHEY_DUPLEX, font_scale_note, max(1, int(2 * s))
            )
            tx = x + (key_w - sz[0]) // 2
            cv2.putText(
                frame,
                note,
                (tx, y0 + key_h // 2 + int(10 * s)),
                cv2.FONT_HERSHEY_DUPLEX,
                font_scale_note,
                text_color,
                max(1, int(2 * s)),
                cv2.LINE_AA,
            )

            font_scale_sub = 0.45 * s
            sz_sub, _ = cv2.getTextSize(
                finger, cv2.FONT_HERSHEY_SIMPLEX, font_scale_sub, max(1, int(1 * s))
            )
            tx_sub = x + (key_w - sz_sub[0]) // 2
            cv2.putText(
                frame,
                finger,
                (tx_sub, y0 + key_h - int(20 * s)),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale_sub,
                text_color,
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
