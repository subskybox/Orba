## Script to update Disentangle.orbapreset with a new ModifierData string
## from the clipboard. It then renames the file to force the Orba App to update.
## Copyright (C) 2022 subskybox@gmail.com - All Rights Reserved
## Last revised 05/23/2022
##
## USAGE: ./OrbaDeployDaemon.ps1
##

Write-Host "Orba Deploy Daemon" -ForegroundColor Gray
Write-Host "Listening..."

#requires -Version 2
function Show-Process($Process)
{
  $sig = '
    [DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")] public static extern int SetForegroundWindow(IntPtr hwnd);
  '
  
  $type = Add-Type -MemberDefinition $sig -Name WindowAPI -PassThru
  $hwnd = $process.MainWindowHandle
  $null = $type::ShowWindowAsync($hwnd, 2)
  $null = $type::ShowWindowAsync($hwnd, 4)
  $null = $type::SetForegroundWindow($hwnd)
}

# Check every second for the DEPLOY token in the clipboard
for (;;)
{
	Start-Sleep -Seconds 1
	$modifierData=Get-Clipboard

    if ( $modifierData.StartsWith("DEPLOY") -And ($modifierData.length -eq 242) ) {
        Write-Host "Deploying..."

        # Trim the token from the clipboard to prevent redeployment
	    $modifierData=$modifierData.substring(6)
	    Set-Clipboard -Value $modifierData

        # Change directory to the Orba Chords folder
        cd $env:USERPROFILE\AppData\Roaming\Artiphon\Orba\Presets\Chords\

        # Create the file Disentangle.orbapreset if it doesn't exist
        if ((Test-Path -Path Disentangle.orbapreset -PathType Leaf) -eq $False){
	        cp 1981.orbapreset Disentangle.orbapreset
        }

        # If the clipboard contains a new modifierData string
	    # Replace the old modifierData string with the new one (from the clipboard)
        if ($modifierData.length -eq 236){
            $filename = $PWD.Path + "\" + "Disentangle.orbapreset"
            [regex]$pattern='modifierData="[^"]*"'
            $newModifierDataStr = 'modifierData="' + $modifierData + '"'
            $pattern.replace([IO.File]::ReadAllText($filename),$newModifierDataStr,1) |
            set-content $filename
        }

        # Rename Disentangle.orbapreset twice to force the Orba App to pickup the change
	    mv Disentangle.orbapreset tmp.tmp
	    Start-Sleep -Seconds 2
	    mv tmp.tmp Disentangle.orbapreset
	    Start-Sleep -Seconds 2
	    Write-Host ("[{0:MM/dd/yy} {0:HH:mm:ss}] " -f (Get-Date)) -NoNewline
        Write-Host "Deployed" -ForegroundColor White -BackgroundColor DarkGreen -NoNewline
        Write-Host " - Load " -NoNewline
        Write-Host "Disentangle " -ForegroundColor Gray -NoNewline
        Write-Host "voice from the Orba Chord Presets."

        # Launch the Orba App if it doesn't exist or bring the window to the front if it does
        $orbaApp = Get-Process Orba -ErrorAction SilentlyContinue
        if ($orbaApp) {
            Show-Process -Process $orbaApp
        } else {
            Start-Process -FilePath “C:\Program Files\Artiphon\Orba\Orba.exe”
            Start-Sleep -Seconds 2
            $orbaApp = Get-Process Orba -ErrorAction SilentlyContinue
            if ($orbaApp) {
                Show-Process -Process $orbaApp
            }
        }
        Remove-Variable orbaApp
    }
}