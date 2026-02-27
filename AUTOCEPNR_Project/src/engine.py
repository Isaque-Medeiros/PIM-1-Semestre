"""Core business logic for the Auto‑Filler engine."""


class SabreScreen:
    """Represents a captured Sabre Interact screen."""

    def __init__(self, raw_image=None):
        self.raw_image = raw_image
        self.extracted_text = None

    def parse_fields(self):
        raise NotImplementedError

    def validate_integrity(self):
        raise NotImplementedError


class LatamForm:
    """Encapsulates the CEPNR HTML form to be filled."""

    def __init__(self, browser_tab=None):
        self.browser_tab = browser_tab

    def focus(self):
        raise NotImplementedError

    def fill_all(self, data):
        raise NotImplementedError

    def submit_form(self):
        raise NotImplementedError
