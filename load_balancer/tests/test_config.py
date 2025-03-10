import unittest
from load_balancer import config

class TestLoadBalancerConfig(unittest.TestCase):

    def setUp(self):
        # This will run before every test method
        self.valid_config = {
            "service1": {"instances": ["instanceA", "instanceB"], "strategy": "round_robin"},
            "service2": {"instances": ["instanceC"], "strategy": "least_connections"}
        }
        self.invalid_config = {
            "service1": {"instances": [], "strategy": "unknown_stratey"},
            "service2": {"instances": ["instanceC"], "strategy": "least_connections"}
        }

    def test_load_configurations(self):
        # Test that configuration settings are loaded correctly
        loaded_config = config.load_configurations()
        
        # Check if the loaded configurations match the expected values
        self.assertIsInstance(loaded_config, dict)
        self.assertIn("service1", loaded_config)
        self.assertIn("service2", loaded_config)
        self.assertEqual(
            loaded_config["service1"]["strategy"], self.valid_config["service1"]["strategy"]
        )
        self.assertEqual(
            loaded_config["service2"]["strategy"], self.valid_config["service2"]["strategy"]
        )

    def test_validate_configurations(self):
        # Test that invalid configurations are correctly identified
        valid_status = config.validate_configurations(self.valid_config)
        invalid_status = config.validate_configurations(self.invalid_config)
        
        # Check if the function responds appropriately to misconfigurations
        self.assertTrue(valid_status)
        self.assertFalse(invalid_status)

if __name__ == '__main__':
    unittest.main()
