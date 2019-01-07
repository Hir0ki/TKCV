import numpy as np
import pytest
from video_utils import resize_frame, pixel_in_color_range


def test_good_pixel_in_color_range():
    MIN = np.array([10, 80, 120])
    MAX = np.array([70, 220, 240])
    pixel = np.array([20, 80, 120])

    result = pixel_in_color_range(MIN, MAX, pixel)

    assert result is True


def test_bad_pixel_in_color_range():
    MIN = np.array([10, 80, 120])
    MAX = np.array([70, 220, 240])
    pixel = np.array([20, 230, 120])

    result = pixel_in_color_range(MIN, MAX, pixel)

    assert result is False


def test_good_resize_frame():
    pass


def test_bad_resize_frame():
    pass
