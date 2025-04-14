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
