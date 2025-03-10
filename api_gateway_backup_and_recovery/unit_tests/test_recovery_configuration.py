import unittest
from api_gateway_backup_and_recovery.recovery_configuration import configure_recovery

class TestRecoveryConfiguration(unittest.TestCase):

    def setUp(self):
        # This method will be called before every test
        self.valid_config = {
            'recovery_location': '/valid/recovery/location',
            'recovery_strategy': 'full'
        }
        self.invalid_config1 = {
            'recovery_location': '',
            'recovery_strategy': 'full'
        }
        self.invalid_config2 = {
            'recovery_location': '/valid/recovery/location',
            'recovery_strategy': ''
        }

    def test_configure_recovery_valid(self):
        # Tests the recovery configuration setup to ensure valid configurations are stored.
        try:
            result = configure_recovery(self.valid_config)
            self.assertTrue(result)
        except Exception as e:
            self.fail(f"configure_recovery() raised {type(e).__name__} unexpectedly: {e}")

    def test_configure_recovery_invalid(self):
        # Tests the recovery configuration setup to ensure invalid configurations are rejected.
        with self.assertRaises(ValueError):
            configure_recovery(self.invalid_config1)
        with self.assertRaises(ValueError):
            configure_recovery(self.invalid_config2)

if __name__ == "__main__":
    unittest.main()
