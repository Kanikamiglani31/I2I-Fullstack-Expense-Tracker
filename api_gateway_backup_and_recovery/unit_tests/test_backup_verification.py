import unittest
from unittest.mock import patch, MagicMock
from api_gateway_backup_and_recovery.backup_verification import verify_backup


class TestBackupVerification(unittest.TestCase):

    @patch('api_gateway_backup_and_recovery.backup_verification.os.path.exists')
    @patch('api_gateway_backup_and_recovery.backup_verification.os.path.getsize')
    def test_verify_backup_success(self, mock_getsize, mock_exists):
        # Mocking os.path.exists to always return True and os.path.getsize to return a non-zero size.
        mock_exists.return_value = True
        mock_getsize.return_value = 1024  # Assume all backup files are 1KB or larger

        backup_location = '/mock/backup/location'
        files_to_verify = ['file1', 'file2', 'file3']

        result = verify_backup(backup_location, files_to_verify)
        self.assertTrue(result)

    @patch('api_gateway_backup_and_recovery.backup_verification.os.path.exists')
    @patch('api_gateway_backup_and_recovery.backup_verification.os.path.getsize')
    def test_verify_backup_failure(self, mock_getsize, mock_exists):
        # Mocking os.path.exists to return True for some files and False for others.
        mock_exists.side_effect = lambda path: path.endswith('file2')
        # Mocking os.path.getsize to return zero size for incomplete/corrupted files.
        mock_getsize.side_effect = lambda path: 1024 if path.endswith('file2') else 0

        backup_location = '/mock/backup/location'
        files_to_verify = ['file1', 'file2', 'file3']

        result = verify_backup(backup_location, files_to_verify)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
