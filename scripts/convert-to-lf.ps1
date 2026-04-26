# Converts line endings to LF (Unix-style) in documentation, log, and image files.
#
# Processes .md, .txt, Dockerfile*, .sh, and .py files under docs/, logs_tests/,
# and images/, rewriting each file in UTF-8 without BOM with LF line endings.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

$paths = @(
    "docs",
    "logs_tests",
    "images"
)

foreach ($path in $paths) {
    Get-ChildItem -Path $path -File -Recurse -Include *.md, *.txt, *Dockerfile*, *.sh, *.py | ForEach-Object {

        # --- Dateiinhalt in UTF-8 einlesen ---
        $utf8 = New-Object System.Text.UTF8Encoding($true)  # BOM optional erlauben
        $reader = New-Object System.IO.StreamReader($_.FullName, $utf8)
        $content = $reader.ReadToEnd()
        $reader.Close()

        # --- Zeilenenden konvertieren ---
        $content = $content -replace "`r`n", "`n"

        # --- UTF-8 ohne BOM schreiben ---
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        $writer = New-Object System.IO.StreamWriter($_.FullName, $false, $utf8NoBom)
        $writer.Write($content)
        $writer.Close()

        Write-Host "Verarbeitet: $($_.FullName)"
    }
}
