"""
test.py

Unit testing the rocket.

TODO
"""

import unittest

from lib import Actions

class TestActions:

    def test_halt(self):
        self.assertTrue(
            "HALT" == Actions.halt({}, None)
        )

    def test_idle(self):
        self.assertTrue(
            "IDLE" == Actions.halt()
        )


if __name__ == "__main__":
    unittest.main()
