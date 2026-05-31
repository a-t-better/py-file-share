"""Basic tests for PyFileShare"""

import unittest
import tempfile
from pathlib import Path
from pyfileshare.config import ServerConfig, ClientConfig, HTTPConfig, StorageConfig
from pyfileshare.core import FileTransfer, CryptoManager, StorageManager
from pyfileshare.core.utils import format_bytes, format_time


class TestConfiguration(unittest.TestCase):
    """Test configuration loading"""
    
    def test_server_config_defaults(self):
        """Test server config with defaults"""
        config = ServerConfig()
        self.assertEqual(config.http.port, 8080)
        self.assertEqual(config.storage.upload_dir, './uploads')
        self.assertTrue(config.auth.enabled)
    
    def test_client_config_defaults(self):
        """Test client config with defaults"""
        config = ClientConfig()
        self.assertEqual(config.default_server, 'http://localhost:8080')
        self.assertTrue(config.progress.show_progress)


class TestFileTransfer(unittest.TestCase):
    """Test file transfer functionality"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.transfer = FileTransfer(chunk_size=1024)
        self.temp_dir = tempfile.mkdtemp()
    
    def test_checksum_calculation(self):
        """Test checksum calculation"""
        # Create a test file
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text('Hello, World!')
        
        checksum = self.transfer.calculate_checksum(str(test_file), 'sha256')
        self.assertIsNotNone(checksum)
        self.assertEqual(len(checksum), 64)  # SHA256 hex digest length
    
    def test_checksum_verification(self):
        """Test checksum verification"""
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text('Test content')
        
        checksum = self.transfer.calculate_checksum(str(test_file), 'sha256')
        verified = self.transfer.verify_checksum(str(test_file), checksum, 'sha256')
        
        self.assertTrue(verified)
    
    def test_wrong_checksum_fails(self):
        """Test that wrong checksum fails verification"""
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text('Test content')
        
        wrong_checksum = 'wrong' * 16
        verified = self.transfer.verify_checksum(str(test_file), wrong_checksum, 'sha256')
        
        self.assertFalse(verified)


class TestCrypto(unittest.TestCase):
    """Test cryptography utilities"""
    
    def test_api_key_generation(self):
        """Test API key generation"""
        key1 = CryptoManager.generate_api_key()
        key2 = CryptoManager.generate_api_key()
        
        self.assertNotEqual(key1, key2)
        self.assertTrue(len(key1) > 0)
    
    def test_password_hashing(self):
        """Test password hashing"""
        password = "test_password"
        hashed, salt = CryptoManager.hash_password(password)
        
        self.assertIsNotNone(hashed)
        self.assertIsNotNone(salt)
    
    def test_password_verification(self):
        """Test password verification"""
        password = "test_password"
        hashed, salt = CryptoManager.hash_password(password)
        
        verified = CryptoManager.verify_password(password, hashed, salt)
        self.assertTrue(verified)
    
    def test_wrong_password_fails(self):
        """Test that wrong password fails verification"""
        password = "test_password"
        wrong_password = "wrong_password"
        hashed, salt = CryptoManager.hash_password(password)
        
        verified = CryptoManager.verify_password(wrong_password, hashed, salt)
        self.assertFalse(verified)


class TestStorage(unittest.TestCase):
    """Test storage management"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = StorageManager(self.temp_dir)
    
    def test_storage_initialization(self):
        """Test storage manager initialization"""
        self.assertTrue(Path(self.temp_dir).exists())
    
    def test_get_file_path(self):
        """Test getting file path"""
        file_path = self.storage.get_file_path('test.txt')
        self.assertIsInstance(file_path, Path)
    
    def test_file_list(self):
        """Test listing files"""
        # Create test files
        (Path(self.temp_dir) / 'file1.txt').write_text('content1')
        (Path(self.temp_dir) / 'file2.txt').write_text('content2')
        
        files = self.storage.list_files()
        self.assertEqual(len(files), 2)
    
    def test_delete_file(self):
        """Test file deletion"""
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text('content')
        
        self.assertTrue(test_file.exists())
        self.storage.delete_file(test_file)
        self.assertFalse(test_file.exists())


class TestUtilities(unittest.TestCase):
    """Test utility functions"""
    
    def test_format_bytes(self):
        """Test byte formatting"""
        self.assertEqual(format_bytes(512), "512.00 B")
        self.assertIn("KB", format_bytes(1024))
        self.assertIn("MB", format_bytes(1024 * 1024))
    
    def test_format_time(self):
        """Test time formatting"""
        self.assertIn("s", format_time(45))
        self.assertIn("m", format_time(125))
        self.assertIn("h", format_time(3725))


if __name__ == '__main__':
    unittest.main()
