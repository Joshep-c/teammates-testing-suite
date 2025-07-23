# CONFIGURACIÓN
$token   = "6e0668ccc5c2d84ba04deaf53f9fb613c36d29fc"   # Tu token SonarCloud
$project = "andre98652_teammates-backend-clean"

# AUTENTICACIÓN
$authBytes  = [Text.Encoding]::ASCII.GetBytes("${token}:")
$authValue  = [Convert]::ToBase64String($authBytes)
$headers    = @{ Authorization = "Basic $authValue" }

# DESCARGAR MÉTRICAS GENERALES
Write-Host "Descargando métricas generales..."
$urlM = "https://sonarcloud.io/api/measures/component?component=$project&metricKeys=bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density,alert_status,reliability_rating,security_rating,sqale_rating,security_hotspots"
$respM = Invoke-RestMethod -Uri $urlM -Headers $headers
$respM | ConvertTo-Json -Depth 5 | Out-File -Encoding UTF8 "measures.json"
Write-Host "Guardado: measures.json"

# FUNCION PARA DESCARGAR TODAS LAS ISSUES
function Get-AllIssues {
    param([string]$Types)
    $page = 1
    $pageSize = 500
    $all = @()

    do {
        $url = "https://sonarcloud.io/api/issues/search?componentKeys=$project&types=$Types&ps=$pageSize&p=$page"
        try {
            $resp = Invoke-RestMethod -Uri $url -Headers $headers -ErrorAction Stop
        } catch {
            Write-Host "Error en página ${page}: $($_.Exception.Message)" -ForegroundColor Red

            break
        }
        if ($null -eq $resp.issues) { break }

        $all += $resp.issues
        Write-Host "Descargadas $($all.Count) / $($resp.paging.total) ($Types)"
        $page++
    } while ($all.Count -lt $resp.paging.total)

    return $all
}

# DESCARGAR ISSUES
Write-Host "`nDescargando issues..."
$issues   = Get-AllIssues "BUG,VULNERABILITY,CODE_SMELL"
$hotspots = Get-AllIssues "SECURITY_HOTSPOTS"

# EXPORTAR A CSV
$issues | Select key,type,severity,rule,message,component,line,creationDate,updateDate,status,resolution,debt |
    Export-Csv -Path "issues_all.csv" -NoTypeInformation -Encoding UTF8

$hotspots | Select key,type,severity,rule,message,component,line,creationDate,updateDate,status,resolution |
    Export-Csv -Path "hotspots_all.csv" -NoTypeInformation -Encoding UTF8

Write-Host "`nExportaciones completadas:"
Write-Host "→ issues_all.csv"
Write-Host "→ hotspots_all.csv"
Write-Host "→ measures.json"
# =========================
# DESCARGAR SECURITY HOTSPOTS (API dedicada)
# =========================
$page = 1
$pageSize = 500
$hotspots = @()
do {
    $url = "https://sonarcloud.io/api/hotspots/search?projectKey=$project&ps=$pageSize&p=$page"
    $resp = Invoke-RestMethod -Uri $url -Headers $headers
    $hotspots += $resp.hotspots
    Write-Host "Descargados $($hotspots.Count) de $($resp.paging.total) hotspots..."
    $page++
} while ($hotspots.Count -lt $resp.paging.total)

# Guardar como CSV
$hotspots |
  Select key,component,securityCategory,severity,message,line,creationDate,status |
  Export-Csv -Path "hotspots_all.csv" -NoTypeInformation -Encoding UTF8

Write-Host "Hotspots exportados a hotspots_all.csv"
