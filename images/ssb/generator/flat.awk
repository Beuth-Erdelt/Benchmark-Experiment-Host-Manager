# Benchmark-Experiment-Host-Manager | images/ssb/generator
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
#
# Second half of the lineorder_flat pipeline (see generator.sh):
#   awk -F'|' -v OFS='|' -f flat.awk supplier.tbl part.tbl -
# Input 1 and 2: supplier.tbl and part.tbl, held in memory as key -> other columns.
# Input 3 (stdin): lineorder joined with customer, 17 lineorder columns followed by
# the 7 customer columns without c_custkey.
# Output (38 columns): lineorder (lo_orderdate, lo_commitdate as YYYY-MM-DD),
# customer, supplier and part columns, each dimension without its key.
# A missing supplier or part key is fatal (exit 1).

function iso_date(d) {
    return substr(d, 1, 4) "-" substr(d, 5, 2) "-" substr(d, 7, 2)
}

FNR == 1 { file++ }

file == 1 {
    key = $1
    sub(/^[^|]*\|/, "")
    supplier[key] = $0
    next
}

file == 2 {
    key = $1
    sub(/^[^|]*\|/, "")
    part[key] = $0
    next
}

{
    if (!($5 in supplier)) {
        print "FATAL: lo_suppkey " $5 " not in supplier (lo_orderkey " $1 ")" > "/dev/stderr"
        exit 1
    }
    if (!($4 in part)) {
        print "FATAL: lo_partkey " $4 " not in part (lo_orderkey " $1 ")" > "/dev/stderr"
        exit 1
    }
    $6 = iso_date($6)
    $16 = iso_date($16)
    print $0, supplier[$5], part[$4]
}
