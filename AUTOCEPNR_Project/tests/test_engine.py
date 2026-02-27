import pytest

from autocepnr.engine import SabreScreen, LatamForm


def test_sabre_screen_init():
    s = SabreScreen()
    assert s.raw_image is None
    assert s.extracted_text is None


def test_latam_form_init():
    f = LatamForm()
    assert f.browser_tab is None
