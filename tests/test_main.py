import unittest

from config import Config
from main import FingerPianoApp


class DemoModeFlowTests(unittest.TestCase):
    def test_handle_demo_toggle_turns_autoplay_on_and_schedules_next_step(self):
        app = FingerPianoApp(demo_mode=True, autoplay_demo=False)

        toggled = app.handle_demo_toggle(ord("a"), now=3.5)

        self.assertTrue(toggled)
        self.assertTrue(app.autoplay_demo)
        self.assertEqual(app.next_autoplay_at, 3.5)

    def test_handle_demo_toggle_turns_autoplay_off_and_clears_timer(self):
        app = FingerPianoApp(demo_mode=True, autoplay_demo=True)
        app.next_autoplay_at = 9.0

        toggled = app.handle_demo_toggle(ord("A"), now=4.0)

        self.assertTrue(toggled)
        self.assertFalse(app.autoplay_demo)
        self.assertEqual(app.next_autoplay_at, 0.0)

    def test_handle_demo_toggle_ignores_other_keys(self):
        app = FingerPianoApp(demo_mode=True, autoplay_demo=False)

        toggled = app.handle_demo_toggle(ord("1"), now=2.0)

        self.assertFalse(toggled)
        self.assertFalse(app.autoplay_demo)

    def test_trigger_note_advances_sequence_when_note_matches_target(self):
        app = FingerPianoApp(demo_mode=True)
        finger_notes = app.get_current_finger_notes()

        app.trigger_note("PINKY", finger_notes, now=1.0)

        self.assertEqual(app.seq_idx, 1)
        self.assertGreater(app.cooldowns["PINKY"], 1.0)
        self.assertGreater(app.demo_flash_until["PINKY"], 1.0)
        self.assertEqual(len(app.wave_buf), 400)

    def test_trigger_note_does_not_advance_sequence_for_wrong_note(self):
        app = FingerPianoApp(demo_mode=True)
        finger_notes = app.get_current_finger_notes()

        app.trigger_note("INDEX", finger_notes, now=1.0)

        self.assertEqual(app.seq_idx, 0)

    def test_apply_demo_input_returns_none_for_unknown_key(self):
        app = FingerPianoApp(demo_mode=True)

        result = app.apply_demo_input(ord("x"), app.get_current_finger_notes(), now=1.0)

        self.assertIsNone(result)
        self.assertEqual(app.seq_idx, 0)

    def test_apply_demo_input_respects_cooldown(self):
        app = FingerPianoApp(demo_mode=True)
        finger_notes = app.get_current_finger_notes()

        first = app.apply_demo_input(ord("5"), finger_notes, now=1.0)
        second = app.apply_demo_input(ord("5"), finger_notes, now=1.1)

        self.assertEqual(first, "PINKY")
        self.assertIsNone(second)
        self.assertEqual(app.seq_idx, 1)

    def test_apply_demo_input_triggers_mapped_finger(self):
        app = FingerPianoApp(demo_mode=True)

        triggered_finger = app.apply_demo_input(
            ord("1"), app.get_current_finger_notes(), now=1.0
        )

        self.assertEqual(triggered_finger, "THUMB")
        self.assertEqual(app.cooldowns["THUMB"], 1.0 + Config.COOLDOWN_SEC)

    def test_get_target_finger_resolves_current_sequence_note(self):
        app = FingerPianoApp(demo_mode=True)

        target_finger = app.get_target_finger(app.get_current_finger_notes())

        self.assertEqual(target_finger, "PINKY")

    def test_apply_demo_autoplay_triggers_target_finger(self):
        app = FingerPianoApp(demo_mode=True, autoplay_demo=True)

        triggered_finger = app.apply_demo_autoplay(app.get_current_finger_notes(), now=1.0)

        self.assertEqual(triggered_finger, "PINKY")
        self.assertEqual(app.seq_idx, 1)
        self.assertEqual(app.next_autoplay_at, 1.0 + Config.DEMO_AUTOPLAY_SEC)

    def test_apply_demo_autoplay_respects_next_autoplay_time(self):
        app = FingerPianoApp(demo_mode=True, autoplay_demo=True)
        app.next_autoplay_at = 2.0

        triggered_finger = app.apply_demo_autoplay(app.get_current_finger_notes(), now=1.0)

        self.assertIsNone(triggered_finger)
        self.assertEqual(app.seq_idx, 0)


if __name__ == "__main__":
    unittest.main()