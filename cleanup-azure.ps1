# Azure Cleanup Script for Leave App (PowerShell)
# This script removes all Azure resources created for the Leave App

param(
    [string]$ResourceGroupName = "rg-leave-app-prod"
)

function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }

Write-Warning "========================================"
Write-Warning "Azure Cleanup Script for Leave App"
Write-Warning "========================================"
Write-Warning "This will DELETE the resource group: $ResourceGroupName"
Write-Warning "and ALL resources within it!"
Write-Warning "========================================"

# Check if Azure CLI is installed
try {
    $azVersion = az version --output tsv --query '"azure-cli"'
    Write-Info "Azure CLI version: $azVersion"
} catch {
    Write-Error "Azure CLI is not installed."
    exit 1
}

# Check if logged in
try {
    $account = az account show --output json | ConvertFrom-Json
    Write-Info "Logged in as: $($account.user.name)"
} catch {
    Write-Error "Not logged in to Azure. Please run: az login"
    exit 1
}

# Check if resource group exists
Write-Info "Checking if resource group exists..."
try {
    $rg = az group show --name $ResourceGroupName --output json | ConvertFrom-Json
    Write-Info "Resource group found: $($rg.name)"
} catch {
    Write-Warning "Resource group '$ResourceGroupName' does not exist."
    exit 0
}

# List resources in the group
Write-Info "Resources that will be deleted:"
az resource list --resource-group $ResourceGroupName --output table

Write-Host ""
Write-Warning "Are you sure you want to delete ALL these resources?"
$confirmation = Read-Host "Type 'yes' to confirm"

if ($confirmation -ne "yes") {
    Write-Info "Cleanup cancelled."
    exit 0
}

Write-Info "Deleting resource group and all resources..."
az group delete --name $ResourceGroupName --yes --no-wait

if ($LASTEXITCODE -eq 0) {
    Write-Success "Deletion initiated successfully."
    Write-Info "Note: Deletion is running in the background and may take several minutes."
    Write-Info "You can check the status in the Azure Portal."
} else {
    Write-Error "Failed to initiate deletion."
    exit 1
}

Write-Success "Cleanup script completed!"
