# Benchmark-Experiment-Host-Manager | experiments/tpch/Clickhouse
# Authors: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Load TPC-H data at scale factor 10 (SF10 ≈ 10 GB) into the tpch database
#          using the clickhouse-client CSV importer. The pipe character '|' is
#          used as the field delimiter, matching the dbgen .tbl output format.

cat /data/tpch/SF10/customer.tbl | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.customer FORMAT CSV"
cat /data/tpch/SF10/lineitem.tbl | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.lineitem FORMAT CSV"
cat /data/tpch/SF10/nation.tbl   | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.nation FORMAT CSV"
cat /data/tpch/SF10/orders.tbl   | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.orders FORMAT CSV"
cat /data/tpch/SF10/part.tbl     | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.part FORMAT CSV"
cat /data/tpch/SF10/partsupp.tbl | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.partsupp FORMAT CSV"
cat /data/tpch/SF10/region.tbl   | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.region FORMAT CSV"
cat /data/tpch/SF10/supplier.tbl | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.supplier FORMAT CSV"
