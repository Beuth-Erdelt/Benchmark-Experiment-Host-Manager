
VACUUM ANALYZE customer;
VACUUM ANALYZE district;
VACUUM ANALYZE history;
VACUUM ANALYZE warehouse;
VACUUM ANALYZE stock;
VACUUM ANALYZE new_order;
VACUUM ANALYZE oorder;
VACUUM ANALYZE order_line;
VACUUM ANALYZE item;

SELECT COUNT(*) AS "count warehouses" FROM warehouse;

