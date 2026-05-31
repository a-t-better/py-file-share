"""Client usage example"""

from pyfileshare.config import ClientConfig
from pyfileshare.client import FileShareClient
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def progress_callback(processed, total, **kwargs):
    """Progress callback function"""
    percentage = (processed / total * 100) if total > 0 else 0
    print(f"\rProgress: {percentage:.1f}% ({processed}/{total})", end='', flush=True)

if __name__ == '__main__':
    config = ClientConfig.from_yaml('config/client.yaml')
    
    client = FileShareClient(config)
    
    print("PyFileShare Client Example")
    print("=" * 50)
    
    print("\n1. Checking server health...")
    try:
        health = client.health_check()
        print(f"   Server status: {health['status']}")
        print(f"   Available space: {health['available_space']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n2. Listing files on server...")
    try:
        files = client.list_files()
        print(f"   Found {files['count']} files:")
        for f in files['files'][:5]:
            print(f"     • {f}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n3. Upload example:")
    print("   client.upload('local_file.zip')")
    
    print("\n4. Download example:")
    print("   client.download('remote_file.zip', 'download_location')")
    
    print("\n5. Delete example:")
    print("   client.delete_file('filename.zip')")
    
    print("\n" + "=" * 50)
    print("Use CLI commands for actual file operations:")
    print("  pyfileshare client upload <file>")
    print("  pyfileshare client download <remote> <local>")
    print("  pyfileshare client list")
    print("  pyfileshare client delete <filename>")
