[CmdletBinding()]
param(
    [string]$BaseUrl,
    [string]$Model,
    [SecureString]$SecureApiKey
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$envPath = Join-Path $projectRoot "backend\.env"
$examplePath = Join-Path $projectRoot "backend\.env.example"

function ConvertTo-DotEnvValue {
    param([Parameter(Mandatory)][string]$Value)

    if ($Value.Contains("`r") -or $Value.Contains("`n")) {
        throw "Configuration values cannot contain line breaks."
    }
    $escaped = $Value.Replace("\", "\\").Replace('"', '\"')
    return '"' + $escaped + '"'
}

function Set-DotEnvValue {
    param(
        [Parameter(Mandatory)][AllowEmptyString()][string[]]$Lines,
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$Value
    )

    $entry = "$Name=$(ConvertTo-DotEnvValue -Value $Value)"
    $updated = [System.Collections.Generic.List[string]]::new()
    $found = $false
    foreach ($line in $Lines) {
        if ($line -match "^\s*$([regex]::Escape($Name))\s*=") {
            if (-not $found) {
                $updated.Add($entry)
                $found = $true
            }
        }
        else {
            $updated.Add($line)
        }
    }
    if (-not $found) {
        $updated.Add($entry)
    }
    return $updated.ToArray()
}

if (-not $BaseUrl) {
    $BaseUrl = Read-Host "OpenAI-compatible base URL [https://api.openai.com/v1]"
}
if ([string]::IsNullOrWhiteSpace($BaseUrl)) {
    $BaseUrl = "https://api.openai.com/v1"
}
$BaseUrl = $BaseUrl.Trim().TrimEnd("/")

if (-not [Uri]::IsWellFormedUriString($BaseUrl, [UriKind]::Absolute)) {
    throw "Base URL must be an absolute HTTP or HTTPS URL."
}
$baseUri = [Uri]$BaseUrl
if ($baseUri.Scheme -notin @("http", "https")) {
    throw "Base URL must use HTTP or HTTPS."
}

$secureKey = if ($SecureApiKey) { $SecureApiKey } else { Read-Host "API key (input is hidden)" -AsSecureString }
$credential = [System.Net.NetworkCredential]::new("", $secureKey)
$providerKey = $credential.Password
if ([string]::IsNullOrWhiteSpace($providerKey)) {
    throw "API key cannot be empty."
}

$models = @()
try {
    $headers = @{ Authorization = "Bearer $providerKey" }
    $response = Invoke-RestMethod -Method Get -Uri "$BaseUrl/models" -Headers $headers -TimeoutSec 15
    $models = @($response.data | ForEach-Object { $_.id } | Where-Object { $_ } | Sort-Object -Unique)
}
catch {
    Write-Warning "Could not fetch $BaseUrl/models. The relay may not expose an OpenAI-compatible model list."
}

if (-not $Model -and $models.Count -gt 0) {
    Write-Host "`nAvailable models:" -ForegroundColor Cyan
    for ($index = 0; $index -lt $models.Count; $index++) {
        Write-Host ("[{0}] {1}" -f ($index + 1), $models[$index])
    }
    do {
        $selection = Read-Host "Choose model number"
        $selectedIndex = 0
        $validSelection = [int]::TryParse($selection, [ref]$selectedIndex) -and $selectedIndex -ge 1 -and $selectedIndex -le $models.Count
        if (-not $validSelection) {
            Write-Warning "Enter a number from 1 to $($models.Count)."
        }
    } until ($validSelection)
    $Model = $models[$selectedIndex - 1]
}
elseif (-not $Model) {
    $Model = Read-Host "Model ID"
}

if ([string]::IsNullOrWhiteSpace($Model)) {
    throw "Model ID cannot be empty."
}
if ($models.Count -gt 0 -and $Model -notin $models) {
    Write-Warning "The selected model was not returned by the relay's model list."
}

if (Test-Path -LiteralPath $envPath) {
    $lines = @(Get-Content -LiteralPath $envPath)
}
elseif (Test-Path -LiteralPath $examplePath) {
    $lines = @(Get-Content -LiteralPath $examplePath)
}
else {
    $lines = @()
}

$lines = Set-DotEnvValue -Lines $lines -Name "OPENAI_API_KEY" -Value $providerKey
$lines = Set-DotEnvValue -Lines $lines -Name "AI_BASE_URL" -Value $BaseUrl
$lines = Set-DotEnvValue -Lines $lines -Name "AI_MODEL" -Value $Model.Trim()
Set-Content -LiteralPath $envPath -Value $lines -Encoding utf8

$credential.Password = ""
$providerKey = $null

Write-Host "`nAI provider configured successfully." -ForegroundColor Green
Write-Host "Base URL: $BaseUrl"
Write-Host "Model:    $($Model.Trim())"
Write-Host "Saved to backend/.env (ignored by Git). Restart the backend to apply changes."
