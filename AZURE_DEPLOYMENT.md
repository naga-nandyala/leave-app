# Azure Deployment Guide for Leave App

This guide provides step-by-step instructions to deploy your Flask Leave Management application to Azure App Service using Azure CLI.

## Prerequisites

1. **Azure CLI**: Install from [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
2. **Azure Subscription**: Active Azure subscription with sufficient quota
3. **Git**: For version control (optional)

## Deployment Options

### Option 1: PowerShell Script (Windows)

```powershell
# Make script executable and run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deploy-azure.ps1
```

**With custom parameters:**
```powershell
.\deploy-azure.ps1 -ResourceGroupName "my-rg" -Location "westus2" -WebAppName "my-leave-app"
```

### Option 2: Bash Script (Linux/Mac)

```bash
# Make script executable
chmod +x deploy-azure.sh

# Run with default settings
./deploy-azure.sh

# Run with custom parameters
./deploy-azure.sh --resource-group "my-rg" --location "westus2" --app-name "my-leave-app"
```

### Option 3: Manual Azure CLI Commands

If you prefer to run commands manually, follow these steps:

#### 1. Login to Azure
```bash
az login
```

#### 2. Set Variables
```bash
# Bash/Linux
RESOURCE_GROUP="rg-leave-app-prod"
LOCATION="eastus"
APP_SERVICE_PLAN="asp-leave-app-prod"
WEB_APP_NAME="leave-app-$(shuf -i 1000-9999 -n 1)"
```

```powershell
# PowerShell
$RESOURCE_GROUP = "rg-leave-app-prod"
$LOCATION = "eastus"
$APP_SERVICE_PLAN = "asp-leave-app-prod"
$WEB_APP_NAME = "leave-app-$(Get-Random -Minimum 1000 -Maximum 9999)"
```

#### 3. Create Resource Group
```bash
az group create --name $RESOURCE_GROUP --location $LOCATION
```

#### 4. Create App Service Plan
```bash
# Try Basic tier first
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# If quota issues, use Free tier
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku F1 --is-linux
```

#### 5. Create Web App
```bash
az webapp create \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --runtime "PYTHON|3.12"
```

#### 6. Configure App Settings
```bash
az webapp config appsettings set \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    FLASK_APP=app \
    FLASK_ENV=production \
    SECRET_KEY="your-secret-key-here" \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true \
    WEBSITES_ENABLE_APP_SERVICE_STORAGE=false
```

#### 7. Configure Startup Command
```bash
az webapp config set \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
```

#### 8. Enable HTTPS Only
```bash
az webapp update \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --https-only true
```

#### 9. Deploy Application
```bash
# Navigate to src directory
cd src

# Deploy using zip
az webapp deployment source config-zip \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --src .
```

#### 10. Restart Web App
```bash
az webapp restart --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP
```

## Post-Deployment

### Check Application Status
```bash
# View application URL
az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query "defaultHostName" -o tsv

# Check deployment logs
az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP

# View application logs
az webapp log download --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP
```

### Access Your Application
Your application will be available at: `https://your-app-name.azurewebsites.net`

## Troubleshooting

### Common Issues

1. **Quota Exceeded**: Try different Azure regions or use Free tier instead of Basic
2. **Deployment Failed**: Check logs using `az webapp log tail`
3. **App Not Starting**: Verify startup command and check application logs

### Useful Commands

```bash
# Check quota usage
az vm list-usage --location eastus

# List available locations
az account list-locations --query "[].name" -o table

# View app service logs
az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP

# SSH into the container (for debugging)
az webapp ssh --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP
```

## Configuration Options

### Environment Variables
The deployment sets the following environment variables:
- `FLASK_APP=app`
- `FLASK_ENV=production`
- `SECRET_KEY=[auto-generated]`
- `SCM_DO_BUILD_DURING_DEPLOYMENT=true`
- `WEBSITES_ENABLE_APP_SERVICE_STORAGE=false`

### Scaling
To scale your application:
```bash
# Scale up (change tier)
az appservice plan update --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku S1

# Scale out (add instances)
az appservice plan update --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --number-of-workers 2
```

## Security Considerations

1. **HTTPS Only**: Automatically enabled in deployment
2. **Secret Key**: Auto-generated secure key
3. **Environment Variables**: Sensitive data stored as app settings
4. **Access Restrictions**: Consider adding IP restrictions if needed

## Cost Management

- **Free Tier**: Limited to 60 CPU minutes per day
- **Basic Tier**: ~$13-55/month depending on size
- **Standard Tier**: ~$75-300/month with additional features

## Cleanup

To remove all resources:
```bash
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

## Support

For issues with:
- **Azure CLI**: [Azure CLI Documentation](https://docs.microsoft.com/en-us/cli/azure/)
- **App Service**: [App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- **Python on Azure**: [Python on Azure Documentation](https://docs.microsoft.com/en-us/azure/developer/python/)
