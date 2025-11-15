# Script PowerShell pour envoyer les alertes de leçons quotidiennement
# Usage: Ce script doit être exécuté par le Planificateur de tâches Windows

# Aller dans le répertoire du projet
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectPath = Join-Path $scriptPath ".."
Set-Location $projectPath

# Activer l'environnement virtuel (si présent)
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
}

# Exécuter la commande Django
python manage.py envoyer_alertes_lecons

# Désactiver l'environnement virtuel
if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    deactivate
}

# Log de l'exécution
$logPath = Join-Path $projectPath "logs\alertes_lecons.log"
$logDir = Split-Path -Parent $logPath
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logPath -Value "[$timestamp] Commande envoyer_alertes_lecons executee"

