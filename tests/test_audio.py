import unittest
from importlib.util import find_spec

import numpy as np

from config import Config

pygame_available = find_spec("pygame") is not None
scipy_available = find_spec("scipy") is not None

if pygame_available and scipy_available:
    from audio import AudioEngine


@unittest.skipUnless(pygame_available and scipy_available, "pygame e scipy sao necessarios para testar o sintetizador")
class AudioEngineTests(unittest.TestCase):
    def test_synthesize_note_returns_stereo_int16_buffer(self):
        engine = AudioEngine.__new__(AudioEngine)

        wave = engine._synthesize_note(Config.NOTE_FREQS["A5"])

        expected_samples = int(Config.SAMPLE_RATE * Config.DURATION)
        self.assertEqual(wave.shape, (expected_samples, 2))
        self.assertEqual(wave.dtype, np.int16)
        self.assertTrue(np.any(wave != 0))


if __name__ == "__main__":
    unittest.main()