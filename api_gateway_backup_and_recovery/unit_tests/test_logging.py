import unittest
from unittest.mock import patch, Mock
from api_gateway_backup_and_recovery.logging import initialize_logging, log_backup_activity, log_recovery_activity


class TestLogging(unittest.TestCase):

    @patch('api_gateway_backup_and_recovery.logging.logging')
    def test_initialize_logging(self, mock_logging):
        # Test setup of the logging system
        initialize_logging()
        mock_logging.basicConfig.assert_called_once_with(
            filename='backup_recovery.log',
            level=mock_logging.INFO,
            format='%(asctime)s:%(levelname)s:%(message)s'
        )

    @patch('api_gateway_backup_and_recovery.logging.logging')
    def test_log_backup_activity(self, mock_logging):
        # Test logging during the backup process
        activity = "Backup completed successfully"
        log_backup_activity(activity)
        mock_logging.info.assert_called_once_with(f"BACKUP: {activity}")

    @patch('api_gateway_backup_and_recovery.logging.logging')
    def test_log_recovery_activity(self, mock_logging):
        # Test logging during the recovery process
        activity = "Recovery completed successfully"
        log_recovery_activity(activity)
        mock_logging.info.assert_called_once_with(f"RECOVERY: {activity}")


if __name__ == '__main__':
    unittest.main()
