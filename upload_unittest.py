import unittest
from unittest.mock import patch, MagicMock
from ankit_filesupload import UploadFile

class TestUploadFiles(unittest.TestCase):
    """
    Test cases for upload_files method
    """
    @patch('os.walk')
    @patch('os.path.join')
    @patch('boto3.resource')
    def test_upload_files(self, mock_boto3, mock_os_path_join, mock_os_walk):
        # Arrange
        mock_s3 = MagicMock()
        mock_bucket = MagicMock()
        mock_s3.Bucket.return_value = mock_bucket
        mock_boto3.return_value = mock_s3
        mock_os_walk.return_value = [
            ('root', 'dirs', ['file1', 'file2']),
        ]
        mock_os_path_join.side_effect = lambda *args: '/'.join(args)
        uploader = UploadFile('mock_folder')

        # Act
        uploader.upload_files()

        # Assert
        mock_os_walk.assert_called_once_with(uploader.local_folder)
        mock_os_path_join.assert_any_call('root', 'file1')
        mock_os_path_join.assert_any_call('root', 'file2')
        print(mock_bucket.upload_file.call_args_list)
        mock_bucket.upload_file.assert_any_call('root/file1', 'assignment1//root/file1')
        mock_bucket.upload_file.assert_any_call('root/file2', 'assignmenet1//root/file2')

    @patch('os.walk')
    @patch('os.path.join')
    @patch('boto3.resource')
    def test_upload_files_exception(self, mock_boto3, mock_os_path_join, mock_os_walk):
        """
        Test case to check if the method exits on exception
        """
        # Arrange
        mock_s3 = MagicMock()
        mock_bucket = MagicMock()
        mock_s3.Bucket.return_value = mock_bucket
        mock_boto3.return_value = mock_s3
        mock_os_walk.return_value = [
            ('root', 'dirs', ['file1', 'file2']),
        ]
        mock_os_path_join.side_effect = lambda *args: '/'.join(args)
        
        mock_bucket.upload_file.side_effect = Exception('Test exception')
        uploader = UploadFile('mock_folder')

        # Act
        with self.assertRaises(SystemExit) as cm:
            uploader.upload_files()

        # Assert
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()