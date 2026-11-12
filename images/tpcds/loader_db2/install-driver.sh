#!/bin/bash
# Installs the Db2 client of the loader at the start of the container, not at build time.
#
# ibm_db (PyPI) contains IBM's Data Server Driver for ODBC and CLI. Its license allows
# passing it on only together with an end-user license that protects IBM as much as
# IBM's, which the public images of bexhoma (AGPL) cannot give: so the images contain
# no IBM software, and every pod downloads the driver from PyPI itself.
#
# The installation is cached on the data volume (DB2_DRIVER_CACHE, default
# /data/drivers), so it is downloaded once per version; several pods starting at the
# same time each install into their own folder and move it into place, the first wins.
# Without a writable data volume it is installed into /tmp.
#
# Sourced by loader.sh: exports PYTHONPATH. Exits the loader with 1 if the driver
# cannot be installed.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

IBM_DB_VERSION="${IBM_DB_VERSION:-3.2.6}"
DB2_DRIVER_CACHE="${DB2_DRIVER_CACHE:-/data/drivers}"
if ! mkdir -p "$DB2_DRIVER_CACHE" 2>/dev/null || [ ! -w "$DB2_DRIVER_CACHE" ]; then
    echo "Driver cache $DB2_DRIVER_CACHE not writable, using /tmp/drivers"
    DB2_DRIVER_CACHE=/tmp/drivers
    mkdir -p "$DB2_DRIVER_CACHE"
fi
IBM_DB_DIR="$DB2_DRIVER_CACHE/ibm_db-$IBM_DB_VERSION"
if PYTHONPATH="$IBM_DB_DIR" python3 -c "import ibm_db" 2>/dev/null; then
    echo "ibm_db $IBM_DB_VERSION found in $IBM_DB_DIR"
else
    echo "Installing ibm_db $IBM_DB_VERSION (with IBM Data Server Driver for ODBC and CLI) from PyPI into $IBM_DB_DIR"
    IBM_DB_TMP="$IBM_DB_DIR.tmp.$(hostname).$$"
    rm -rf "$IBM_DB_TMP"
    if ! pip install --no-cache-dir --quiet --disable-pip-version-check --target "$IBM_DB_TMP" "ibm_db==$IBM_DB_VERSION"; then
        echo "ERROR: cannot install ibm_db $IBM_DB_VERSION"
        rm -rf "$IBM_DB_TMP"
        exit 1
    fi
    # another pod may have been faster: then its folder stays and this one is removed
    mv -T "$IBM_DB_TMP" "$IBM_DB_DIR" 2>/dev/null || rm -rf "$IBM_DB_TMP"
    if ! PYTHONPATH="$IBM_DB_DIR" python3 -c "import ibm_db"; then
        echo "ERROR: ibm_db $IBM_DB_VERSION cannot be imported from $IBM_DB_DIR"
        exit 1
    fi
fi
export PYTHONPATH="$IBM_DB_DIR${PYTHONPATH:+:$PYTHONPATH}"
