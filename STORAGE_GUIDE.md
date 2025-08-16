# Leave Management App - Storage Configuration Guide

## Overview

This application now supports both local file storage and Azure Blob Storage for data persistence. You can easily switch between the two based on your deployment environment.

## Storage Options

### 1. Local File Storage (Default)
- Stores data in local JSON files in the `src/data/` directory
- Perfect for development and testing
- No cloud dependencies

### 2. Azure Blob Storage
- Stores data in Azure Blob Storage containers
- Recommended for production deployments
- Provides cloud-native scalability and reliability

## Configuration

### Environment Variables

The application uses environment variables to configure storage. Create a `.env` file in the root directory:

```bash
# Copy the example file
cp .env.example .env
```

### Local Storage Configuration

```env
STORAGE_TYPE=local
SECRET_KEY=your-secret-key-change-this-in-production
```

### Azure Storage Configuration

```env
STORAGE_TYPE=azure
AZURE_STORAGE_ACCOUNT_NAME=yourstorageaccountname
AZURE_STORAGE_CONTAINER_NAME=leaveapp-data
SECRET_KEY=your-secret-key-change-this-in-production
```

## Azure Setup

### Prerequisites
1. Azure subscription
2. Azure Storage Account
3. Proper authentication configured

### 1. Create Azure Storage Account

```bash
# Using Azure CLI
az storage account create \
  --name yourstorageaccountname \
  --resource-group your-resource-group \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2
```

### 2. Authentication Options

The application uses `DefaultAzureCredential` which supports multiple authentication methods:

#### For Local Development:
```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login to Azure
az login
```

#### For Production (Managed Identity - Recommended):
```bash
# Enable system-assigned managed identity for your App Service
az webapp identity assign --name your-app-name --resource-group your-resource-group

# Grant Storage Blob Data Contributor role to the managed identity
az role assignment create \
  --assignee <managed-identity-principal-id> \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>"
```

#### For CI/CD (Service Principal):
```env
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id
```

## Installation and Setup

### 1. Install Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r src/requirements.txt
```

### 2. Run the Application

```bash
cd src
python app.py
```

## Data Migration

Use the migration utility to move data between local and Azure storage:

### Migrate from Local to Azure
```bash
python migrate_data.py local-to-azure --azure-account yourstorageaccountname
```

### Migrate from Azure to Local
```bash
python migrate_data.py azure-to-local --azure-account yourstorageaccountname
```

### List Files in Storage
```bash
# List local files
python migrate_data.py list local

# List Azure files
python migrate_data.py list azure --azure-account yourstorageaccountname
```

## API Endpoints

### Check Storage Configuration
```bash
curl http://localhost:5000/api/storage_info
```

Returns information about the currently configured storage backend.

## Troubleshooting

### Common Issues

#### 1. Azure Authentication Errors
```
DefaultAzureCredential failed to retrieve a token
```

**Solutions:**
- Ensure you're logged in with `az login` for local development
- Verify managed identity is properly configured for production
- Check that environment variables are set correctly for service principal auth

#### 2. Storage Account Access Issues
```
This request is not authorized to perform this operation
```

**Solutions:**
- Verify the identity has "Storage Blob Data Contributor" role
- Check that the storage account name is correct
- Ensure the container exists or the app has permissions to create it

#### 3. Network Connectivity Issues
```
Name or service not known
```

**Solutions:**
- Verify the storage account name is correct
- Check network connectivity to Azure
- Ensure no firewall rules are blocking access

### Debug Mode

Enable debug logging by setting:
```env
PYTHONPATH=.
FLASK_ENV=development
FLASK_DEBUG=1
```

### Testing Storage Configuration

```bash
# Test with local storage
STORAGE_TYPE=local python -c "from src.storage_manager import storage_manager; print(storage_manager.get_storage_info())"

# Test with Azure storage
STORAGE_TYPE=azure AZURE_STORAGE_ACCOUNT_NAME=yourstorageaccountname python -c "from src.storage_manager import storage_manager; print(storage_manager.get_storage_info())"
```

## Security Considerations

1. **Never hardcode credentials** in your code
2. **Use Managed Identity** in production when possible
3. **Rotate secrets regularly** when using service principal authentication
4. **Enable encryption** at rest and in transit (enabled by default in Azure Storage)
5. **Monitor access logs** for suspicious activity
6. **Use least privilege** access principles

## Performance Tips

1. **Connection pooling** is handled automatically by the Azure SDK
2. **Retry logic** with exponential backoff is built into the storage manager
3. **Consider batch operations** for multiple file operations
4. **Monitor costs** - frequent small operations can be expensive

## Backup and Recovery

### Local Storage Backup
```bash
# Create backup
cp -r src/data src/data.backup.$(date +%Y%m%d)
```

### Azure Storage Backup
Azure Blob Storage provides:
- **Soft delete** for accidental deletions
- **Point-in-time restore** for containers
- **Cross-region replication** options
- **Versioning** for blob objects

Configure these features in the Azure portal for production deployments.
