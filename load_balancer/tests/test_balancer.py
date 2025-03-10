import unittest
from unittest.mock import MagicMock, patch
from load_balancer.balancer import distribute_requests, monitor_instances, scale_instances

class TestBalancer(unittest.TestCase):

    @patch('load_balancer.balancer.get_current_load_distribution')
    @patch('load_balancer.balancer.send_request_to_instance')
    def test_distribute_requests(self, mock_send_request, mock_get_load_distribution):
        mock_get_load_distribution.return_value = {'instance_1': 5, 'instance_2': 3, 'instance_3': 8}

        request = {"data": "sample_request"}
        
        distribute_requests(request)
        
        mock_send_request.assert_called()
        # Check that all instances received requests and that they were distributed efficiently
        self.assertEqual(mock_send_request.call_count, 1)
        called_instances = [call[0][0] for call in mock_send_request.call_args_list]
        self.assertIn('instance_2', called_instances)  # Assuming instance_2 had the least load

    @patch('load_balancer.balancer.get_instances_status')
    @patch('load_balancer.balancer.update_instance_health')
    def test_monitor_instances(self, mock_update_health, mock_get_status):
        mock_get_status.return_value = {
            'instance_1': {'health': 'healthy', 'load': 5},
            'instance_2': {'health': 'unhealthy', 'load': 3},
            'instance_3': {'health': 'healthy', 'load': 8}
        }

        monitor_instances()
        
        mock_update_health.assert_called()
        # Verify that only healthy instances get status updated
        healthy_instances = [inst for inst in mock_get_status.return_value if mock_get_status.return_value[inst]['health'] == 'healthy']
        called_instances = [call[0][0] for call in mock_update_health.call_args_list]
        self.assertTrue(all(instance in healthy_instances for instance in called_instances), "Unhealthy instances should not be monitored.")

    @patch('load_balancer.balancer.get_total_load')
    @patch('load_balancer.balancer.trigger_scale_up')
    @patch('load_balancer.balancer.trigger_scale_down')
    def test_scale_instances(self, mock_scale_down, mock_scale_up, mock_get_total_load):
        mock_get_total_load.return_value = 15  # Setting a high load to simulate scale up necessity

        scale_instances()

        mock_scale_up.assert_called_once()
        mock_scale_down.assert_not_called()

        # Simulate a scenario where load is reduced, requiring scale down
        mock_get_total_load.return_value = 3

        scale_instances()

        mock_scale_down.assert_called_once()
        mock_scale_up.assert_not_called()

if __name__ == '__main__':
    unittest.main()
