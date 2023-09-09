IMPORT INTO public.customer CSV DATA ('nodelocal://self/data/tpch/SF1/customer-nobom.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.lineitem CSV DATA ('nodelocal://self/data/tpch/SF1/lineitem-nobom.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.nation CSV DATA ('nodelocal://self/data/tpch/SF1/nation-nobom.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.orders CSV DATA ('nodelocal://self/data/tpch/SF1/orders-nobom.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.part CSV DATA ('nodelocal://self/data/tpch/SF1/part-nobom.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.partsupp CSV DATA ('nodelocal://self/data/tpch/SF1/partsupp-nobom.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.region CSV DATA ('nodelocal://self/data/tpch/SF1/region-nobom.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.supplier CSV DATA ('nodelocal://self/data/tpch/SF1/supplier-nobom.tbl') WITH delimiter = '|', nullif = '';
