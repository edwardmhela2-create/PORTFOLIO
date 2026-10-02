# ============================================================
# P1 - SYSREPORT: Ripoti ya Mfumo kwa PowerShell
# Endesha: .\sysreport.ps1  (inatengeneza report.html na kufungua)
# Muda wa kiotomatiki: .\sysreport.ps1 -NoBrowser  (hifadhi tu, usifungue browser)
param([switch]$NoBrowser)
# ============================================================

# ---------- HATUA 1: KUKUSANYA DATA ----------
$cpu  = Get-CimInstance Win32_Processor
$os   = Get-CimInstance Win32_OperatingSystem
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$cs   = Get-CimInstance Win32_ComputerSystem
$net  = Get-CimInstance Win32_NetworkAdapterConfiguration -Filter "IPEnabled='True'"
$batt = Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue

$ramGB   = [math]::Round($cs.TotalPhysicalMemory/1GB, 1)
$ramFree = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB, 1)
$diskGB  = [math]::Round($disk.Size/1GB, 1)
$freeGB  = [math]::Round($disk.FreeSpace/1GB, 1)
$usedPct = [math]::Round(100 - ($disk.FreeSpace/$disk.Size*100), 0)
$uptime  = (Get-Date) - $os.LastBootUpTime
$ip      = $net.IPAddress | Where-Object { $_ -like '192.*' -or $_ -like '10.*' } | Select-Object -First 1
$gw      = $net.DefaultIPGateway | Select-Object -First 1
$mac     = $net.MACAddress | Select-Object -First 1

# Programu zilizosakinishwa (njia ya haraka - registry, si Win32_Product)
$apps = Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue |
        Where-Object DisplayName |
        Select-Object DisplayName, DisplayVersion, Publisher |
        Sort-Object DisplayName
$appCount = ($apps | Measure-Object).Count

# ---------- HATUA 2: ALAMA ZA TAHADHARI (status) ----------
function Get-Status([int]$pct, [int]$warn = 60, [int]$crit = 80) {
    if ($pct -ge $crit) { return @('#e74c3c', '#fff', 'SEPETU') }
    if ($pct -ge $warn) { return @('#f39c12', '#fff', 'ONYO') }
    return @('#27ae60', '#fff', 'SAWA')
}
$diskSt = Get-Status $usedPct
$ramPct = [math]::Round(100 - ($ramFree / $ramGB * 100), 0)
$ramSt  = Get-Status $ramPct 85 95

# ---------- HEALTH SUMMARY (jumla ya afya) ----------
$checks = @(
    @{ Jina = 'Diski';  Hali = $diskSt[2]; Rangi = $diskSt[0] },
    @{ Jina = 'RAM';    Hali = $ramSt[2];  Rangi = $ramSt[0] }
)
if ($batt) {
    $bcol = if ($batt.EstimatedChargeRemaining -le 20) { 'SEPETU'; '#e74c3c' }
            elseif ($batt.EstimatedChargeRemaining -le 50) { 'ONYO'; '#f39c12' }
            else { 'SAWA'; '#27ae60' }
    $checks += @{ Jina = 'Betri'; Hali = $bcol[0]; Rangi = $bcol[1] }
}
$jmSawa  = ($checks | Where-Object { $_.Hali -eq 'SAWA' }).Count
$jmOnyo  = ($checks | Where-Object { $_.Hali -eq 'ONYO' }).Count
$jmSepetu = ($checks | Where-Object { $_.Hali -eq 'SEPETU' }).Count
$afya = if ($jmSepetu -gt 0) { @('INAHITAJI MATENGENEZO', '#e74c3c') }
        elseif ($jmOnyo -gt 0) { @('INA ONYO', '#f39c12') }
        else { @('SAWA VIZURI', '#27ae60') }

# ---------- HATUA 3: KUTENGENEZA HTML ----------
$tarehe = Get-Date -Format "dd/MM/yyyy HH:mm"
$html = @"
<!DOCTYPE html>
<html lang="sw">
<head>
<meta charset="UTF-8">
<title>SYSREPORT - $($cs.Name)</title>
<style>
  body { font-family: 'Segoe UI', Arial, sans-serif; background:#f4f6f9; margin:0; padding:24px; color:#2c3e50; }
  .wrap { max-width: 900px; margin: auto; }
  h1 { background:linear-gradient(135deg,#2c3e50,#3498db); color:#fff; padding:20px 26px; border-radius:10px; margin:0 0 6px; box-shadow:0 4px 10px rgba(0,0,0,.15); }
  .health { display:flex; gap:12px; align-items:center; flex-wrap:wrap; background:#fff; border-radius:10px; padding:14px 18px; margin-bottom:18px; box-shadow:0 2px 6px rgba(0,0,0,.08); border-left:6px solid $($afya[1]); }
  .health .pill { color:#fff; padding:4px 14px; border-radius:16px; font-weight:700; font-size:14px; }
  .sub { color:#7f8c8d; margin-bottom:24px; }
  .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(260px,1fr)); gap:16px; }
  .card { background:#fff; border-radius:10px; padding:18px 20px; box-shadow:0 2px 6px rgba(0,0,0,.08); border-left:6px solid #3498db; }
  .card h3 { margin:0 0 10px; font-size:14px; text-transform:uppercase; letter-spacing:1px; color:#7f8c8d; }
  .big { font-size:26px; font-weight:700; margin:4px 0; }
  .row { display:flex; justify-content:space-between; padding:4px 0; border-bottom:1px dashed #ecf0f1; font-size:14px; }
  .row:last-child { border:none; }
  .badge { color:#fff; padding:2px 10px; border-radius:12px; font-size:12px; font-weight:700; }
  .bar { background:#ecf0f1; border-radius:6px; height:14px; overflow:hidden; margin:8px 0; }
  .bar > div { height:100%; }
  footer { text-align:center; color:#95a5a6; font-size:12px; margin-top:24px; }
</style>
</head>
<body><div class="wrap">
<h1>&#128202; SYSREPORT</h1>
<div class="sub">$($cs.Name) &mdash; Iliyotengenezwa: $tarehe</div>

<div class="health">
  <b>AFYA YA PC:</b>
  <span class="pill" style="background:$($afya[1]);font-size:16px">$($afya[0])</span>
  <span class="pill" style="background:#27ae60">&#10004; $jmSawa SAWA</span>
  <span class="pill" style="background:#f39c12">&#9888; $jmOnyo ONYO</span>
  <span class="pill" style="background:#e74c3c">&#128308; $jmSepetu SEPETU</span>
  <span style="color:#7f8c8d;font-size:13px">Checks: $(($checks | ForEach-Object { $_.Jina }) -join ' | ')</span>
</div>

<div class="grid">

  <div class="card" style="border-left-color:$($diskSt[0])">
    <h3>Diski C:</h3>
    <div class="big">$usedPct% imejaa</div>
    <div class="bar"><div style="width:$usedPct%;background:$($diskSt[0])"></div></div>
    <div class="row"><span>Jumla</span><b>$diskGB GB</b></div>
    <div class="row"><span>Imebaki</span><b>$freeGB GB</b></div>
    <div class="row"><span>Hali</span><span class="badge" style="background:$($diskSt[0])">$($diskSt[2])</span></div>
  </div>

  <div class="card" style="border-left-color:$($ramSt[0])">
    <h3>RAM</h3>
    <div class="big">$ramGB GB</div>
    <div class="bar"><div style="width:$ramPct%;background:$($ramSt[0])"></div></div>
    <div class="row"><span>Imetumika</span><b>$ramPct%</b></div>
    <div class="row"><span>Imebaki</span><b>$ramFree GB</b></div>
    <div class="row"><span>Hali</span><span class="badge" style="background:$($ramSt[0])">$($ramSt[2])</span></div>
  </div>

  <div class="card">
    <h3>Processor (CPU)</h3>
    <div class="row"><span>Jina</span><b>$($cpu.Name)</b></div>
    <div class="row"><span>Core</span><b>$($cpu.NumberOfCores) (thread $($cpu.NumberOfLogicalProcessors))</b></div>
    <div class="row"><span>Kasi</span><b>$([math]::Round($cpu.MaxClockSpeed/1000,1)) GHz</b></div>
  </div>

  <div class="card">
    <h3>Mfumo wa Uendeshaji</h3>
    <div class="row"><span>Mfumo</span><b>$($os.Caption)</b></div>
    <div class="row"><span>Build</span><b>$($os.Version)</b></div>
    <div class="row"><span>Uptime</span><b>siku $($uptime.Days) : saa $($uptime.Hours)</b></div>
  </div>

  <div class="card">
    <h3>Mtandao</h3>
    <div class="row"><span>IP</span><b>$ip</b></div>
    <div class="row"><span>Gateway</span><b>$gw</b></div>
    <div class="row"><span>MAC</span><b>$mac</b></div>
    <div class="row"><span>PC</span><b>$($cs.Manufacturer) $($cs.Model)</b></div>
  </div>

  <div class="card">
    <h3>Programu Zilizosakinishwa</h3>
    <div class="big">$appCount programu</div>
    $(($apps | Select-Object -First 6 | ForEach-Object {
        "<div class='row'><span>$($_.DisplayName)</span><b>$($_.DisplayVersion)</b></div>"
    }) -join "`n")
    <div class="row"><span>Jina zaidi: tumia ripoti kamili</span><b>...</b></div>
  </div>

  <div class="card">
    <h3>Betri</h3>
    $(if ($batt) {
        $bp = $batt.EstimatedChargeRemaining
        $bs = if ($batt.BatteryStatus -eq 1) { 'Inachaji' } else { 'Inatumika' }
        $bcol = if ($bp -le 20) { '#e74c3c' } elseif ($bp -le 50) { '#f39c12' } else { '#27ae60' }
        "<div class='big'>$bp%</div>
         <div class='bar'><div style='width:$bp%;background:$bcol'></div></div>
         <div class='row'><span>Hali</span><b>$bs</b></div>"
    } else { "<div class='big'>Hakuna betri (PC ya mezani)</div>" })
  </div>

</div>

<div class="card" style="margin-top:16px">
  <h3>Orodha Kamili ya Programu</h3>
  <table style="width:100%;border-collapse:collapse;font-size:13px">
    <tr style="background:#2c3e50;color:#fff;text-align:left">
      <th style="padding:6px">#</th><th style="padding:6px">Jina</th>
      <th style="padding:6px">Toleo</th><th style="padding:6px">Mtayarishaji</th>
    </tr>
    $(($apps | ForEach-Object -Begin {$i=0} -Process {
        $i++
        $bg = if ($i % 2 -eq 0) { '#f9f9f9' } else { '#ffffff' }
        "<tr style='background:$bg'><td style='padding:5px'>$i</td><td>$($_.DisplayName)</td><td>$($_.DisplayVersion)</td><td>$($_.Publisher)</td></tr>"
    }) -join "`n")
  </table>
</div>

<footer>SYSREPORT v1.0 &mdash; iliyotengenezwa kwa PowerShell &amp; CIM/WMI &mdash; PORTFOLIO P1</footer>
</div></body></html>
"@

# ---------- HATUA 4: KUHIFADHI NA KUFUNGUA ----------
$dir  = if ($PSScriptRoot) { $PSScriptRoot } else { Get-Location }
$out  = Join-Path $dir "report.html"
$html | Out-File -FilePath $out -Encoding utf8
Write-Host "Ripoti imehifadhiwa: $out" -ForegroundColor Green
if (-not $NoBrowser) { Start-Process $out }
else { Write-Host "(NoBrowser: browser haijafunguliwa - ripoti ipo kwenye faili)" -ForegroundColor Yellow }
