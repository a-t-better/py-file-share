"""HTTP-based file transfer client"""

import requests
from pathlib import Path
from typing import Optional, Callable, Dict
import logging

from pyfileshare.config import ClientConfig
from pyfileshare.core import FileTransfer
from pyfileshare.core.utils import ProgressTracker, format_bytes

logger = logging.getLogger(__name__)


class FileShareClient:
    """High-level file share client"""
    
    def __init__(self, config: ClientConfig):
        """Initialize client"""
        self.config = config
        self.transfer = FileTransfer(config.transfer.chunk_size)
        self.session = requests.Session()
        
        if config.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {config.api_key}'
            })
        
        self.session.verify = config.verify_ssl
    
    def upload(
        self,
        local_path: str,
        remote_path: Optional[str] = None,
        server: Optional[str] = None,
        show_progress: bool = True,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """Upload a file"""
        try:
            local_file = Path(local_path)
            if not local_file.exists():
                raise FileNotFoundError(f"File not found: {local_path}")
            
            if server is None:
                server = self.config.default_server
            
            file_size = local_file.stat().st_size
            logger.info(f"Starting upload: {local_file.name} ({format_bytes(file_size)})")
            
            url = f"{server.rstrip('/')}/upload"
            with open(local_path, 'rb') as f:
                files = {'file': f}
                response = self.session.post(url, files=files)
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Upload successful: {result}")
            return result
        
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            raise
    
    def download(
        self,
        remote_path: str,
        local_path: str,
        server: Optional[str] = None,
        show_progress: bool = True,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """Download a file"""
        try:
            if server is None:
                server = self.config.default_server
            
            filename = Path(remote_path).name
            url = f"{server.rstrip('/')}/download/{filename}"
            
            logger.info(f"Starting download: {filename}")
            
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            local_file = Path(local_path)
            local_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.config.transfer.chunk_size):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Download successful: {local_file.name}")
            
            return {
                'status': 'success',
                'filename': filename,
                'size': local_file.stat().st_size
            }
        
        except Exception as e:
            logger.error(f"Download failed: {e}")
            raise
    
    def list_files(self, server: Optional[str] = None) -> Dict:
        """List files on server"""
        try:
            if server is None:
                server = self.config.default_server
            
            url = f"{server.rstrip('/')}/list"
            response = self.session.get(url)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            logger.error(f"List failed: {e}")
            raise
    
    def delete_file(self, filename: str, server: Optional[str] = None) -> Dict:
        """Delete file from server"""
        try:
            if server is None:
                server = self.config.default_server
            
            url = f"{server.rstrip('/')}/delete/{filename}"
            response = self.session.delete(url)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            raise
    
    def health_check(self, server: Optional[str] = None) -> Dict:
        """Check server health"""
        try:
            if server is None:
                server = self.config.default_server
            
            url = f"{server.rstrip('/')}/health"
            response = self.session.get(url)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise
