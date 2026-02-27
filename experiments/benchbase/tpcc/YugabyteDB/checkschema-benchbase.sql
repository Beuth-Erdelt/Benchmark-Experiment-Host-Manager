select 'yb_table_properties.warehouse' as msg;
SELECT * FROM yb_table_properties('warehouse'::regclass);

select 'yb_table_properties.item' as msg;
SELECT * FROM yb_table_properties('item'::regclass);

select 'yb_table_properties.stock' as msg;
SELECT * FROM yb_table_properties('stock'::regclass);

select 'yb_table_properties.district' as msg;
SELECT * FROM yb_table_properties('district'::regclass);

select 'yb_table_properties.customer' as msg;
SELECT * FROM yb_table_properties('customer'::regclass);

select 'yb_table_properties.history' as msg;
SELECT * FROM yb_table_properties('history'::regclass);

select 'yb_table_properties.oorder' as msg;
SELECT * FROM yb_table_properties('oorder'::regclass);

select 'yb_table_properties.new_order' as msg;
SELECT * FROM yb_table_properties('new_order'::regclass);

select 'yb_table_properties.order_line' as msg;
SELECT * FROM yb_table_properties('order_line'::regclass);

select 'yb_servers' as msg;
SELECT * -- public_ip, yb_local_tablets.*
FROM yb_servers()
JOIN yb_local_tablets ON true;

-- Check the actual max allowed connections
SHOW max_connections;

-- Check if the YSQL connection manager is enabled
-- SHOW ysql_conn_mgr_max_client_connections;
-- SHOW ysql_conn_mgr_max_conns_per_db;

-- Optional: How many connections are currently in use
SELECT count(*) AS active_connections FROM pg_stat_activity;
