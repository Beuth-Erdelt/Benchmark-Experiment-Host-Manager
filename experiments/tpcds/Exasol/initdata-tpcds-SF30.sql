IMPORT INTO public.call_center FROM LOCAL CSV FILE '/data/tpcds/SF30/call_center.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.catalog_page FROM LOCAL CSV FILE '/data/tpcds/SF30/catalog_page.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.catalog_returns FROM LOCAL CSV FILE '/data/tpcds/SF30/catalog_returns.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.catalog_sales FROM LOCAL CSV FILE '/data/tpcds/SF30/catalog_sales.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.customer FROM LOCAL CSV FILE '/data/tpcds/SF30/customer.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.customer_address FROM LOCAL CSV FILE '/data/tpcds/SF30/customer_address.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.customer_demographics FROM LOCAL CSV FILE '/data/tpcds/SF30/customer_demographics.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.date_dim FROM LOCAL CSV FILE '/data/tpcds/SF30/date_dim.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.dbgen_version FROM LOCAL CSV FILE '/data/tpcds/SF30/dbgen_version.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.household_demographics FROM LOCAL CSV FILE '/data/tpcds/SF30/household_demographics.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.income_band FROM LOCAL CSV FILE '/data/tpcds/SF30/income_band.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.inventory FROM LOCAL CSV FILE '/data/tpcds/SF30/inventory.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.item FROM LOCAL CSV FILE '/data/tpcds/SF30/item.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.promotion FROM LOCAL CSV FILE '/data/tpcds/SF30/promotion.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.reason FROM LOCAL CSV FILE '/data/tpcds/SF30/reason.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.ship_mode FROM LOCAL CSV FILE '/data/tpcds/SF30/ship_mode.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.store FROM LOCAL CSV FILE '/data/tpcds/SF30/store.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.store_returns FROM LOCAL CSV FILE '/data/tpcds/SF30/store_returns.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.store_sales FROM LOCAL CSV FILE '/data/tpcds/SF30/store_sales.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.time_dim FROM LOCAL CSV FILE '/data/tpcds/SF30/time_dim.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.warehouse FROM LOCAL CSV FILE '/data/tpcds/SF30/warehouse.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.web_page FROM LOCAL CSV FILE '/data/tpcds/SF30/web_page.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.web_returns FROM LOCAL CSV FILE '/data/tpcds/SF30/web_returns.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.web_sales FROM LOCAL CSV FILE '/data/tpcds/SF30/web_sales.dat' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.web_site FROM LOCAL CSV FILE '/data/tpcds/SF30/web_site.dat' COLUMN SEPARATOR = '|' SKIP = 0;

