param(
    [Parameter(Mandatory=$true)]
    [string]$Path
)

# Definiere die erlaubten Textdateiendungen
$textExtensions = @(".txt", ".csv", ".py", ".sh", ".md", ".json", ".log")

# Alle Dateien rekursiv durchlaufen, nur die mit Text-Endungen
Get-ChildItem -Path $Path -Recurse -File | Where-Object { $textExtensions -contains $_.Extension.ToLower() } | ForEach-Object {

    # Datei als Raw-Text lesen
    $content = Get-Content $_.FullName -Raw

    if ($null -ne $content) {
        # CRLF (\r\n) und CR (\r) in LF (\n) umwandeln
        $newContent = $content -replace "`r`n", "`n" -replace "`r", "`n"

        # Nur überschreiben, wenn sich etwas geändert hat
        if ($newContent -ne $content) {
            Set-Content -Path $_.FullName -Value $newContent -NoNewline -Encoding utf8
            Write-Host "Converted: $($_.FullName)"
        }
    }
}

Write-Host "Done."
