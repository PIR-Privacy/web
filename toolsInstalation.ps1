# Instalation de Chocolatey et de python / navigateur
Start-Process powershell.exe -ArgumentList "-command `"Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y python3; choco install -y pip; choco install -y googlechrome; choco install -y firefox; pause `" " -Verb RunAs -Wait


# Definition des chemins
[string]$curentPath = Get-Location
[string]$chromedriverDriverPathZip = $curentPath + "\chromedriver.zip"
[string]$chromedriverDriverPathFile = $curentPath + "\chromedriver"
[string]$chromedriver = $curentPath + "\chromedriver\chromedriver.exe"
[string]$chromeDriverPath = $curentPath + "\chromedriver.exe"
[string]$firefoxDriverPathZip = $curentPath + "\firefoxdriver.zip"
[string]$firefoxDriverPathFile = $curentPath + "\firefoxdriver"
[string]$geckodriver = $curentPath + "\firefoxdriver\geckodriver.exe"
[string]$pipRequierments = $curentPath + "\requierments.txt"


Write-Output "Telechargement du driver de Google Chrome"
(new-object System.Net.WebClient).DownloadFile('https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_win32.zip', $chromedriverDriverPathZip)
Write-Output "Telechargement du driver de FireFox"
(new-object System.Net.WebClient).DownloadFile('https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip/', $firefoxDriverPathZip)

# Decompression de l'archive et suppression des fichiers
Expand-Archive -LiteralPath $firefoxDriverPathZip -DestinationPath $firefoxDriverPathFile
Copy-Item -Path $geckodriver -Destination .\
Remove-Item -Path $firefoxDriverPathFile -Recurse
Remove-Item -Path $firefoxDriverPathZip

Expand-Archive -LiteralPath $chromedriverDriverPathZip -DestinationPath $chromedriverDriverPathFile
Copy-Item -Path $chromedriver -Destination .\
Remove-Item -Path $chromedriverDriverPathFile -Recurse
Remove-Item -Path $chromedriverDriverPathZip

Write-Output "upgrade de pip et instalation des modules python"
python -m pip install --upgrade pip
pip install -r $pipRequierments

Read-Host -Prompt "Press Enter to continue"