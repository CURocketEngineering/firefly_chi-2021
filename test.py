"""
test.py

Unit testing the rocket.
"""

import unittest

from modules import Actions

class TestActions:

    def test_halt(self):
        self.assertTrue(
            "HALT" == Actions.halt({}, None)
        )

    def test_idle(self):
        self.assertTrue(
            "IDLE" == Actions.halt()
        )
