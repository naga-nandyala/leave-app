# Azure CLI Deployment Script for Leave App
# This script deploys a Flask web application to Azure App Service

param(
    [string]$ResourceGroupName = "rg-leave-app",
    [string]$Location = "australiaeast",
    [string]$AppServicePlanName = "asp-leave-app1",
    [string]$WebAppName = "",
    [string]$SubscriptionId = "",
    [string]$FlaskSecretKey = ""
)

# Color functions for better output
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }

Write-Info "========================================"
Write-Info "Azure CLI Deployment Script for Leave App"
Write-Info "========================================"

# Check if Azure CLI is installed
Write-Info "Checking Azure CLI installation..."
try {
    $azVersion = az version --output json | ConvertFrom-Json | Select-Object -ExpandProperty "azure-cli"
    Write-Success "Azure CLI version: $azVersion"
} catch {
    Write-Error "Azure CLI is not installed. Please install it from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
}

# Check if user is logged in
Write-Info "Checking Azure authentication..."
try {
    $account = az account show --output json | ConvertFrom-Json
    Write-Success "Logged in as: $($account.user.name)"
    Write-Success "Subscription: $($account.name) ($($account.id))"
    
    if ($SubscriptionId -and $account.id -ne $SubscriptionId) {
        Write-Warning "Setting subscription to: $SubscriptionId"
        az account set --subscription $SubscriptionId
    }
} catch {
    Write-Error "Not logged in to Azure. Please run: az login"
    exit 1
}

# Generate unique web app name if not provided
if ([string]::IsNullOrEmpty($WebAppName)) {
    $randomSuffix = Get-Random -Minimum 1000 -Maximum 9999
    $WebAppName = "leave-app-$randomSuffix"
}

# Generate secret key if not provided
if ([string]::IsNullOrEmpty($FlaskSecretKey)) {
    $FlaskSecretKey = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((New-Guid).ToString()))
}

Write-Info "Deployment Configuration:"
Write-Info "Resource Group: $ResourceGroupName"
Write-Info "Location: $Location"
Write-Info "App Service Plan: $AppServicePlanName"
Write-Info "Web App Name: $WebAppName"
Write-Info "Flask Secret Key: [HIDDEN]"

# # Prompt for confirmation
# $confirmation = Read-Host "Do you want to proceed with the deployment? (y/N)"
# if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
#     Write-Warning "Deployment cancelled."
#     exit 0
# }

Write-Info "Starting deployment..."

# Step 1: Create Resource Group
Write-Info "Step 1: Creating resource group..."
$rgResult = az group create --name $ResourceGroupName --location $Location --output json | ConvertFrom-Json
if ($rgResult.properties.provisioningState -eq "Succeeded") {
    Write-Success "Resource group created successfully."
} else {
    Write-Error "Failed to create resource group."
    exit 1
}

# Step 2: Create App Service Plan
Write-Info "Step 2: Creating App Service Plan..."

# Try with Free tier first (F1) since Basic tier requires quota
Write-Info "Creating App Service Plan with Free tier (F1)..."
try {
    $planResult = az appservice plan create `
        --name $AppServicePlanName `
        --resource-group $ResourceGroupName `
        --sku B1 `
        --is-linux `
        --output json 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Free tier failed, trying Basic tier (B1)..."
        $planResult = az appservice plan create `
            --name $AppServicePlanName `
            --resource-group $ResourceGroupName `
            --sku B1 `
            --is-linux `
            --output json 2>&1
    }
    
    if ($LASTEXITCODE -eq 0) {
        $planResult = $planResult | ConvertFrom-Json
        Write-Success "App Service Plan created successfully."
    } else {
        Write-Error "Failed to create App Service Plan. Error: $planResult"
        Write-Error "This might be due to quota limitations. Please check your Azure subscription quota."
        exit 1
    }
} catch {
    Write-Error "Failed to create App Service Plan: $($_.Exception.Message)"
    Write-Error "Please check your Azure subscription quota and try again."
    exit 1
}

# Step 3: Create Web App
Write-Info "Step 3: Creating Web App..."
try {
    $webappResult = az webapp create `
        --name $WebAppName `
        --resource-group $ResourceGroupName `
        --plan $AppServicePlanName `
        --runtime "PYTHON:3.12" `
        --output json 2>&1

    if ($LASTEXITCODE -eq 0) {
        $webappResultJson = $webappResult | ConvertFrom-Json
        Write-Success "Web App created successfully."
        $appUrl = "https://$($webappResultJson.defaultHostName)"
        Write-Success "App URL: $appUrl"
    } else {
        Write-Error "Failed to create Web App. Error: $webappResult"
        exit 1
    }
} catch {
    Write-Error "Failed to create Web App: $($_.Exception.Message)"
    exit 1
}

# Step 4: Configure App Settings
Write-Info "Step 4: Configuring application settings..."
$appSettings = @(
    "FLASK_APP=app",
    "FLASK_ENV=production",
    "SECRET_KEY=$FlaskSecretKey",
    "SCM_DO_BUILD_DURING_DEPLOYMENT=true",
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE=false"
)

az webapp config appsettings set `
    --name $WebAppName `
    --resource-group $ResourceGroupName `
    --settings $appSettings `
    --output none

Write-Success "Application settings configured."

# Step 5: Configure startup command
Write-Info "Step 5: Configuring startup command..."
az webapp config set `
    --name $WebAppName `
    --resource-group $ResourceGroupName `
    --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app" `
    --output none

Write-Success "Startup command configured."

# Step 6: Enable HTTPS only
Write-Info "Step 6: Enabling HTTPS only..."
az webapp update `
    --name $WebAppName `
    --resource-group $ResourceGroupName `
    --https-only true `
    --output none

Write-Success "HTTPS only enabled."

# Step 7: Ensure Web App is started
Write-Info "Step 7: Ensuring web app is started..."
az webapp start `
    --name $WebAppName `
    --resource-group $ResourceGroupName `
    --output none

if ($LASTEXITCODE -eq 0) {
    Write-Success "Web app is now running."
} else {
    Write-Warning "Could not start web app, but continuing with deployment..."
}

# Step 8: Deploy the application
Write-Info "Step 8: Deploying application code..."
Write-Info "Creating deployment package from src folder..."

try {
    # Create a temporary zip file for deployment
    $tempZipPath = Join-Path $env:TEMP "leave-app-deployment.zip"
    
    # Remove existing zip if it exists
    if (Test-Path $tempZipPath) {
        Remove-Item $tempZipPath -Force
    }
    
    # Create zip file from src directory
    Write-Info "Compressing source files..."
    Compress-Archive -Path "src\*" -DestinationPath $tempZipPath -Force
    
    # Ensure the web app is running before deployment
    Write-Info "Verifying web app status before deployment..."
    
    # Wait a bit for the app to be fully started
    Start-Sleep -Seconds 5
    
    # Check web app state
    $webappState = az webapp show --name $WebAppName --resource-group $ResourceGroupName --query "state" --output tsv
    Write-Info "Current web app state: $webappState"
    
    if ($webappState -ne "Running") {
        Write-Warning "Web app is not running. Starting it again..."
        az webapp start --name $WebAppName --resource-group $ResourceGroupName --output none
        Start-Sleep -Seconds 10
    }
    
    # Try deployment with retries
    $maxRetries = 3
    $retryCount = 0
    $deploymentSuccess = $false
    
    while ($retryCount -lt $maxRetries -and -not $deploymentSuccess) {
        $retryCount++
        Write-Info "Deployment attempt $retryCount of $maxRetries..."
        
        # Deploy using the new az webapp deploy command
        Write-Info "Uploading deployment package..."
        az webapp deploy `
            --name $WebAppName `
            --resource-group $ResourceGroupName `
            --src-path $tempZipPath `
            --type zip `
            --output none
        
        if ($LASTEXITCODE -eq 0) {
            $deploymentSuccess = $true
            Write-Success "Application deployed successfully."
        } else {
            Write-Warning "Deployment attempt $retryCount failed."
            if ($retryCount -lt $maxRetries) {
                Write-Info "Waiting 10 seconds before retry..."
                Start-Sleep -Seconds 10
                
                # Ensure app is still running before retry
                az webapp start --name $WebAppName --resource-group $ResourceGroupName --output none
                Start-Sleep -Seconds 5
            }
        }
    }
    
    if (-not $deploymentSuccess) {
        Write-Error "Failed to deploy application after $maxRetries attempts."
        Write-Error "Please check the web app status in Azure Portal: https://portal.azure.com"
        exit 1
    }
    
    # Clean up temporary zip file
    if (Test-Path $tempZipPath) {
        Remove-Item $tempZipPath -Force
    }
    
} catch {
    Write-Error "Failed to deploy application: $($_.Exception.Message)"
    exit 1
}

# Step 9: Restart the web app
Write-Info "Step 9: Restarting web app..."
az webapp restart `
    --name $WebAppName `
    --resource-group $ResourceGroupName `
    --output none

Write-Success "Web app restarted."

# Final output
Write-Success "========================================"
Write-Success "Deployment completed successfully!"
Write-Success "========================================"
Write-Success "Resource Group: $ResourceGroupName"
Write-Success "Web App Name: $WebAppName"
Write-Success "App URL: $appUrl"
Write-Success "========================================"

Write-Info "Next steps:"
Write-Info "1. Visit your app at: $appUrl"
Write-Info "2. Check logs with: az webapp log tail --name $WebAppName --resource-group $ResourceGroupName"
Write-Info "3. Monitor your app in Azure Portal"

# Optional: Open the app in browser
$openBrowser = Read-Host "Do you want to open the app in your browser? (y/N)"
if ($openBrowser -eq 'y' -or $openBrowser -eq 'Y') {
    Start-Process $appUrl
}

Write-Success "Deployment script completed!"
