DROP USER 'root'@'%';
FLUSH PRIVILEGES;

CREATE USER 'root'@'%';
ALTER USER 'root'@'%' IDENTIFIED BY 'root';

 -- SET PASSWORD FOR root@'172.17.0.3' = PASSWORD('root');

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- speed up import
SET GLOBAL innodb_buffer_pool_size = 32*1024*1024*1024;
-- SET GLOBAL innodb_log_buffer_size = 16*1024*1024*1024;
SET GLOBAL innodb_flush_log_at_trx_commit =0;

-- SET GLOBAL innodb_redo_log_capacity = 8*1024*1024*1024;

SET GLOBAL max_connections = 1024;

-- do not cache host names
SET GLOBAL host_cache_size=0;

CREATE DATABASE benchbase;
