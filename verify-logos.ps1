# Logo Verification Script
Write-Host "`n=== PowerFuel Logo Verification ===" -ForegroundColor Cyan
Write-Host ""

$logoPath = "d:\Harun\Projects\powerfuel_final\static\images"
$requiredLogos = @("logo_white_bg.png", "logo_transparent.png")
$allGood = $true

foreach ($logo in $requiredLogos) {
    $fullPath = Join-Path $logoPath $logo
    if (Test-Path $fullPath) {
        $fileInfo = Get-Item $fullPath
        if ($fileInfo.Length -gt 1000) {
            Write-Host "OK $logo - Size: $([math]::Round($fileInfo.Length / 1KB, 2)) KB" -ForegroundColor Green
        } else {
            Write-Host "FAIL $logo - File too small" -ForegroundColor Yellow
            $allGood = $false
        }
    } else {
        Write-Host "FAIL $logo - NOT FOUND" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host ""
if ($allGood) {
    Write-Host "All logos verified! Ready to commit and push." -ForegroundColor Green
} else {
    Write-Host "Please save logo files to: $logoPath" -ForegroundColor Yellow
}
Write-Host ""
