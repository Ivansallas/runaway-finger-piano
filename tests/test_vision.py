import unittest
from importlib.util import find_spec
from types import SimpleNamespace
from unittest.mock import patch

mediapipe_available = find_spec("mediapipe") is not None

from vision import HandTracker, ModelDownloader


def landmark(x=0.0, y=0.0):
    return SimpleNamespace(x=x, y=y)


@unittest.skipUnless(mediapipe_available, "mediapipe e necessario para importar vision.py")
class HandTrackerRuleTests(unittest.TestCase):
    def test_thumb_pressed_for_right_hand_when_tip_is_left_of_pip(self):
        landmarks = [landmark() for _ in range(21)]
        landmarks[4] = landmark(x=0.20)
        landmarks[3] = landmark(x=0.35)

        self.assertTrue(HandTracker.is_finger_pressed(landmarks, 0, "Right"))

    def test_thumb_pressed_for_left_hand_when_tip_is_right_of_pip(self):
        landmarks = [landmark() for _ in range(21)]
        landmarks[4] = landmark(x=0.60)
        landmarks[3] = landmark(x=0.45)

        self.assertTrue(HandTracker.is_finger_pressed(landmarks, 0, "Left"))

    def test_non_thumb_pressed_when_tip_is_below_pip_threshold(self):
        landmarks = [landmark() for _ in range(21)]
        landmarks[8] = landmark(y=0.52)
        landmarks[6] = landmark(y=0.50)

        self.assertTrue(HandTracker.is_finger_pressed(landmarks, 1, "Right"))

    def test_non_thumb_not_pressed_when_tip_is_above_pip_threshold(self):
        landmarks = [landmark() for _ in range(21)]
        landmarks[8] = landmark(y=0.44)
        landmarks[6] = landmark(y=0.50)

        self.assertFalse(HandTracker.is_finger_pressed(landmarks, 1, "Right"))

    def test_non_thumb_uses_adaptive_margin_to_avoid_small_jitter(self):
        landmarks = [landmark() for _ in range(21)]
        landmarks[0] = landmark(x=0.10, y=0.10)
        landmarks[8] = landmark(y=0.49)
        landmarks[6] = landmark(y=0.50)

        self.assertFalse(HandTracker.is_finger_pressed(landmarks, 1, "Right"))


class ModelDownloaderTests(unittest.TestCase):
    @patch("builtins.print")
    @patch("vision.os.path.getsize", return_value=20_000)
    @patch("vision.os.path.exists", return_value=True)
    @patch("vision.urllib.request.urlretrieve")
    def test_existing_model_skips_download(
        self, mock_urlretrieve, _mock_exists, _mock_getsize, _mock_print
    ):
        ModelDownloader.ensure_model_exists()

        mock_urlretrieve.assert_not_called()

    @patch("builtins.print")
    @patch("vision.urllib.request.urlretrieve")
    @patch("vision.os.makedirs")
    @patch("vision.os.path.getsize", return_value=0)
    @patch("vision.os.path.exists", return_value=False)
    def test_missing_model_downloads_file(
        self,
        _mock_exists,
        _mock_getsize,
        mock_makedirs,
        mock_urlretrieve,
        _mock_print,
    ):
        ModelDownloader.ensure_model_exists()

        mock_makedirs.assert_called_once()
        mock_urlretrieve.assert_called_once()

    @patch("builtins.print")
    @patch("vision.urllib.request.urlretrieve", side_effect=OSError("sem rede"))
    @patch("vision.os.makedirs")
    @patch("vision.os.path.getsize", return_value=0)
    @patch("vision.os.path.exists", return_value=False)
    def test_download_failure_raises_runtime_error(
        self,
        _mock_exists,
        _mock_getsize,
        _mock_makedirs,
        _mock_urlretrieve,
        _mock_print,
    ):
        with self.assertRaises(RuntimeError):
            ModelDownloader.ensure_model_exists()


if __name__ == "__main__":
    unittest.main()
