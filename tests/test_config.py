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

    def test_music_library_has_more_than_one_song(self):
        self.assertGreaterEqual(len(Config.MUSIC_LIBRARY), 2)

    def test_get_sequence_returns_selected_song_sequence(self):
        self.assertEqual(
            Config.get_sequence(0),
            Config.MUSIC_LIBRARY[0]["sequence"],
        )
        self.assertEqual(
            Config.get_sequence(1),
            Config.MUSIC_LIBRARY[1]["sequence"],
        )

    def test_silent_night_notes_have_thumb_mapping(self):
        self.assertEqual(Config.get_thumb_note(0, ["G5"]), "G5")
        self.assertEqual(Config.get_thumb_note(0, ["B5"]), "B5")
        self.assertEqual(Config.get_thumb_note(0, ["C6"]), "C6")
        self.assertEqual(Config.get_thumb_note(0, ["D6"]), "D6")

    def test_dragon_ball_notes_have_frequencies(self):
        dragon_song = next(
            song for song in Config.MUSIC_LIBRARY if song["name"] == "DRAGON BALL GT"
        )
        for note in dragon_song["sequence"]:
            self.assertIn(note, Config.NOTE_FREQS)

    def test_dragon_ball_high_notes_have_thumb_mapping(self):
        self.assertEqual(Config.get_thumb_note(0, ["D5"]), "D5")
        self.assertEqual(Config.get_thumb_note(0, ["F6"]), "F6")
        self.assertEqual(Config.get_thumb_note(0, ["G6"]), "G6")
        self.assertEqual(Config.get_thumb_note(0, ["A6"]), "A6")
        self.assertEqual(Config.get_thumb_note(0, ["F7"]), "F7")


if __name__ == "__main__":
    unittest.main()
