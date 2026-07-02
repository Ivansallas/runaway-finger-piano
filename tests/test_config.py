import unittest

from config import Config


class ConfigTests(unittest.TestCase):
    def test_thumb_note_changes_with_sequence_progress(self):
        self.assertEqual(Config.get_thumb_note(0), "E5")
        self.assertEqual(Config.get_thumb_note(15), "E5")
        self.assertEqual(Config.get_thumb_note(16), "D#5")
        self.assertEqual(Config.get_thumb_note(20), "C#5")
        self.assertEqual(Config.get_thumb_note(24), "G#5")

    def test_finger_notes_keep_static_notes_except_thumb(self):
        finger_notes = Config.get_finger_notes(20)

        self.assertEqual(finger_notes["THUMB"], "C#5")
        self.assertEqual(finger_notes["INDEX"], "A5")
        self.assertEqual(finger_notes["MIDDLE"], "C#6")
        self.assertEqual(finger_notes["RING"], "D#6")
        self.assertEqual(finger_notes["PINKY"], "E6")

    def test_demo_key_bindings_map_number_keys_to_fingers(self):
        self.assertEqual(Config.get_demo_finger("1"), "THUMB")
        self.assertEqual(Config.get_demo_finger("2"), "INDEX")
        self.assertEqual(Config.get_demo_finger("3"), "MIDDLE")
        self.assertEqual(Config.get_demo_finger("4"), "RING")
        self.assertEqual(Config.get_demo_finger("5"), "PINKY")
        self.assertIsNone(Config.get_demo_finger("x"))


if __name__ == "__main__":
    unittest.main()