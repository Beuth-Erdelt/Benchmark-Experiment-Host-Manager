ANALYZE VERBOSE public.customer;
ANALYZE VERBOSE public.lineitem;
ANALYZE VERBOSE public.nation;
ANALYZE VERBOSE public.orders;
ANALYZE VERBOSE public.part;
ANALYZE VERBOSE public.partsupp;
ANALYZE VERBOSE public.region;
ANALYZE VERBOSE public.supplier;

SELECT COUNT(*) AS "count nation" FROM nation;
SELECT COUNT(*) AS "count region" FROM region;
