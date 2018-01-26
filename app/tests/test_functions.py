import unittest
# import logging
from app.scripts_bank.lib.functions import containsSkipped, removeDictKey, setUserCredentials


class TestFunctions(unittest.TestCase):
    """CI testing class for Cisco IOS devices."""

    def setUp(self):
        """Initialize static class testing variables."""
        pass

    def test_setUserCredentials(self):
        """Test creds class is returned properly."""
        actual_output = setUserCredentials("admin", "Password1", privPassword="Priv2")
        self.assertEqual(actual_output.un, "admin")
        self.assertEqual(actual_output.pw, "Password1")
        self.assertEqual(actual_output.priv, "Priv2")

    def test_containsSkipped(self):
        """Test function if the word 'skipped' is in the provided string."""
        input_data = "Unable to connect - skipped connection attempt."
        actual_output = containsSkipped(input_data)
        expected_output = True

        self.assertEqual(actual_output, expected_output)
        self.assertIsInstance(actual_output, bool)

    def test_removeDictKey(self):
        """Test removal of key from dictionary."""
        testDict = {"name": "Cisco", "type": "switch"}
        testKey = "name"
        actual_output = removeDictKey(testDict, testKey)
        expected_output = {"type": "switch"}

        self.assertEqual(actual_output, expected_output)
        self.assertIsInstance(actual_output, dict)
