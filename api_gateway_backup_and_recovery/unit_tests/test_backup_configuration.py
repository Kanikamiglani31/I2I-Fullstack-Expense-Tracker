import unittest
from api_gateway_backup_and_recovery.backup_configuration import configure_backup

class TestBackupConfiguration(unittest.TestCase):
    def test_configure_backup_valid(self):
        # Valid configuration scenarios
        valid_configurations = [
            {"interval": "24h", "retention": "30d", "location": "/backup/location1"},
            {"interval": "12h", "retention": "60d", "location": "/backup/location2"},
            {"interval": "6h", "retention": "90d", "location": "/backup/location3"},
        ]

        for config in valid_configurations:
            with self.subTest(config=config):
                result = configure_backup(config["interval"], config["retention"], config["location"])
                self.assertTrue(result["success"])
                self.assertEqual(result["interval"], config["interval"])
                self.assertEqual(result["retention"], config["retention"])
                self.assertEqual(result["location"], config["location"])

    def test_configure_backup_invalid(self):
        # Invalid configuration scenarios
        invalid_configurations = [
            {"interval": "", "retention": "30d", "location": "/backup/location1"},
            {"interval": "24h", "retention": "", "location": "/backup/location2"},
            {"interval": "24h", "retention": "30d", "location": ""},
            {"interval": "1h", "retention": "1000d", "location": "/backup/location4"},
            {"interval": "invalid", "retention": "30d", "location": "/backup/location5"},
            {"interval": "24h", "retention": "invalid", "location": "/backup/location6"},
        ]

        for config in invalid_configurations:
            with self.subTest(config=config):
                result = configure_backup(config["interval"], config["retention"], config["location"])
                self.assertFalse(result["success"])
                self.assertIn("error", result)

if __name__ == '__main__':
    unittest.main()
