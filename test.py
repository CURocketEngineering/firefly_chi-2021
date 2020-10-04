#!/bin/python
"""
System integrity testing for the fchi.
"""

import unittest

from src import Config, Data, State

class TestStates(unittest.TestCase):
    """
    Test state transitions.
    """
    
    def test_apogee_generic(self):
        """
        Test that apogee occurs after enough pressure differentials are positive.
        """
        configuration = {}
        config = Config.Config(configuration, "COAST")
        data = Data.Data("output.json", config)
        state = State.State(config, data)
        pressures = [5, 4, 3, 2, 2, 1, 2, 2, 3, 4, 5]
        for i, p in enumerate(pressures):
            data.current_data["sensors"]["pres"] = p
            data.add_dp(p - data.last_pressure)
            data.last_pressure = p
            state.act()
        self.assertTrue(config.state == "APOGEE")

class TestPluginHooks(unittest.TestCase):
    pass

class TestLogging(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()  # Run the tests
