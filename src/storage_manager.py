"""
Storage Manager - Abstraction layer for data storage
Supports both local file storage and Azure Blob Storage
"""

import json
import os
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

# Azure imports (will be None if not installed)
try:
    from azure.storage.blob import BlobServiceClient
    from azure.identity import DefaultAzureCredential
    from azure.core.exceptions import ResourceNotFoundError, ServiceRequestError

    AZURE_AVAILABLE = True
except ImportError:
    BlobServiceClient = None
    DefaultAzureCredential = None
    ResourceNotFoundError = None
    ServiceRequestError = None
    AZURE_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)


class StorageInterface(ABC):
    """Abstract interface for storage operations"""

    @abstractmethod
    def load_data(self, filename: str, default: Any = None) -> Any:
        """Load data from storage"""
        pass

    @abstractmethod
    def save_data(self, filename: str, data: Any) -> bool:
        """Save data to storage"""
        pass

    @abstractmethod
    def file_exists(self, filename: str) -> bool:
        """Check if file exists in storage"""
        pass

    @abstractmethod
    def list_files(self) -> list:
        """List all files in storage"""
        pass


class LocalFileStorage(StorageInterface):
    """Local file system storage implementation"""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        logger.info(f"Initialized local storage at: {data_dir}")

    def load_data(self, filename: str, default: Any = None) -> Any:
        """Load data from local JSON file"""
        if default is None:
            default = {}

        file_path = os.path.join(self.data_dir, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(f"Loaded data from {filename}")
                return data
        except FileNotFoundError:
            logger.info(f"File {filename} not found, returning default")
            return default
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filename}: {e}")
            return default
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            return default

    def save_data(self, filename: str, data: Any) -> bool:
        """Save data to local JSON file"""
        file_path = os.path.join(self.data_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)
            logger.debug(f"Saved data to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving {filename}: {e}")
            return False

    def file_exists(self, filename: str) -> bool:
        """Check if file exists locally"""
        file_path = os.path.join(self.data_dir, filename)
        return os.path.exists(file_path)

    def list_files(self) -> list:
        """List all JSON files in local directory"""
        try:
            files = [f for f in os.listdir(self.data_dir) if f.endswith(".json")]
            return sorted(files)
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []


class AzureBlobStorage(StorageInterface):
    """Azure Blob Storage implementation"""

    def __init__(self, account_name: str, container_name: str = "leaveapp-data"):
        if not AZURE_AVAILABLE:
            raise ImportError(
                "Azure Storage libraries not available. Install with: pip install azure-storage-blob azure-identity"
            )

        self.account_name = account_name
        self.container_name = container_name
        self.account_url = f"https://{account_name}.blob.core.windows.net"

        # Use DefaultAzureCredential for authentication
        # This supports Managed Identity, Azure CLI, Environment variables, etc.
        try:
            credential = DefaultAzureCredential()
            self.blob_service_client = BlobServiceClient(account_url=self.account_url, credential=credential)

            # Ensure container exists
            self._ensure_container_exists()
            logger.info(f"Initialized Azure Blob storage: {account_name}/{container_name}")

        except Exception as e:
            logger.error(f"Failed to initialize Azure Blob Storage: {e}")
            raise

    def _ensure_container_exists(self):
        """Ensure the container exists, create if it doesn't"""
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            container_client.get_container_properties()
            logger.debug(f"Container {self.container_name} exists")
        except ResourceNotFoundError:
            try:
                container_client.create_container()
                logger.info(f"Created container {self.container_name}")
            except Exception as e:
                logger.error(f"Failed to create container {self.container_name}: {e}")
                raise
        except Exception as e:
            logger.error(f"Error checking container {self.container_name}: {e}")
            raise

    def load_data(self, filename: str, default: Any = None) -> Any:
        """Load data from Azure Blob Storage"""
        if default is None:
            default = {}

        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=filename)

            blob_data = blob_client.download_blob()
            content = blob_data.readall().decode("utf-8")
            data = json.loads(content)
            logger.debug(f"Loaded data from blob {filename}")
            return data

        except ResourceNotFoundError:
            logger.info(f"Blob {filename} not found, returning default")
            return default
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in blob {filename}: {e}")
            return default
        except Exception as e:
            logger.error(f"Error loading blob {filename}: {e}")
            return default

    def save_data(self, filename: str, data: Any) -> bool:
        """Save data to Azure Blob Storage"""
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=filename)

            json_content = json.dumps(data, indent=2, default=str, ensure_ascii=False)
            blob_client.upload_blob(
                data=json_content.encode("utf-8"),
                overwrite=True,
                content_settings={"content_type": "application/json", "content_encoding": "utf-8"},
            )
            logger.debug(f"Saved data to blob {filename}")
            return True

        except Exception as e:
            logger.error(f"Error saving blob {filename}: {e}")
            return False

    def file_exists(self, filename: str) -> bool:
        """Check if blob exists in Azure Storage"""
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=filename)
            blob_client.get_blob_properties()
            return True
        except ResourceNotFoundError:
            return False
        except Exception as e:
            logger.error(f"Error checking blob {filename}: {e}")
            return False

    def list_files(self) -> list:
        """List all blobs in container"""
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blobs = container_client.list_blobs()
            files = [blob.name for blob in blobs if blob.name.endswith(".json")]
            return sorted(files)
        except Exception as e:
            logger.error(f"Error listing blobs: {e}")
            return []


class StorageManager:
    """Storage manager that provides unified interface for both local and cloud storage"""

    def __init__(self):
        self.storage: Optional[StorageInterface] = None
        self._initialize_storage()

    def _initialize_storage(self):
        """Initialize storage based on environment configuration"""
        storage_type = os.getenv("STORAGE_TYPE", "local").lower()

        if storage_type == "azure":
            # Azure Blob Storage configuration
            account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
            container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "leaveapp-data")

            if not account_name:
                logger.error("AZURE_STORAGE_ACCOUNT_NAME environment variable is required for Azure storage")
                raise ValueError("Azure storage account name not configured")

            try:
                self.storage = AzureBlobStorage(account_name, container_name)
                logger.info("Using Azure Blob Storage")
            except Exception as e:
                logger.error(f"Failed to initialize Azure storage: {e}")
                logger.info("Falling back to local storage")
                self._initialize_local_storage()

        else:
            # Local file storage (default)
            self._initialize_local_storage()

    def _initialize_local_storage(self):
        """Initialize local file storage"""
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, "data")

        self.storage = LocalFileStorage(data_dir)
        logger.info("Using local file storage")

    def load_data(self, filename: str, default: Any = None) -> Any:
        """Load data using the configured storage"""
        return self.storage.load_data(filename, default)

    def save_data(self, filename: str, data: Any) -> bool:
        """Save data using the configured storage"""
        return self.storage.save_data(filename, data)

    def file_exists(self, filename: str) -> bool:
        """Check if file exists using the configured storage"""
        return self.storage.file_exists(filename)

    def list_files(self) -> list:
        """List files using the configured storage"""
        return self.storage.list_files()

    def get_storage_info(self) -> Dict[str, Any]:
        """Get information about the current storage configuration"""
        storage_type = "Azure Blob Storage" if isinstance(self.storage, AzureBlobStorage) else "Local File Storage"

        info = {"type": storage_type, "timestamp": datetime.now().isoformat()}

        if isinstance(self.storage, AzureBlobStorage):
            info.update({"account_name": self.storage.account_name, "container_name": self.storage.container_name})
        elif isinstance(self.storage, LocalFileStorage):
            info.update({"data_directory": self.storage.data_dir})

        return info


# Global storage manager instance
storage_manager = StorageManager()
