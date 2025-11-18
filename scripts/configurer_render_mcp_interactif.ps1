# Script interactif pour configurer Render MCP Server dans Cursor
# Usage: .\scripts\configurer_render_mcp_interactif.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuration Render MCP Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$mcpConfigPath = "$env:USERPROFILE\.cursor\mcp.json"
$cursorDir = "$env:USERPROFILE\.cursor"

# Créer le dossier .cursor s'il n'existe pas
if (-not (Test-Path $cursorDir)) {
    New-Item -ItemType Directory -Path $cursorDir -Force | Out-Null
    Write-Host "✓ Dossier .cursor créé" -ForegroundColor Green
}

Write-Host "Étape 1 : Obtenir votre clé API Render" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pour créer une clé API Render :" -ForegroundColor White
Write-Host "1. Allez sur https://dashboard.render.com" -ForegroundColor Gray
Write-Host "2. Cliquez sur votre nom/avatar en haut à droite" -ForegroundColor Gray
Write-Host "3. Sélectionnez 'Account Settings'" -ForegroundColor Gray
Write-Host "4. Allez dans 'API Keys'" -ForegroundColor Gray
Write-Host "5. Cliquez sur 'New API Key'" -ForegroundColor Gray
Write-Host "6. Donnez un nom (ex: 'Cursor MCP')" -ForegroundColor Gray
Write-Host "7. Copiez la clé API générée" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  IMPORTANT : La clé ne sera affichée qu'une seule fois !" -ForegroundColor Red
Write-Host ""

# Demander la clé API
$apiKey = Read-Host "Collez votre clé API Render ici (ou appuyez sur Entrée pour annuler)"

if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host ""
    Write-Host "Configuration annulée." -ForegroundColor Yellow
    Write-Host "Vous pouvez relancer ce script quand vous aurez votre clé API." -ForegroundColor Gray
    exit 0
}

# Vérifier le format de la clé (commence généralement par "rnd_")
if (-not $apiKey.StartsWith("rnd_")) {
    Write-Host ""
    Write-Host "⚠️  Attention : La clé API Render commence généralement par 'rnd_'" -ForegroundColor Yellow
    $continue = Read-Host "Voulez-vous continuer quand même ? (O/N)"
    if ($continue -ne "O" -and $continue -ne "o" -and $continue -ne "Y" -and $continue -ne "y") {
        Write-Host "Configuration annulée." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "Étape 2 : Configuration du fichier MCP..." -ForegroundColor Yellow

# Lire la configuration existante si elle existe
$existingConfig = @{}
if (Test-Path $mcpConfigPath) {
    try {
        $existingContent = Get-Content $mcpConfigPath -Raw | ConvertFrom-Json
        if ($existingContent.mcpServers) {
            $existingConfig = $existingContent.mcpServers
        }
    } catch {
        Write-Host "⚠️  Erreur lors de la lecture de la configuration existante" -ForegroundColor Yellow
    }
}

# Configuration MCP avec Supabase (si existant) et Render
$mcpConfig = @{
    mcpServers = @{}
}

# Conserver la configuration Supabase si elle existe
if ($existingConfig.supabase) {
    $mcpConfig.mcpServers.supabase = $existingConfig.supabase
    Write-Host "✓ Configuration Supabase conservée" -ForegroundColor Green
}

# Ajouter la configuration Render
$mcpConfig.mcpServers.render = @{
    url = "https://mcp.render.com/mcp"
    headers = @{
        Authorization = "Bearer $apiKey"
    }
}

# Convertir en JSON avec indentation
$jsonContent = $mcpConfig | ConvertTo-Json -Depth 10

# Sauvegarder le fichier
try {
    $jsonContent | Out-File -FilePath $mcpConfigPath -Encoding utf8 -Force
    Write-Host "✓ Configuration Render MCP sauvegardée" -ForegroundColor Green
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Configuration terminée avec succès !" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Prochaines étapes :" -ForegroundColor Yellow
    Write-Host "1. Fermez complètement Cursor (toutes les fenêtres)" -ForegroundColor White
    Write-Host "2. Rouvrez Cursor" -ForegroundColor White
    Write-Host "3. Testez avec : 'Liste mes services Render'" -ForegroundColor White
    Write-Host ""
    Write-Host "Fichier de configuration : $mcpConfigPath" -ForegroundColor Gray
} catch {
    Write-Host ""
    Write-Host "✗ Erreur lors de la sauvegarde : $_" -ForegroundColor Red
    exit 1
}

