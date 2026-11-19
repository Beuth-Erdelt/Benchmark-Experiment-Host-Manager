#!/bin/bash
# Installs Microsoft's ODBC driver and command-line tools (sqlcmd, bcp) at the start of
# the container, not at build time.
#
# The licence terms of msodbcsql18 and mssql-tools18 do not allow publishing them in an
# image (mssql-tools18: no publishing for others to copy, distribution only for Windows;
# msodbcsql18: only as REDIST code inside one's own application, with an indemnity for
# Microsoft). So the public images of bexhoma contain no Microsoft software, and every
# pod installs the packages from packages.microsoft.com itself. Running the loader means
# accepting Microsoft's licence terms (ACCEPT_EULA=Y), as deploying SQL Server does.
# The image contains the repository configuration (packages-microsoft-prod, MIT) and the
# open-source dependencies of the packages.
#
# The packages are cached on the data volume (MSSQL_TOOLS_CACHE, default /data/drivers),
# so they are downloaded once per version; several pods starting at the same time each
# download into their own folder and move it into place, the first wins. Without a
# writable data volume they are downloaded into /tmp.
#
# Sourced by loader.sh. Exits the loader with 1 if the tools cannot be installed.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

MSSQL_TOOLS_VERSION="${MSSQL_TOOLS_VERSION:-18.7.1.1-1}"
MSSQL_TOOLS_CACHE="${MSSQL_TOOLS_CACHE:-/data/drivers}"
if command -v sqlcmd >/dev/null && command -v bcp >/dev/null; then
    echo "mssql-tools18 already installed"
else
    if ! mkdir -p "$MSSQL_TOOLS_CACHE" 2>/dev/null || [ ! -w "$MSSQL_TOOLS_CACHE" ]; then
        echo "Driver cache $MSSQL_TOOLS_CACHE not writable, using /tmp/drivers"
        MSSQL_TOOLS_CACHE=/tmp/drivers
        mkdir -p "$MSSQL_TOOLS_CACHE"
    fi
    MSSQL_TOOLS_DIR="$MSSQL_TOOLS_CACHE/mssql-tools18-$MSSQL_TOOLS_VERSION"
    if [ -f "$MSSQL_TOOLS_DIR/msodbcsql18.deb" ] && [ -f "$MSSQL_TOOLS_DIR/mssql-tools18.deb" ]; then
        echo "msodbcsql18 and mssql-tools18 $MSSQL_TOOLS_VERSION found in $MSSQL_TOOLS_DIR"
    else
        echo "Downloading msodbcsql18 and mssql-tools18 $MSSQL_TOOLS_VERSION from packages.microsoft.com into $MSSQL_TOOLS_DIR"
        MSSQL_TOOLS_TMP="$MSSQL_TOOLS_DIR.tmp.$(hostname).$$"
        rm -rf "$MSSQL_TOOLS_TMP"
        mkdir -p "$MSSQL_TOOLS_TMP"
        # only the Microsoft repository is read
        if ! apt-get update -qq \
                -o Dir::Etc::sourcelist=sources.list.d/microsoft-prod.list \
                -o Dir::Etc::sourceparts=- -o APT::Get::List-Cleanup=0 \
            || ! (cd "$MSSQL_TOOLS_TMP" \
                && apt-get download -qq -o APT::Sandbox::User=root "msodbcsql18=$MSSQL_TOOLS_VERSION" "mssql-tools18=$MSSQL_TOOLS_VERSION" \
                && mv msodbcsql18_*.deb msodbcsql18.deb \
                && mv mssql-tools18_*.deb mssql-tools18.deb); then
            echo "ERROR: cannot download msodbcsql18 and mssql-tools18 $MSSQL_TOOLS_VERSION"
            rm -rf "$MSSQL_TOOLS_TMP"
            exit 1
        fi
        # another pod may have been faster: then its folder stays and this one is removed
        mv -T "$MSSQL_TOOLS_TMP" "$MSSQL_TOOLS_DIR" 2>/dev/null || rm -rf "$MSSQL_TOOLS_TMP"
    fi
    if ! ACCEPT_EULA=Y DEBIAN_FRONTEND=noninteractive dpkg -i \
            "$MSSQL_TOOLS_DIR/msodbcsql18.deb" "$MSSQL_TOOLS_DIR/mssql-tools18.deb" > /tmp/install-tools.log 2>&1 \
        || ! command -v bcp >/dev/null; then
        cat /tmp/install-tools.log
        echo "ERROR: cannot install msodbcsql18 and mssql-tools18 $MSSQL_TOOLS_VERSION"
        exit 1
    fi
    echo "Installed msodbcsql18 and mssql-tools18 $MSSQL_TOOLS_VERSION"
fi
