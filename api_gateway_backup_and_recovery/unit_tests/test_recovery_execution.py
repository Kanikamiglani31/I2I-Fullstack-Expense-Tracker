import unittest
from unittest.mock import patch
from api_gateway_backup_and_recovery.recovery_execution import execute_recovery
from api_gateway_backup_and_recovery.logging import log_recovery_activity

class TestRecoveryExecution(unittest.TestCase):

    @patch('api_gateway_backup_and_recovery.recovery_execution.log_recovery_activity')
    @patch('api_gateway_backup_and_recovery.recovery_execution.restore_backup')
    @patch('api_gateway_backup_and_recovery.recovery_execution.get_recovery_configuration')
    def test_execute_recovery_success(self, mock_get_recovery_configuration, mock_restore_backup, mock_log_recovery_activity):
        # Setup mock responses
        mock_get_recovery_configuration.return_value = {
            'recovery_location': '/backup/location',
            'recovery_strategy': 'FULL'
        }
        mock_restore_backup.return_value = True

        # Execute recovery
        result = execute_recovery()

        # Validations
        self.assertTrue(result)
        mock_get_recovery_configuration.assert_called_once()
        mock_restore_backup.assert_called_once_with('/backup/location', 'FULL')
        mock_log_recovery_activity.assert_any_call('Recovery process started.')
        mock_log_recovery_activity.assert_any_call('Recovery process completed successfully.')

    @patch('api_gateway_backup_and_recovery.recovery_execution.log_recovery_activity')
    @patch('api_gateway_backup_and_recovery.recovery_execution.restore_backup')
    @patch('api_gateway_backup_and_recovery.recovery_execution.get_recovery_configuration')
    def test_execute_recovery_failure(self, mock_get_recovery_configuration, mock_restore_backup, mock_log_recovery_activity):
        # Setup mock responses
        mock_get_recovery_configuration.return_value = {
            'recovery_location': '/backup/location',
            'recovery_strategy': 'FULL'
        }
        mock_restore_backup.side_effect = Exception("Recovery failed due to some issue")

        # Execute recovery
        result = execute_recovery()

        # Validations
        self.assertFalse(result)
        mock_get_recovery_configuration.assert_called_once()
        mock_restore_backup.assert_called_once_with('/backup/location', 'FULL')
        mock_log_recovery_activity.assert_any_call('Recovery process started.')
        mock_log_recovery_activity.assert_any_call('Recovery process failed: Recovery failed due to some issue.')

if __name__ == '__main__':
    unittest.main()
