# Script pour configurer Render MCP Server dans Cursor
# Usage: .\scripts\configurer_render_mcp.ps1 -ApiKey "votre_cle_api"

param(
    [Parameter(Mandatory=$true)]
    [string]$ApiKey
)

$mcpConfigPath = "$env:USERPROFILE\.cursor\mcp.json"
$cursorDir = "$env:USERPROFILE\.cursor"

# Créer le dossier .cursor s'il n'existe pas
if (-not (Test-Path $cursorDir)) {
    New-Item -ItemType Directory -Path $cursorDir -Force | Out-Null
    Write-Host "✓ Dossier .cursor créé" -ForegroundColor Green
}

# Configuration MCP avec Supabase et Render
$mcpConfig = @{
    mcpServers = @{
        supabase = @{
            url = "https://mcp.supabase.com/mcp?project_ref=bmfkvwpfeuyserrfrqjb"
            headers = @{}
        }
        render = @{
            url = "https://mcp.render.com/mcp"
            headers = @{
                Authorization = "Bearer $ApiKey"
            }
        }
    }
}

# Convertir en JSON avec indentation
$jsonContent = $mcpConfig | ConvertTo-Json -Depth 10

# Sauvegarder le fichier
try {
    $jsonContent | Out-File -FilePath $mcpConfigPath -Encoding utf8 -Force
    Write-Host "✓ Configuration Render MCP sauvegardée dans $mcpConfigPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "Configuration créée avec succès !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Prochaines étapes :" -ForegroundColor Yellow
    Write-Host "1. Redémarrez Cursor complètement" -ForegroundColor White
    Write-Host "2. Testez la connexion avec : 'Liste mes services Render'" -ForegroundColor White
} catch {
    Write-Host "✗ Erreur lors de la sauvegarde : $_" -ForegroundColor Red
    exit 1
}

