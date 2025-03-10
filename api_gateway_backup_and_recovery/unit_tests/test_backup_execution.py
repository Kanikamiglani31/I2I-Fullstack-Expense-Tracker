# api_gateway_backup_and_recovery/unit_tests/test_backup_execution.py

import unittest
from unittest.mock import patch, MagicMock
from api_gateway_backup_and_recovery.backup_execution import execute_backup

class TestBackupExecution(unittest.TestCase):

    @patch('api_gateway_backup_and_recovery.backup_execution.configure_backup')
    @patch('api_gateway_backup_and_recovery.backup_execution.log_backup_activity')
    def test_execute_backup_success(self, mock_log_backup_activity, mock_configure_backup):
        """
        Tests successful execution of the backup process ensuring all files are backed up.
        """
        backup_config = {
            'interval': 'daily',
            'retention_period': '7 days',
            'backup_location': '/backups'
        }
        
        mock_configure_backup.return_value = backup_config
        mock_log_backup_activity.return_value = None
        
        result = execute_backup()
        
        self.assertTrue(result)
        mock_log_backup_activity.assert_called_with('Backup completed successfully')
        mock_configure_backup.assert_called_once()

    @patch('api_gateway_backup_and_recovery.backup_execution.configure_backup')
    @patch('api_gateway_backup_and_recovery.backup_execution.log_backup_activity')
    def test_execute_backup_failure(self, mock_log_backup_activity, mock_configure_backup):
        """
        Tests failure scenarios during the backup process ensuring proper handling and notifications.
        """
        backup_config = {
            'interval': 'daily',
            'retention_period': '7 days',
            'backup_location': '/invalid_path'
        }
        
        mock_configure_backup.return_value = backup_config
        mock_log_backup_activity.return_value = None
        
        with self.assertRaises(Exception):
            execute_backup()
        
        mock_log_backup_activity.assert_called_with('Backup failed')
        mock_configure_backup.assert_called_once()

if __name__ == '__main__':
    unittest.main()
