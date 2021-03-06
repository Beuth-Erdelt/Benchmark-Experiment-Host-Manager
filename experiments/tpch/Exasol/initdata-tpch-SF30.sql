IMPORT INTO public.customer FROM LOCAL CSV FILE '/data/tpch/SF30/customer.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.lineitem FROM LOCAL CSV FILE '/data/tpch/SF30/lineitem.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.nation FROM LOCAL CSV FILE '/data/tpch/SF30/nation.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.orders FROM LOCAL CSV FILE '/data/tpch/SF30/orders.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.part FROM LOCAL CSV FILE '/data/tpch/SF30/part.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.partsupp FROM LOCAL CSV FILE '/data/tpch/SF30/partsupp.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.region FROM LOCAL CSV FILE '/data/tpch/SF30/region.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.supplier FROM LOCAL CSV FILE '/data/tpch/SF30/supplier.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
