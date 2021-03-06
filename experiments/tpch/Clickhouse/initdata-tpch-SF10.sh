clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.customer FORMAT CSV" < /data/tpch/SF10/customer.tbl
clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.lineitem FORMAT CSV" < /data/tpch/SF10/lineitem.tbl
clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.nation FORMAT CSV" < /data/tpch/SF10/nation.tbl
clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.orders FORMAT CSV" < /data/tpch/SF10/orders.tbl
clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.part FORMAT CSV" < /data/tpch/SF10/part.tbl
clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.partsupp FORMAT CSV" < /data/tpch/SF10/partsupp.tbl
clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.region FORMAT CSV" < /data/tpch/SF10/region.tbl
clickhouse-client --format_csv_delimiter="|" --query="INSERT INTO tpch.supplier FORMAT CSV" < /data/tpch/SF10/supplier.tbl
