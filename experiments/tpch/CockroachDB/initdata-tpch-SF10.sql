IMPORT INTO public.customer CSV DATA ('nodelocal://self/data/tpch/SF10/customer.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.lineitem CSV DATA ('nodelocal://self/data/tpch/SF10/lineitem.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.nation CSV DATA ('nodelocal://self/data/tpch/SF10/nation.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.orders CSV DATA ('nodelocal://self/data/tpch/SF10/orders.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.part CSV DATA ('nodelocal://self/data/tpch/SF10/part.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.partsupp CSV DATA ('nodelocal://self/data/tpch/SF10/partsupp.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.region CSV DATA ('nodelocal://self/data/tpch/SF10/region.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.supplier CSV DATA ('nodelocal://self/data/tpch/SF10/supplier.tbl') WITH delimiter = '|', nullif = '';
