# Benchmark-Experiment-Host-Manager | experiments/tpch/Clickhouse
# Authors: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Load TPC-H data at scale factor 1 (SF1 ~ 1 GB) into the tpch database
#          using the clickhouse-client CSV importer. The pipe character '|' is
#          used as the field delimiter, matching the dbgen .tbl output format.

cat /data/tpch/SF1/customer.tbl | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.customer FORMAT CSV"
cat /data/tpch/SF1/lineitem.tbl | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.lineitem FORMAT CSV"
cat /data/tpch/SF1/nation.tbl   | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.nation FORMAT CSV"
cat /data/tpch/SF1/orders.tbl   | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.orders FORMAT CSV"
cat /data/tpch/SF1/part.tbl     | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.part FORMAT CSV"
cat /data/tpch/SF1/partsupp.tbl | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.partsupp FORMAT CSV"
cat /data/tpch/SF1/region.tbl   | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.region FORMAT CSV"
cat /data/tpch/SF1/supplier.tbl | clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.supplier FORMAT CSV"
