"""Batch transfer operations"""

import os
from pathlib import Path
from typing import List, Dict, Optional, Callable
import logging

from pyfileshare.client import FileShareClient
from pyfileshare.core.utils import format_bytes

logger = logging.getLogger(__name__)


class BatchTransfer:
    """Batch file transfer operations"""
    
    def __init__(self, client: FileShareClient):
        """Initialize batch transfer"""
        self.client = client
        self.total_transferred = 0
        self.transfer_count = 0
        self.failed_count = 0
    
    def batch_upload(
        self,
        local_paths: List[str],
        server: Optional[str] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """Upload multiple files
        
        Args:
            local_paths: List of local file paths
            server: Server URL
            progress_callback: Progress callback function
            
        Returns:
            Dictionary with batch upload results
        """
        results = {
            'total_files': len(local_paths),
            'successful': 0,
            'failed': 0,
            'total_size': 0,
            'details': []
        }
        
        for idx, local_path in enumerate(local_paths):
            try:
                file_path = Path(local_path)
                if not file_path.exists():
                    logger.warning(f"File not found: {local_path}")
                    results['failed'] += 1
                    results['details'].append({
                        'file': local_path,
                        'status': 'error',
                        'message': 'File not found'
                    })
                    continue
                
                file_size = file_path.stat().st_size
                
                logger.info(f"Uploading [{idx + 1}/{len(local_paths)}]: {file_path.name}")
                
                result = self.client.upload(
                    local_path,
                    server=server,
                    show_progress=True,
                    progress_callback=progress_callback
                )
                
                if result.get('status') == 'success':
                    results['successful'] += 1
                    results['total_size'] += file_size
                    results['details'].append({
                        'file': file_path.name,
                        'size': file_size,
                        'status': 'success'
                    })
                    logger.info(f"✓ Upload successful: {file_path.name}")
                else:
                    results['failed'] += 1
                    results['details'].append({
                        'file': file_path.name,
                        'status': 'error',
                        'message': result.get('error', 'Unknown error')
                    })
                    logger.error(f"✗ Upload failed: {file_path.name}")
            
            except Exception as e:
                logger.error(f"Upload error: {e}")
                results['failed'] += 1
                results['details'].append({
                    'file': local_path,
                    'status': 'error',
                    'message': str(e)
                })
        
        logger.info(f"\nBatch upload completed: {results['successful']}/{len(local_paths)} successful")
        logger.info(f"Total size transferred: {format_bytes(results['total_size'])}")
        
        return results
    
    def batch_download(
        self,
        remote_files: List[str],
        local_dir: str,
        server: Optional[str] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """Download multiple files
        
        Args:
            remote_files: List of remote file paths
            local_dir: Local directory to save files
            server: Server URL
            progress_callback: Progress callback function
            
        Returns:
            Dictionary with batch download results
        """
        results = {
            'total_files': len(remote_files),
            'successful': 0,
            'failed': 0,
            'total_size': 0,
            'details': []
        }
        
        # Create local directory
        local_path = Path(local_dir)
        local_path.mkdir(parents=True, exist_ok=True)
        
        for idx, remote_file in enumerate(remote_files):
            try:
                filename = Path(remote_file).name
                local_file_path = local_path / filename
                
                logger.info(f"Downloading [{idx + 1}/{len(remote_files)}]: {filename}")
                
                result = self.client.download(
                    remote_file,
                    str(local_file_path),
                    server=server,
                    show_progress=True,
                    progress_callback=progress_callback
                )
                
                if result.get('status') == 'success':
                    file_size = result.get('size', 0)
                    results['successful'] += 1
                    results['total_size'] += file_size
                    results['details'].append({
                        'file': filename,
                        'size': file_size,
                        'status': 'success'
                    })
                    logger.info(f"✓ Download successful: {filename}")
                else:
                    results['failed'] += 1
                    results['details'].append({
                        'file': filename,
                        'status': 'error',
                        'message': result.get('error', 'Unknown error')
                    })
                    logger.error(f"✗ Download failed: {filename}")
            
            except Exception as e:
                logger.error(f"Download error: {e}")
                results['failed'] += 1
                results['details'].append({
                    'file': remote_file,
                    'status': 'error',
                    'message': str(e)
                })
        
        logger.info(f"\nBatch download completed: {results['successful']}/{len(remote_files)} successful")
        logger.info(f"Total size transferred: {format_bytes(results['total_size'])}")
        
        return results
    
    def batch_delete(
        self,
        remote_files: List[str],
        server: Optional[str] = None
    ) -> Dict:
        """Delete multiple files
        
        Args:
            remote_files: List of filenames to delete
            server: Server URL
            
        Returns:
            Dictionary with batch delete results
        """
        results = {
            'total_files': len(remote_files),
            'successful': 0,
            'failed': 0,
            'details': []
        }
        
        for idx, filename in enumerate(remote_files):
            try:
                logger.info(f"Deleting [{idx + 1}/{len(remote_files)}]: {filename}")
                
                result = self.client.delete_file(filename, server=server)
                
                if result.get('status') == 'success':
                    results['successful'] += 1
                    results['details'].append({
                        'file': filename,
                        'status': 'success'
                    })
                    logger.info(f"✓ Delete successful: {filename}")
                else:
                    results['failed'] += 1
                    results['details'].append({
                        'file': filename,
                        'status': 'error',
                        'message': result.get('error', 'Unknown error')
                    })
                    logger.error(f"✗ Delete failed: {filename}")
            
            except Exception as e:
                logger.error(f"Delete error: {e}")
                results['failed'] += 1
                results['details'].append({
                    'file': filename,
                    'status': 'error',
                    'message': str(e)
                })
        
        logger.info(f"\nBatch delete completed: {results['successful']}/{len(remote_files)} successful")
        
        return results
    
    def upload_directory(
        self,
        local_dir: str,
        server: Optional[str] = None,
        recursive: bool = True,
        pattern: Optional[str] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """Upload all files in a directory
        
        Args:
            local_dir: Local directory path
            server: Server URL
            recursive: Whether to upload subdirectories
            pattern: Optional file pattern (e.g., '*.zip')
            progress_callback: Progress callback function
            
        Returns:
            Dictionary with upload results
        """
        dir_path = Path(local_dir)
        
        if not dir_path.exists():
            return {'status': 'error', 'message': f'Directory not found: {local_dir}'}
        
        # Find all files
        if recursive:
            glob_pattern = f'**/{pattern}' if pattern else '**/*'
            files = [str(f) for f in dir_path.glob(glob_pattern) if f.is_file()]
        else:
            glob_pattern = pattern if pattern else '*'
            files = [str(f) for f in dir_path.glob(glob_pattern) if f.is_file()]
        
        logger.info(f"Found {len(files)} files to upload from {local_dir}")
        
        return self.batch_upload(files, server, progress_callback)
