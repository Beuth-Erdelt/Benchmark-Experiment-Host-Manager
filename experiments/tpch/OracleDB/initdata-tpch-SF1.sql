ALTER SESSION SET nls_date_format='YYYY-MM-DD';

INSERT /*+ APPEND */ INTO  tpch.part     SELECT * FROM tpch.ext_part;
INSERT /*+ APPEND */ INTO  tpch.supplier SELECT * FROM tpch.ext_supplier;
INSERT /*+ APPEND */ INTO  tpch.partsupp SELECT * FROM tpch.ext_partsupp;
INSERT /*+ APPEND */ INTO  tpch.customer SELECT * FROM tpch.ext_customer;
INSERT /*+ APPEND */ INTO  tpch.orders   SELECT * FROM tpch.ext_orders;
INSERT /*+ APPEND */ INTO  tpch.lineitem SELECT * FROM tpch.ext_lineitem;
INSERT /*+ APPEND */ INTO  tpch.nation   SELECT * FROM tpch.ext_nation;
INSERT /*+ APPEND */ INTO  tpch.region   SELECT * FROM tpch.ext_region;
